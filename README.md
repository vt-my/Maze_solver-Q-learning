# Maze generator

The aim of this project is to generate a maze using [Q-Learning](https://en.wikipedia.org/wiki/Q-learning) methods.


## _Requirements_
Works with Python 3.7.5 and requires:
- matplotlib
- python
- toml
- tqdm

## _Usage_
First, you need a config file in the ```toml``` format. You can find some examples in the folder cfg.
Run ```python  main.py path_to_cfg.toml```, so that it generates a plot and a csv file (by default, respectively in ./plot and ./maze) for each maze defined in the field ````[maze] nb_maze```` of the config file.

## _Description of a maze_
A maze of size HxW is represented by a nested list ```maze.walls``` and the cell ```c``` at position (h, w) is stored in ```c = maze.walls[h][w]```.
The cell ```c``` is a list of length equal to the number of walls surronding it. ```len(c) = 0``` means that if there is no walls directly around ```c```, and ```len(c) = 4``` means ```c``` is totally isolated from the other cells of the maze.

```c``` can have its values in ```['N', 'E', 'S', 'W']``` (respectively for North, East, South, and West) representing the relative position of a wall.  Consider the following trivial maze of size 4x4:
```text
*-------*-------*-------*-------*
| (0,0)                         |
|                               |
|         (2,1)         |       |
|                       | (3,3) |
*-------*-------*-------*-------*
```

For cell (0,0), there is a wall in North and West position, then ```maze.walls[0][0]=['N', 'W']```. There are no walls for cell (2,1), then ```maze.walls[2][1]=[]```. Cell (3,3) is surronded by three walls, then ```maze.walls[3][3]=['E', 'S', 'W']```.
According to the description above, this maze would be represented by:
```python
maze.walls = [[['N', 'W'], ['N'], ['N'], ['N', 'E']],
               [['W'], [], [], ['E']],
               [['W'], [], ['E'], ['E', 'W']],
               [['S', 'E'], ['S'], ['E', 'S'], ['E', 'S', 'W']]
             ]
```

## _Output_

As output, a csv file and a .png file will be generated.
#### _CSV_
For the csv file, each cell is a string separted by a '-'. The left part signifies the direction of the wall, with N for North, E fort East, S for South and W for West. The right part is a string representing what is inside the cell: a space if the cell is empty, otherwise the name of the keypoint.

## _Config File_

* [data]
    * plot_path : path where the plot will be saved.
    * maze_path : path where a .csv representing a maze will be saved.
* [maze]
    * generator : "random_fuse", "exhaustive_search" for different methods to generate a maze.
    * width : width of the maze.
    * height : height of the maze.
    * nb_maze : number of maze to generate.
* [solver]
    * nb_epoch : number of maze to solve.
    * nb_step : length of the path given to solve a maze.
    * epsilon : a parameter of the Epsilon-Greedy Algorithm.
    * alpha : learning rate.
    * gamma :  discount factor.

## _File Description_
* main.py : Generate the solver, the maze, run the training, and create the plot and .csv file.
* cfg/ : examples of config file.
* png/ : Png images representing the start and exit that will be put in the final plot.
* src/ : 
     * maze/maze.py : Contain Maze classes that generates a maze.
     * solver/solver.py : Contain Solver classes that learn a policy function from a maze.
     * utils.py : Contains some utils functions.
