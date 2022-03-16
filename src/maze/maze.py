import random

import src.utils as utils


class Maze:
    def __init__(self, cfg):
        self.height = cfg.maze['height']
        self.width = cfg.maze['width']
        self.grid = []
        self.start = None
        self.treasure = None
        self.walls = []

    def build_walls(self):
        # Fill the maze of walls
        for i in range(self.height):
            center = []
            for i in range(self.width):
                center.append(['N', 'E', 'S', 'W'])
            self.walls.append(center)

    def nb_cells_walls(self, state):
        return len(self.walls[state[0]][state[1]])

    def remove_wall(self, cell, new_cell):
        # Remove the wall between cell and new_cell
        dy = new_cell[0] - cell[0]
        dx = new_cell[1] - cell[1]
        if [dy, dx] == [-1, 0]:
            a, b = 'N', 'S'
        elif [dy, dx] == [1, 0]:
            a, b = 'S', 'N'
        elif [dy, dx] == [0, -1]:
            a, b = 'W', 'E'
        elif [dy, dx] == [0, 1]:
            a, b = 'E', 'W'

        self.walls[cell[0]][cell[1]].remove(a)
        self.walls[new_cell[0]][new_cell[1]].remove(b)

    def get_neighbour(self, cell):
        candidate = []
        for pos in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            y = pos[0] + cell[0]
            x = pos[1] + cell[1]
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.grid[y][x] == 0:
                    candidate.append([y, x])
        if len(candidate) > 0:
            return random.choice(candidate)
        else:
            None


class MazeBorder(Maze):
    # Deprecated
    def __init__(self, cfg):
        super().__init__(cfg)
        self.build_walls()

    def build_walls(self):
        self.walls = []
        top = []
        top.append(['N', 'W'])
        for i in range(self.width - 2):
            top.append(['N'])
        top.append(['N', 'E'])
        self.walls.append(top)

        for h in range(self.height - 2):
            center = []
            center.append(['W'])
            for i in range(self.width - 2):
                center.append([])
            center.append(['E'])
            self.walls.append(center)

        bottom = []
        bottom.append(['S', 'W'])
        for i in range(self.width - 2):
            bottom.append(['S'])
        bottom.append(['E', 'S'])
        self.walls.append(bottom)


class MazeRandomFuse(Maze):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.build_walls()
        self.construction()

    def construction(self):
        # Construct a grid of the size height x width, and put a unique index
        # between 0 and height * widht - 1 to each element.
        self.grid = []
        for i in range(self.height):
            self.grid.append([i*self.height + j for j in range(self.width)])

        # While all index in grid are not equal to 0:
        while sum([sum(g) for g in self.grid]) > 0:
            cell_b = None
            while cell_b is None:
                cell_a = utils.random_2d(self.height, self.width)
                idx_a = self.grid[cell_a[0]][cell_a[1]]
                cell_b = self.get_neighbour(cell_a, idx_a)
            idx_b = self.grid[cell_b[0]][cell_b[1]]

            if idx_a < idx_b:
                old_idx = idx_b
                new_idx = idx_a
            else:
                old_idx = idx_a
                new_idx = idx_b

            # Two set of cells became 'connected' => they have the same index.
            # The minimum of the index between these two sets are kept.
            for h in range(self.height):
                for w in range(self.width):
                    if self.grid[h][w] == old_idx:
                        self.grid[h][w] = new_idx

            self.remove_wall(cell_a, cell_b)

    def get_neighbour(self, cell, idx):
        candidate = []
        for pos in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            y = pos[0] + cell[0]
            x = pos[1] + cell[1]
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.grid[y][x] != idx:
                    candidate.append([y, x])
        if len(candidate) > 0:
            return random.choice(candidate)
        else:
            None


class MazeExhaustiveSearch(Maze):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.build_walls()
        self.construction()

    def construction(self):
        # Set a grid of size height x width which all cells are set to 0.
        # 0 : not visited
        # 1 : visited
        for i in range(self.height):
            self.grid.append([0 for i in range(self.width)])

        # Choose a random cell
        cell = utils.random_2d(self.height, self.width)

        # Set this cell as visited
        self.grid[cell[0]][cell[1]] = 1

        path = [cell]
        new_cell = None
        # While all cell are not visited.
        while sum([sum(g) for g in self.grid]) != self.width * self.height:
            for p in path[::-1]:
                new_cell = self.get_neighbour(p)
                if new_cell is not None:
                    path.append(new_cell)
                    self.grid[new_cell[0]][new_cell[1]] = 1
                    self.remove_wall(p, new_cell)
                    break
