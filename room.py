class Room(object):
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.explored = False
        self.objects = []

    def addgold(self):
        if 'g' not in self.objects:
            self.objects.append('g')

    def addwumpus(self):
        if 'w' not in self.objects:
            self.objects.append('w')

    def addpit(self):
        if 'p' not in self.objects:
            self.objects.append('p')

    def addbreeze(self):
        if 'b' not in self.objects:
            self.objects.append('b')

    def addstench(self):
        if 's' not in self.objects:
            self.objects.append('s')

    def addhero(self):
        if 'h' not in self.objects:
            self.objects.append('h')

    def hasgold(self):
        return 'g' in self.objects

    def haswumpus(self):
        return 'w' in self.objects

    def haspit(self):
        return 'p' in self.objects

    def hasbreeze(self):
        return 'b' in self.objects

    def hasstench(self):
        return 's' in self.objects

    def hashero(self):
        return 'h' in self.objects

    def killwumpus(self):
        if 'w' in self.objects:
            self.objects.remove('w')

    def movehero(self):
        self.objects.remove('h')

    def explore(self):
        self.explored = True
