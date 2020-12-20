class Room(object):
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.explored = False
        self.objects = []

    def can_place_entity(self):
        return ('g' not in self.objects and
                'w' not in self.objects and
                'h' not in self.objects and
                'p' not in self.objects)

    def no_hazards_around(self):
        return ('b' not in self.objects and
                's' not in self.objects)

    def add_gold(self):
        if 'g' not in self.objects:
            self.objects.append('g')

    def add_wumpus(self):
        if 'w' not in self.objects:
            self.objects.append('w')

    def add_pit(self):
        if 'p' not in self.objects:
            self.objects.append('p')

    def add_breeze(self):
        if 'b' not in self.objects:
            self.objects.append('b')

    def add_stench(self):
        if 's' not in self.objects:
            self.objects.append('s')

    def remove_stench(self):
        if 's' in self.objects:
            self.objects.remove('s')

    def add_hero(self):
        if 'h' not in self.objects:
            self.objects.append('h')

    def has_gold(self):
        return 'g' in self.objects

    def has_wumpus(self):
        return 'w' in self.objects

    def has_pit(self):
        return 'p' in self.objects

    def has_breeze(self):
        return 'b' in self.objects

    def has_stench(self):
        return 's' in self.objects

    def has_hero(self):
        return 'h' in self.objects

    def kill_wumpus(self):
        if 'w' in self.objects:
            self.objects.remove('w')

    def remove_hero(self):
        self.objects.remove('h')

    def explore(self):
        self.explored = True
