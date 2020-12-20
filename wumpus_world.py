import random

import room


class Action(object):
    def __init__(self, action_type, direction):
        if action_type not in ['a', 'm']:
            raise ValueError
        self.type = action_type
        if direction not in ['n', 's', 'e', 'w']:
            raise ValueError
        self.direction = direction


class World(object):
    def __init__(self, width, height, seed=None, arrows=1):
        self.seed = seed
        self.rooms = {}
        self.width = width
        self.height = height
        self.is_hero_dead = False
        self.found_gold = False
        self.is_wumpus_dead = False
        self.arrows = arrows

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

    def get_adjacent_rooms(self, center_room):
        rooms = []
        j, i = center_room.posx, center_room.posy
        if (i + 1, j) in self.rooms.keys():
            rooms.append(self.rooms[i + 1, j])
        if (i - 1, j) in self.rooms.keys():
            rooms.append(self.rooms[i - 1, j])
        if (i, j + 1) in self.rooms.keys():
            rooms.append(self.rooms[i, j + 1])
        if (i, j - 1) in self.rooms.keys():
            rooms.append(self.rooms[i, j - 1])
        return rooms

    def generate_rooms(self):
        for i in range(self.height):
            for j in range(self.width):
                self.rooms[i, j] = room.Room(j, i)

    def place_breezes_around(self, i, j):
        adjacent_rooms = self.get_adjacent_rooms(self.rooms[i, j])
        for a_room in adjacent_rooms:
            a_room.add_breeze()

    def place_stenches_around(self, i, j):
        adjacent_rooms = self.get_adjacent_rooms(self.rooms[i, j])
        for a_room in adjacent_rooms:
            a_room.add_stench()

    def remove_stenches_around(self, i, j):
        adjacent_rooms = self.get_adjacent_rooms(self.rooms[i, j])
        for a_room in adjacent_rooms:
            a_room.remove_stench()

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

    def arrow_room(self, i, j):
        if (i, j) not in self.rooms.keys():
            return False
        arrowed_room = self.rooms[i, j]
        if arrowed_room.has_wumpus():
            arrowed_room.kill_wumpus()
            self.remove_stenches_around(i, j)
            self.is_wumpus_dead = True
            return True
        return False

    def fire_arrow(self, arrow_direction):
        if self.arrows == 0:
            return False
        else:
            self.arrows -= 1
        step = 1 if arrow_direction in ['s', 'w'] else -1
        hero_pos = self.find_hero()
        if arrow_direction in ['n', 's']:
            for i in range(hero_pos[0] + step, self.height if step == 1 else -1, step):
                if self.arrow_room(i, hero_pos[1]):
                    return True
        else:
            for j in range(hero_pos[1] + step, self.width if step == 1 else -1, step):
                if self.arrow_room(hero_pos[0], j):
                    return True
        return False

    def get_size(self):
        return self.width, self.height
