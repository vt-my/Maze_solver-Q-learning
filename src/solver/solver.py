import random

import numpy as np
from tqdm import tqdm

import src.utils as utils


class Solver:
    """A Q-learning solver.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.height = cfg.maze['height']
        self.width = cfg.maze['width']
        self.alpha = self.cfg.solver['alpha']
        self.gamma = self.cfg.solver['gamma']
        self.epsilon = self.cfg.solver['epsilon']
        self.nb_epoch = self.cfg.solver['nb_epoch']
        self.nb_step = self.cfg.solver['nb_step']
        self.start = None
        self.treasure = None
        self.exit = None
        self.keypoint = None
        self.initialisation()

    def set_keypoint(self):
        keypoint = utils.random_2d(self.height, self.width)
        while self.nb_cells_walls(keypoint) == 4:
            keypoint = utils.random_2d(self.height, self.width)
        return keypoint

    def initialisation(self):
        # Set all state at -1.5 in the policy function.
        self.q_table = []
        for i in range(self.height):
            tmp = []
            for j in range(self.width):
                # Four columns for North, East, South and West direction
                tmp.append([-1.5 for k in range(4)])
            self.q_table.append(tmp)

    def quality(self, action, state):
        # Return the value of the policy function at a given state
        # and direction.
        return self.q_table[state[0]][state[1]][utils.DIR.index(action)]

    def get_reward(self, state, action):
        new_state = self.get_new_state(state, action)

        if len(self.maze.walls[state[0]][state[1]]) == 3:  # if entering in
            return -1                                      # a dead end.
        elif new_state == self.keypoint:  # if reaching the keypoint
            return 2
        elif new_state in self.visited:  # if go back to an already
            return -2                    # visited cell.
        else:
            return 1  # Going to a new cell.

    def update_q_table(self, old_state, state, action):
        idx_action = utils.DIR.index(action)
        reward = self.get_reward(state, action)
        _, max_q = self.get_max_quality(old_state)

        self.q_table[old_state[0]][old_state[1]][idx_action] += self.alpha * (
            reward + self.gamma * max_q -
            self.q_table[old_state[0]][old_state[1]][idx_action])

    # Get the new state after a given action.
    def get_new_state(self, state, action):
        return [state[0] + utils.ACTION[action][0],
                state[1] + utils.ACTION[action][1]]

    def get_start(self, dist=0):
        self.start = self.keypoint
        while (utils.manhattan_distance(self.keypoint, self.start) <= dist
               or self.maze.nb_cells_walls(self.start) == 4
               or self.start in self.forbidden_points):

            self.start = utils.random_2d(self.height, self.width)

    def train_solver(self, maze, points=[]):
        self.maze = maze
        self.forbidden_points = points
        # Set the keypoint at 0.
        self.q_table[self.keypoint[0]][self.keypoint[1]] = [0, 0, 0, 0]

        # Train on nb_epoch.
        for i in tqdm(range(self.nb_epoch)):
            self.epoch = i
            self.visited = []
            self.get_start()
            state = self.start

            for j in range(self.nb_step):
                self.visited.append(state)
                action = self.eps_greedy_action_selection(state)

                old_state = state.copy()
                state = self.get_new_state(state, action)

                self.update_q_table(old_state, state, action)

                if state == self.keypoint:
                    break

    def eps_greedy_action_selection(self, state):
        """ Epsilon greedy algorithm.
            Provides a new state from the current one.
            With a probabily that decreases with time, either a random
            direction is chosen, either the new direction is chosen from
            the quality function.
        """

        eps = np.random.uniform(0, 1)
        if eps < self.epsilon ** self.epoch:
            return random.choice(
                [a for a in utils.DIR if a not in
                    self.maze.walls[state[0]][state[1]]])
        else:
            new_direction, _ = self.get_max_quality(state)
            return new_direction

    def get_max_quality(self, state):
        directions = {}
        for a in utils.DIR:
            if a not in self.maze.walls[state[0]][state[1]]:
                directions[a] = self.quality(a, state)

        max_quality = max(directions.values())
        # The comparison >= may be usefull for floating point comparison
        candidates = [k for k, v in directions.items() if v >= max_quality]
        return np.random.choice(candidates), max_quality

    def get_new_action(self, maze, state, q_table):
        directions = {}
        for d, q in zip(utils.DIR, q_table[state[0]][state[1]]):
            if d not in maze.walls[state[0]][state[1]]:
                # if q != 0:
                directions[d] = q

        max_prob = max(directions.values())
        # The comparison >= may be usefull for floating point comparison
        candidates = [k for k, v in directions.items() if v >= max_prob]
        return np.random.choice(candidates)

    def get_random_point(self, maze, points=[]):
        keypoint = utils.random_2d(self.height, self.width)
        # Force the new point to do not be isolated or in the points given in
        # input.
        while maze.nb_cells_walls(keypoint) == 4 or keypoint in points:
            keypoint = utils.random_2d(self.height, self.width)
        return keypoint

class SolverOneStep(Solver):
    def __init__(self, cfg):
        super().__init__(cfg)

    def train(self, maze):
        self.exit = self.get_random_point(maze)
        self.keypoint = self.exit
        self.train_solver(maze)
        maze.exit = self.exit
