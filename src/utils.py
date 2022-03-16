import csv
import os
import random

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

CFG_FIELD = {}
CFG_FIELD["data"] = ["plot_path", "items_path", "maze_path"]
CFG_FIELD["maze"] = ["generator", "height", "width", 'save_path', 'nb_maze']
CFG_FIELD["solver"] = ["type", "nb_epoch", "nb_step", "epsilon", "alpha",
                       "gamma"]

DIR = ['N', 'E', 'S', 'W']

ACTION = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def random_2d(h, w):
    return [random.randint(0, h - 1), random.randint(0, w - 1)]


def plot_maze(maze, q_table, data, idx_maze):
    path = data['plot_path']
    items_path = data['items_path']

    # Plot the maze
    # Start by the four borders
    fig, ax = plt.subplots()

    left = [[0, 0], [0, maze.height]]
    top = [[0, maze.width], [maze.height, maze.height]]
    right = [[maze.width, maze.width], [0, maze.height]]
    bottom = [[0, maze.width], [0, 0]]
    for l in [bottom, top, left, right]:
        _ = plt.plot(l[0], l[1], color='black', linewidth=2.0)
    _ = plt.axis('off')

    # Add vertical border cells:
    for w in range(maze.width):
        start = [w, w]
        end = [0, maze.height]
        _ = plt.plot(start, end, color='gray', alpha=0.3)

    # Add hozizontal border cells:
    for h in range(maze.height):
        start = [0, maze.width]
        end = [h, h]
        _ = plt.plot(start, end, color='gray', alpha=0.3)

    # Add walls
    for h in range(maze.height):
        for w in range(maze.width):
            wall = maze.walls[h][w]
            if len(wall) > 0:
                for wa in wall:
                    if wa == 'S':
                        start = [w, w + 1]
                        end = [maze.height - h - 1, maze.height - h - 1]
                    elif wa == 'N':
                        start = [w, w + 1]
                        end = [maze.height - h, maze.height - h]
                    elif wa == 'E':
                        start = [w + 1, w + 1]
                        end = [maze.height - h - 1, maze.height - h]
                    elif wa == 'W':
                        start = [w, w]
                        end = [maze.height - h - 1, maze.height - h]
                    _ = plt.plot(start, end, color='black', linewidth=2.0)

    # Put the exit in the plot
    plt.text(maze.exit[1] + 0.25, maze.exit[0] + 0.5, 'Exit')

    for h in range(maze.height):
        for w in range(maze.width):
            if [h, w] != maze.exit:
                idx = np.argmax(q_table[h][w])
                if idx == 0:
                    x = w + 0.5
                    y = h + 0.1
                    dx = 0
                    dy = 0.5
                elif idx == 1:
                    x = w + 0.1
                    y = h + 0.5
                    dx = 0.5
                    dy = 0
                elif idx == 2:
                    x = w + 0.5
                    y = h + 0.9
                    dx = 0
                    dy = -0.5
                elif idx == 3:
                    x = w + 0.9
                    y = h + 0.5
                    dx = -0.5
                    dy = 0
                _ = plt.arrow(x, y, dx, dy, width=0.06)

    if not os.path.exists(path):
        os.makedirs(path)

    save_path = os.path.join(path, 'maze_' + str(idx_maze) + '.png')
    plt.savefig(save_path)
    plt.close()


def save_maze(maze, q_table, data, idx_maze):
    plot_maze(maze, q_table, data, idx_maze)

    path = data['maze_path']
    if not os.path.exists(path):
        os.makedirs(path)
    save_path = os.path.join(path, 'maze_' + str(idx_maze) + '.csv')
    description = []
    for h in range(maze.height):
        tmp = []
        for w in range(maze.width):
            if [h, w] == maze.start:
                tmp.append(''.join(maze.walls[maze.start[0]][maze.start[1]])
                           + '-start')
            elif [h, w] == maze.exit:
                tmp.append(''.join(maze.walls[maze.exit[0]][maze.exit[1]]) +
                           '-exit')
            else:
                tmp.append(''.join(maze.walls[h][w]) + '- ')
        description.append(tmp)

    file = open(save_path, 'w', newline='')
    with file:
        csv.writer(file).writerows(description)
