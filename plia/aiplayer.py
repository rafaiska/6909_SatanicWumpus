from queue import Queue


class AIPlayer(object):
    def __init__(self, worldsize):
        self.hero_pos = None
        self.worldsize = worldsize
        self.path = Queue()
        self.hero_perception = {}

    def has_pit(self, room):
        adjacencies = self.get_adj(room)
        nadjbreezes = 0
        nadjwalls = 0
        for adj in adjacencies:
            if adj in self.hero_perception.keys():
                if 'b' in self.hero_perception[adj]:
                    nadjbreezes += 1
                else:
                    return 'n'
            else:
                nadjwalls += 1
        if nadjbreezes == 4 or (nadjbreezes >= 2 and nadjwalls >= 1):
            return 'y'
        elif nadjbreezes > 0:
            return 'm'
        else:
            return 'n'

    def has_wumpus(self, room):
        adjacencies = self.get_adj(room)
        nadjstenches = 0
        for adj in adjacencies:
            if adj in self.hero_perception.keys():
                if 's' in self.hero_perception[adj]:
                    nadjstenches += 1
                else:
                    return 'n'
        if nadjstenches >= 2:
            return 'y'
        elif nadjstenches == 1:
            return 'm'
        else:
            return 'n'

    def get_adj(self, room):
        retv = []
        if room[0] + 1 < self.worldsize[0]:
            retv.append((room[0] + 1, room[1]))
        if room[0] - 1 > 0:
            retv.append((room[0] - 1, room[1]))
        if room[1] + 1 < self.worldsize[1]:
            retv.append((room[0], room[1] + 1))
        if room[1] - 1 > 0:
            retv.append((room[0], room[1] - 1))
        return retv

    def get_adj_to_explored(self):
        retv = []
        for room in self.hero_perception.keys():
            adjacencies = self.get_adj(room)
            for adj in adjacencies:
                if adj not in self.hero_perception.keys() and adj not in retv:
                    retv.append(adj)
        return retv

    def discovered(self, room):
        self.hero_pos = (room.posx, room.posy)
        if self.hero_pos not in self.hero_perception.keys():
            self.hero_perception[self.hero_pos] = []
            if room.has_breeze():
                self.hero_perception[self.hero_pos].append('b')
            if room.has_stench():
                self.hero_perception[self.hero_pos].append('s')

    def calculatenextbestroom(self):
        choices = self.get_adj_to_explored()
        minheuristic = 999
        bestchoice = None
        for choice in choices:
            heuristic = 0
            haswumpus = self.has_wumpus(choice)
            if haswumpus == 'y':
                heuristic += 100
            elif haswumpus == 'm':
                heuristic += 5
            else:
                heuristic -= 1
            haspit = self.has_pit(choice)
            if haspit == 'y':
                heuristic += 100
            elif haspit == 'm':
                heuristic += 5
            else:
                heuristic -= 1
            if heuristic < minheuristic:
                bestchoice = choice
                minheuristic = heuristic
        return bestchoice

    def direction(self, room):
        if room[1] == self.hero_pos[1]:
            if room[0] == self.hero_pos[0] + 1:
                return 'w'
            elif room[0] == self.hero_pos[0] - 1:
                return 'e'
        elif room[0] == self.hero_pos[0]:
            if room[1] == self.hero_pos[1] + 1:
                return 's'
            elif room[1] == self.hero_pos[1] - 1:
                return 'n'
        return 'ERROR'

    def buildpath(self, nextroom):
        queue = Queue()
        queue.put(self.hero_pos)
        distances = {}
        parent = {}
        discovered = {}
        for i in range(self.worldsize[0]):
            for j in range(self.worldsize[1]):
                distances[i, j] = 9999
                parent[i, j] = None
                discovered[i, j] = False
        distances[self.hero_pos] = 0
        discovered[self.hero_pos] = True

        while not queue.empty():
            currnode = queue.get_nowait()
            adjacencies = self.get_adj(currnode)
            for adj in adjacencies:
                if (adj in self.hero_perception.keys() or adj == nextroom) and distances[currnode] + 1 < distances[adj]:
                    distances[adj] = distances[currnode] + 1
                    parent[adj] = currnode
                    if not discovered[adj]:
                        discovered[adj] = True
                        queue.put(adj)

        moves = [nextroom]
        nextr = nextroom
        while nextr:
            nextr = parent[nextr]
            if nextr == self.hero_pos:
                break
            moves.append(nextr)

        print('HERO POS:', self.hero_pos)
        # print 'NEXT ROOM:', nextroom
        # print 'DISTANCES:', distances
        # print 'DISCOVERED:', discovered
        # print 'PARENT:', parent
        # print 'MOVES:', moves
        moves.reverse()
        for room in moves:
            self.path.put(room)

    def update(self, room):
        self.discovered(room)

    def nextstep(self):
        if self.path.empty():
            nextroom = self.calculatenextbestroom()
            self.buildpath(nextroom)
        nextroom = self.path.get_nowait()
        nextmove = self.direction(nextroom)
        return nextmove
