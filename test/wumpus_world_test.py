from unittest import TestCase

from wumpus_world import World


class TestWorld(TestCase):
    def setUp(self) -> None:
        self.world = World(5, 5, 1, 4)
        self.world.generate_rooms()

    def testArrowN(self):
        self.world.rooms[0, 0].add_wumpus()
        self.world.rooms[3, 0].add_hero()
        self.assertTrue(self.world.fire_arrow('n'))
        self.assertFalse(self.world.fire_arrow('w'))
        self.assertFalse(self.world.fire_arrow('e'))
        self.assertFalse(self.world.fire_arrow('s'))

    def testArrowE(self):
        self.world.rooms[0, 0].add_wumpus()
        self.world.rooms[0, 3].add_hero()
        self.assertTrue(self.world.fire_arrow('e'))
        self.assertFalse(self.world.fire_arrow('w'))
        self.assertFalse(self.world.fire_arrow('n'))
        self.assertFalse(self.world.fire_arrow('s'))

    def testArrowW(self):
        self.world.rooms[0, 3].add_wumpus()
        self.world.rooms[0, 0].add_hero()
        self.assertTrue(self.world.fire_arrow('w'))
        self.assertFalse(self.world.fire_arrow('e'))
        self.assertFalse(self.world.fire_arrow('n'))
        self.assertFalse(self.world.fire_arrow('s'))

    def testArrowS(self):
        self.world.rooms[3, 0].add_wumpus()
        self.world.rooms[0, 0].add_hero()
        self.assertTrue(self.world.fire_arrow('s'))
        self.assertFalse(self.world.fire_arrow('e'))
        self.assertFalse(self.world.fire_arrow('n'))
        self.assertFalse(self.world.fire_arrow('w'))
