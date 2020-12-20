from abc import ABC

from wumpus_world import World, Action


class AIPlayerBasic(ABC):
    def set_observations(self, world: World) -> None:
        raise NotImplementedError

    def get_action(self) -> Action:
        raise NotImplementedError
