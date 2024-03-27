# Recursive Maze Solver

A program to recursively solve a maze passed in at runtime, displaying each
step along the way.

### Usage

You can run the program with the following command:

`python3 ./mazeSolver.py [-h] [-b BLOCK_SIZE] [-s SLEEP_INTERVAL] filename`

### Maze Blueprint Format

Maze blueprints must adhere to the following form:

- Each line must have the same character count.
* Each character must be one of four possible characters:
  1. '=' denotes a wall
  2. '-' denotes a path cell
  3. 's' denotes the start point
  4. 'e' denotes the end point
+ Each of 's' and 'e' must appear exactly once.

### Demo Mazes

A small set of demo mazes are stored in a [Demo Mazes](demo_mazes/) folder.

The design for [Demo Maze 03](demo_mazes/maze03.txt) was taken from [this website](https://www.cs.rochester.edu/~brown/242/assts/mazedoc.html).

**Happy Solving :D**
