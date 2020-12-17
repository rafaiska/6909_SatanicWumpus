import random

import room


class World(object):
    def __init__(self, width, height, seed=None):
        self.seed = seed
        self.rooms = {}
        self.width = width
        self.height = height
        self.is_hero_dead = False
        self.found_gold = False

    def __str__(self):
        retv = ''
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in self.rooms.keys():
                    retv += str(self.rooms[i, j].objects)
                else:
                    retv += 'VAZIO'
                retv += ', '
            retv += '\n'
        return retv

    def random_location(self):
        posi = random.choice(range(self.height))
        posj = random.choice(range(self.width))
        return posi, posj

    def find_hero(self):
        for pos in self.rooms:
            if self.rooms[pos].has_hero():
                return pos
        return None

    def get_current_room(self):
        pos = self.find_hero()
        return self.rooms[pos]

    def generate_rooms(self):
        for i in range(self.height):
            for j in range(self.width):
                self.rooms[i, j] = room.Room(j, i)

    def place_breezes_around(self, i, j):
        if (i + 1, j) in self.rooms.keys():
            self.rooms[i + 1, j].add_breeze()
        if (i - 1, j) in self.rooms.keys():
            self.rooms[i - 1, j].add_breeze()
        if (i, j + 1) in self.rooms.keys():
            self.rooms[i, j + 1].add_breeze()
        if (i, j - 1) in self.rooms.keys():
            self.rooms[i, j - 1].add_breeze()

    def place_stenches_around(self, i, j):
        if (i + 1, j) in self.rooms.keys():
            self.rooms[i + 1, j].add_stench()
        if (i - 1, j) in self.rooms.keys():
            self.rooms[i - 1, j].add_stench()
        if (i, j + 1) in self.rooms.keys():
            self.rooms[i, j + 1].add_stench()
        if (i, j - 1) in self.rooms.keys():
            self.rooms[i, j - 1].add_stench()

    def place_pits(self, npits):
        pits_to_place = npits
        while pits_to_place:
            i, j = self.random_location()
            room_to_place = self.rooms[i, j]
            if room_to_place.can_place_entity():
                self.rooms[i, j].add_pit()
                pits_to_place -= 1
                self.place_breezes_around(i, j)

    def place_wumpus(self):
        wumpusplaced = False
        while not wumpusplaced:
            i, j = self.random_location()
            room_to_place = self.rooms[i, j]
            if room_to_place.can_place_entity():
                room_to_place.add_wumpus()
                wumpusplaced = True
                self.place_stenches_around(i, j)

    def place_gold(self):
        gold_placed = False
        while not gold_placed:
            i, j = self.random_location()
            room_to_place = self.rooms[i, j]
            if room_to_place.can_place_entity():
                room_to_place.add_gold()
                gold_placed = True

    def place_hero(self):
        hero_placed = False
        while not hero_placed:
            i, j = self.random_location()
            room_to_place = self.rooms[i, j]
            if room_to_place.can_place_entity() and room_to_place.no_hazards_around():
                room_to_place.add_hero()
                room_to_place.explore()
                hero_placed = True

    def populate_rooms(self, npits):
        if self.seed is not None:
            random.seed(self.seed)
        self.place_pits(npits)
        self.place_wumpus()
        self.place_gold()
        self.place_hero()

    def explore_room(self, current_room):
        current_room.explore()
        if current_room.has_wumpus() or current_room.has_pit():
            self.is_hero_dead = True
        elif current_room.has_gold():
            current_room.add_hero()
            self.found_gold = True

    def move_hero(self, direction):
        i, j = self.find_hero()
        prev_room = self.rooms[i, j]
        if direction == 's':
            i += 1
        elif direction == 'n':
            i -= 1
        elif direction == 'e':
            j -= 1
        elif direction == 'w':
            j += 1
        try:
            current_room = self.rooms[i, j]
        except KeyError:
            return False
        prev_room.remove_hero()
        self.explore_room(current_room)
        current_room.add_hero()
        return True

    def random_move(self):
        while not self.move_hero(random.choice(['n', 's', 'e', 'w'])):
            pass

    def setup(self, npits):
        self.generate_rooms()
        self.populate_rooms(npits)

    def reveal_all(self):
        for i in range(self.height):
            for j in range(self.width):
                self.rooms[i, j].explore()

    def fire_arrow(self, arrow_direction):
        step = 1 if arrow_direction in ['s', 'w'] else -1
        hero_pos = self.find_hero()
        if arrow_direction in ['n', 's']:
            for j in range(hero_pos[1] + step, self.height, step):
                self.rooms[hero_pos[0], j].kill_wumpus()
        else:
            for i in range(hero_pos[0] + step, self.width, step):
                self.rooms[i, hero_pos[1]].kill_wumpus()
