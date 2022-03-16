import argparse

from tqdm import tqdm

from src.config_def import Cfg
from src.maze.maze_generator import MazeGenerator
from src.solver.solver_generator import SolverGenerator
from src.utils import save_maze


"""
Q-learning method for solving a maze going through three keypoints:
A starting point, a treasure point and an exit point.

Inputs:
------
A cfg file in toml format with the follwing fields:

[data]
    plot_path  : path where the plot will be saved.
    maze_path  : path where a .csv representing a maze will be saved.
    items_path : path of the .png file representing the three keypoints.
[maze]
    generator  : "random_fuse", "exhaustive_search" for different methods
                    to generate a maze.
    width      : width of the maze.
    height     : height of the maze.
    nb_maze    : number of maze to generate.
[solver]
    nb_epoch   : number of maze to solve.
    nb_step    : length of the path given to solve a maze.
    epsilon    : a parameter of the Epsilon-Greedy Algorithm.
    alpha      : the learning rate.
    gamma      : the discount factor.

Outputs:
-------
A csv file that will describe the maze.
A png file representing the maze.
"""


def main(parse_args, config_args):
    # Construct the config file.
    cfg = Cfg(parse_args)
    # Generate a solver according to the name given in cfg.solver['type']
    solver = SolverGenerator().generate(cfg)
    # maze = MazeGenerator().generate(cfg)

    for m in tqdm(range(cfg.maze['nb_maze'])):
        # Generate a maze according to cfg.maze['generator'],
        # the exit point and the path, towards the exit
        maze = MazeGenerator().generate(cfg)
        solver.train(maze)

        # Create the csv and png files representing the maze.
        save_maze(maze, solver.q_table, cfg.data, m)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate a maze from Q-Learning.')
    parser.add_argument('cfg_path', help='TOML configuration file')
    parsed_args, config_args_in = parser.parse_known_args()

    main(parsed_args, config_args_in)
