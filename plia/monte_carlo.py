import random
from collections import defaultdict

import numpy as np

from plia.abs_player import AIPlayerBasic
from room import Room
from wumpus_world import Action, World

EXPLORATION_REWARD = 5
TEMPORAL_DISCOUNT = -10
PIT_FALL_DISCOUNT = -100
WUMPUS_DISCOUNT = -100


class MonteCarloState(object):
    def __init__(self, room: Room):
        if not room.explored:
            self.state = ['u']
        else:
            self.state.extend(room.objects)

    def get_reward(self):
        reward = EXPLORATION_REWARD if 'u' in self.state else 0
        reward += TEMPORAL_DISCOUNT
        reward += PIT_FALL_DISCOUNT if 'p' in self.state else 0
        reward += WUMPUS_DISCOUNT if 'w' in self.state else 0

    def __str__(self):
        return ''.join(sorted(self.state))


class MonteCarloPlayer(AIPlayerBasic):
    def define_possible_action_states(self):
        self.possible_actions_states = []
        current_room = self.world.get_current_room()
        adjacent_rooms = self.world.get_adjacent_rooms(current_room)
        for r in adjacent_rooms:
            r_state = MonteCarloState(r)
            if r.posx == current_room.posx + 1:
                r_action = Action('m', 'w')
            elif r.posx == current_room.posx - 1:
                r_action = Action('m', 'e')
            elif r.posy == current_room.posy + 1:
                r_action = Action('m', 's')
            else:
                r_action = Action('m', 'n')
            self.possible_actions_states.append((r_action, r_state))

    def set_observations(self, world: World) -> None:
        self.world = world
        self.define_possible_action_states()

    def get_action(self) -> Action:
        pass

    def __init__(self):
        self.world = None
        self.pending_exploration_bonus = False
        self.possible_actions_states = None


# Monte Carlo Agent which learns every episodes from the sample
class MCAgent:
    def __init__(self, actions):
        self.width = 5
        self.height = 5
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.samples = []
        self.value_table = defaultdict(float)

    # append sample to memory(state, reward, done)
    def save_sample(self, state, reward, done):
        self.samples.append([state, reward, done])

    # for every episode, agent updates q function of visited states
    def update(self):
        G_t = 0
        visit_state = []
        for reward in reversed(self.samples):
            state = str(reward[0])
            if state not in visit_state:
                visit_state.append(state)
                G_t = self.discount_factor * (reward[1] + G_t)
                value = self.value_table[state]
                self.value_table[state] = (value +
                                           self.learning_rate * (G_t - value))

    # get action for the state according to the q function table
    # agent pick action of epsilon-greedy policy
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # take random action
            action = np.random.choice(self.actions)
        else:
            # take action according to the q function table
            next_state = self.possible_next_state(state)
            action = self.arg_max(next_state)
        return int(action)

    # compute arg_max if multiple candidates exit, pick one randomly
    @staticmethod
    def arg_max(next_state):
        max_index_list = []
        max_value = next_state[0]
        for index, value in enumerate(next_state):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)

    # get the possible next states
    def possible_next_state(self, state):
        col, row = state
        next_state = [0.0] * 4

        if row != 0:
            next_state[0] = self.value_table[str([col, row - 1])]
        else:
            next_state[0] = self.value_table[str(state)]
        if row != self.height - 1:
            next_state[1] = self.value_table[str([col, row + 1])]
        else:
            next_state[1] = self.value_table[str(state)]
        if col != 0:
            next_state[2] = self.value_table[str([col - 1, row])]
        else:
            next_state[2] = self.value_table[str(state)]
        if col != self.width - 1:
            next_state[3] = self.value_table[str([col + 1, row])]
        else:
            next_state[3] = self.value_table[str(state)]

        return next_state


# main loop
if __name__ == "__main__":
    env = Env()
    agent = MCAgent(actions=list(range(env.n_actions)))

    for episode in range(1000):
        state = env.reset()
        action = agent.get_action(state)

        while True:
            env.render()

            # forward to next state. reward is number and done is boolean
            next_state, reward, done = env.step(action)
            agent.save_sample(next_state, reward, done)

            # get next action
            action = agent.get_action(next_state)

            # at the end of each episode, update the q function table
            if done:
                print("episode : ", episode)
                agent.update()
                agent.samples.clear()
                break
