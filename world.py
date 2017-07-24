import room
import random

class World(object):
    def __init__(self, width, height):
        self.rooms = {}
        self.width = width
        self.height = height
        self.herodead = False
        self.foundgold = False

    def __str__(self):
        retv = ''
        for i in xrange(self.height):
            for j in xrange(self.width):
                if (i, j) in self.rooms.keys():
                    retv += str(self.rooms[i, j].objects)
                else:
                    retv += 'VAZIO'
                retv += ', '
            retv += '\n'
        return retv

    def findhero(self):
        for pos in self.rooms:
            if self.rooms[pos].hashero():
                return pos
        return None

    def getcurrentroom(self):
        pos = self.findhero()
        return self.rooms[pos]

    def generaterooms(self):
        for i in xrange(self.height):
            for j in xrange(self.width):
                self.rooms[i, j] = room.Room(j, i)

    def populaterooms(self, npits):
        def randomlocation():
            posi = random.choice(range(self.height))
            posj = random.choice(range(self.width))
            return posi, posj

        pitstoplace = npits
        wumpusplaced = False
        goldplaced = False
        heroplaced = False

        # place pits and breezes
        while pitstoplace:
            i, j = randomlocation()
            if not self.rooms[i, j].haspit():
                self.rooms[i, j].addpit()
                pitstoplace -= 1
                if (i + 1, j) in self.rooms.keys():
                    self.rooms[i + 1, j].addbreeze()
                if (i - 1, j) in self.rooms.keys():
                    self.rooms[i - 1, j].addbreeze()
                if (i, j + 1) in self.rooms.keys():
                    self.rooms[i, j + 1].addbreeze()
                if (i, j - 1) in self.rooms.keys():
                    self.rooms[i, j - 1].addbreeze()

        # place wumpus and stenches
        while not wumpusplaced:
            i, j = randomlocation()
            if not self.rooms[i, j].haspit():
                self.rooms[i, j].addwumpus()
                wumpusplaced = True
                if (i + 1, j) in self.rooms.keys():
                    self.rooms[i + 1, j].addstench()
                if (i - 1, j) in self.rooms.keys():
                    self.rooms[i - 1, j].addstench()
                if (i, j + 1) in self.rooms.keys():
                    self.rooms[i, j + 1].addstench()
                if (i, j - 1) in self.rooms.keys():
                    self.rooms[i, j - 1].addstench()

        #place gold
        while not goldplaced:
            i, j = randomlocation()
            if not self.rooms[i, j].haspit() and not self.rooms[i, j].haswumpus():
                self.rooms[i, j].addgold()
                goldplaced = True

        #place player
        while not heroplaced:
            i, j = randomlocation()
            if not self.rooms[i, j].haspit() and not self.rooms[i, j].hasgold() and not self.rooms[i, j].haswumpus():
                self.rooms[i, j].addhero()
                self.rooms[i, j].explore()
                heroplaced = True

    def movehero(self, direction):
        i, j = self.findhero()
        prevroom = self.rooms[i, j]
        if direction == 's':
            i += 1
        elif direction == 'n':
            i -= 1
        elif direction == 'e':
            j -= 1
        elif direction == 'w':
            j += 1
        try:
            room = self.rooms[i, j]
        except KeyError:
            return False
        prevroom.movehero()
        room.explore()
        if room.haswumpus() or room.haspit():
            self.herodead = True
        elif room.hasgold():
            room.addhero()
            self.foundgold = True
        else:
            room.addhero()
        return True

    def randommove(self):
        while not self.movehero(random.choice(['n', 's', 'e', 'w'])):
            pass

    def setup(self, npits):
        self.generaterooms()
        self.populaterooms(npits)

    def revealall(self):
        for i in xrange(self.height):
            for j in xrange(self.width):
                self.rooms[i, j].explore()