""" Recursive Maze Solver

    This program uses recursion to solve a maze passed in at runtime, 
        displaying the steps taken to solve the maze.

    Maze files must follow the following form:

        Each line must have the same character count.
        Each character must be one of four possible characters:
            '=' denotes a wall cell
            '-' denotes a path cell
            's' denotes the start point
            'e' denotes the end point
        Each of 's' and 'e' must appear exactly once.

    Example Maze:

        ===e==
        =-=--=
        =-==-=
        =----=
        ===s==

    Usage:
        ./mazeSolver.py [-h] [-b BLOCK_SIZE] [-s SLEEP_INTERVAL] filename

    Written: March 2024 <john.sweeney@gordon.edu>
"""

from jes4py import *
import sys, time, argparse

START_COLOR     = blue
END_COLOR       = yellow
PATH_COLOR      = white
WALL_COLOR      = black
OCCUPIED_COLOR  = lightGray
FAILURE_COLOR   = red
SOLUTION_COLOR  = green

""" Print error message and exit program

    Args:
        msg (str) : error message to print to stderr
"""
def error(msg):
    print(msg, file=sys.stderr)
    exit(1)



""" A class representing a maze cell

    Attributes:
        _x (int)            : x coordinate of cell within maze
        _y (int)            : y coordinate of cell within maze
        _is_end (bool)      : true if this cell is the end of the maze
        _is_start (bool)    : true if this cell is the start of the maze
        _is_wall (bool)     : true if this cell is a wall of the maze
                                (cell must be a path if this is false)
        _is_occupied (bool) : true if cell is occupied by a function call
                                (this is also defaulted to true for wall cells)

    Methods:
        getX()                      
            Accessor for this cell's x coordinate
        getY()                  
            Accessor for this cell's y coordinate
        isEnd()
            Check whether this cell is the end cell
        isStart()
            Check whether this cell is the start cell
        isWall()
            Check whether this cell is a wall cell
        isOccupied()
            Check whether this cell is occupied
        setOccupied(is_occupied : bool)
            Sets the occupied status of this cell
"""
class Cell:

    """ Constructor

        Args:
            x (int)             : x coordinate of this cell
            y (int)             : y coordinate of this cell
            is_end (bool)       : whether this cell is the end of the maze
                                    (true means cell is end of maze)
            is_start (bool)     : whether this cell is the end of the maze
                                    (true means cell is the start of maze)
            is_wall (bool)      : whether this cell is a wall cell 
                                    (true means cell is wall cell)
    """
    def __init__(self, x: int, y: int, is_end: bool, 
                 is_start: bool, is_wall: bool):
        self._x = x
        self._y = y
        self._is_end = is_end
        self._is_start = is_start
        self._is_wall = is_wall
        # wall blocks are considered occupied
        self._is_occupied = is_wall


    """ Returns the x coordinate of this cell """
    def getX(self) -> int:
        return self._x
    

    """ Returns the y coordinate of this cell """
    def getY(self) -> int:
        return self._y
    

    """ Check whether this cell is the end cell (true -> is end cell) """
    def isEnd(self) -> bool:
        return self._is_end
    

    """ Check whether this cell is the start cell (true -> is start cell) """
    def isStart(self) -> bool:
        return self._is_start
    

    """ Check whether this cell is a wall cell (true -> is wall cell) """
    def isWall(self) -> bool:
        return self._is_wall
    

    """ Check whether this cell is occupied (true -> is occupied) """
    def isOccupied(self) -> bool:
        return self._is_occupied


    """ Sets the occupied status of this cell (true -> is occupied)

        Args:
            is_occupied (bool)  : value to set as the occupied status
    """
    def setOccupied(self, is_occupied: bool):
        self._is_occupied = is_occupied




""" A class representing a maze grid

    Attributes:
        _grid (List)  : 2D list of maze cells (accessed 
                            as follows: _grid[row_num][col_num])
        _startx (int) : x coordinate of start cell
        _starty (int) : y coordinate of start cell
        _width (int)  : width of maze grid
        _height (int) : height of maze grid

    Methods:
        getCell(x: int, y: int)
            Access cell at specified coordinates
        getStartCell()
            Returns the start cell of the maze
        getCellLeft()
            Returns cell to the left of specified coordinates
        getCellRight()
            Returns cell to the right of specified coordinates
        getCellUp()
            Returns cell above specified coordinates
        getCellDown()
            Returns cell below specified coordinates
        getWidth()
            Returns the width of maze grid
        getHeight
            Returns the height of maze grid
"""
class MazeGrid:

    """ Constructor

        Args:
            blueprint (str)     : string representing a map blueprint
            width (int)         : number of cells wide
            height (int)        : number of cells tall
    """
    def __init__(self, blueprint: str):
        self._grid = []
        self._startx = 0    # initialize starting x position
        self._starty = 0    # initialize starting y position

        if (len(blueprint) == 0):
            error("ERR: blueprint must contain both a start and end point")

        rows = blueprint.split('\n')
        self._height = len(rows)
        self._width = len(rows[0])

        # Construct maze grid from blueprint

        count_start = 0
        count_end = 0

        for y in range(self._height):
            self._grid.append([])
            for x in range(self._width):
                
                # Assure consistent row width
                if (len(rows[y]) != self._width):
                    error("ERR: inconsistent row length in blueprint")
                
                c = rows[y][x]
                cell = None
                if c == '='   : cell = Cell(x, y, false, false, true) # wall cell
                elif c == '-' : cell = Cell(x, y, false, false, false) # path cell

                elif c == 's' : # start cell
                    count_start = count_start + 1
                    cell = Cell(x, y, false, true, false)
                    self._startx = x
                    self._starty = y

                elif c == 'e' : # end cell
                    count_end = count_end + 1
                    cell = Cell(x, y, true, false, false)

                else: # invalid character
                    error("ERR: invalid character in blueprint")
                self._grid[y].append(cell)

        if count_start != 1:
            error("ERR: blueprint must contain exactly one start cell")
        if count_end != 1:
            error("ERR: blueprint must contain exactly one end cell")
    

    """ Access cell at specified coordinates

        Args:
            x (int) : x coordinate
            y (int) : y coordinate
    """
    def getCell(self, x: int, y: int) -> Cell:
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return None
        return self._grid[y][x]
    

    """ Returns the start cell of the maze """
    def getStartCell(self) -> Cell:
        return self._grid[self._starty][self._startx]
    

    """ Returns cell to the left of specified coordinates

        Args:
            x (int) : x coordinate of current cell
            y (int) : y coordinate of current cell
    """
    def getCellLeft(self, x: int, y: int) -> Cell:
        return self.getCell(x - 1, y)


    """ Returns cell to the right of specified coordinates

        Args:
            x (int) : x coordinate of current cell
            y (int) : y coordinate of current cell
    """
    def getCellRight(self, x: int, y: int) -> Cell:
        return self.getCell(x + 1, y)
    

    """ Returns cell above specified coordinates

        Args:
            x (int) : x coordinate of current cell
            y (int) : y coordinate of current cell
    """
    def getCellUp(self, x: int, y: int) -> Cell:
        return self.getCell(x, y - 1)
    

    """ Returns cell below specified coordinates

        Args:
            x (int) : x coordinate of current cell
            y (int) : y coordinate of current cell
    """
    def getCellDown(self, x: int, y: int) -> Cell:
        return self.getCell(x, y + 1)


    """ Returns width of maze grid """
    def getWidth(self) -> int:
        return self._width
    

    """ Returns height of maze grid """
    def getHeight(self) -> int:
        return self._height




""" Controller class for the maze solver

    Attributes:
        _maze_grid (MazeGrid)   : cell grid of the stored maze
        _block_size (int)       : size of the cell block (units=pixels)
        _sleep_interval (float) : time interval between each image refresh
        _width (int)            : witdh of maze image
        _height (int)           : height of maze image
        _pic (Picture)          : image to represent the maze

    Methods:
        cellCheck(cell: Cell)
            Checks if cell passed in is the end. If not, performs recursive
            calls on cells to the left, above, and to the right.
        attemptSolve()
            boolean describing whether or not maze has a solution
        __getCellColor(x: int, y: int)
            Private helper method for getting the color of a cell at given 
            coordinates
        __fillCell(x: int, y: int, color: Color)
            Private helper method for filling a cell at given coordinates with a
            specified color.
        __updateCell(x: int, y: int, color: Color)
            Private helper function to update color of cell, 
            pause for a bit, then repaint image
"""
class MazeController(object):

    """ Constructor

        Args:
            blueprint (str)        : string with which to construct the maze
            block_size (int)       : size of the cell block (units=pixels)
            sleep_interval (float) : time interval between each image refresh
    """
    def __init__(self, blueprint: str, block_size: int, \
                  sleep_interval: float):
        self._maze_grid = MazeGrid(blueprint)
        self._block_size = block_size
        self._sleep_interval = sleep_interval
        self._width = self._maze_grid.getWidth() * block_size
        self._height = self._maze_grid.getHeight() * block_size
        self._pic = makeEmptyPicture(self._width, self._height)

        # Draw maze
        for x in range(self._maze_grid.getWidth()):
            for y in range(self._maze_grid.getHeight()):
                cell = self._maze_grid.getCell(x, y)
                if cell.isEnd():
                    self.__fillCell(x, y, END_COLOR)
                elif cell.isStart():
                    self.__fillCell(x, y, START_COLOR)
                elif cell.isWall():
                    self.__fillCell(x, y, WALL_COLOR)
                else:
                    self.__fillCell(x, y, PATH_COLOR)


    """ Checks if cell passed in is the end. If not, performs recursive
            calls on cells to the left, above, and to the right.

        Args:
            cell (Cell) - cell of a maze
        Returns:
            boolean describing whether or not the end has been found. (true if found)
    """
    def cellCheck(self, cell: Cell) -> bool:
        # handle cells that are out of bounds
        if cell == None:
            return false
        
        x = cell.getX()
        y = cell.getY()

        # check for end
        if cell.isEnd():
            self.__updateCell(x, y, SOLUTION_COLOR)
            return true
        # check for occupancy
        if cell.isOccupied():
            prev_color = self.__getCellColor(x, y)
            r = prev_color.getRed() + 50
            g = prev_color.getGreen() - 30
            b = prev_color.getBlue() - 30
            failure_color = makeColor(r, g, b)
            self.__updateCell(x, y, failure_color)
            self.__updateCell(x, y, prev_color)
            return false
        
        # this function call occupies cell
        cell.setOccupied(true)
        if not cell.isStart(): # don't recolor start
            self.__updateCell(x, y, OCCUPIED_COLOR)

        # cell has potential, make necessary recursive calls

        left  = self._maze_grid.getCellLeft(x, y)
        up    = self._maze_grid.getCellUp(x, y)
        right = self._maze_grid.getCellRight(x, y)
        down  = self._maze_grid.getCellDown(x, y)

        if self.cellCheck(left) or self.cellCheck(up) \
                or self.cellCheck(right) or self.cellCheck(down):
            # solution found !!!
            self.__updateCell(x, y, SOLUTION_COLOR)
            return true

        # no solution found, unoccupy cell
        cell.setOccupied(false)
        self.__updateCell(x, y, PATH_COLOR)
        return false
    

    """ Perform an attempt to solve the maze

        Returns:
            boolean describing whether or not maze has a solution
                (true if solved)
    """
    def attemptSolve(self) -> bool:
        show(self._pic)
        startCell = self._maze_grid.getStartCell()
        if self.cellCheck(startCell):
            print("  ~  Maze has been solved :D  ~  ")
            return true
        else:
            print("  ~   Maze has no solution :(  ~  ")
            return false


    """ Private helper method for getting the color of a cell at given 
            coordinates
    
        Args:
            x (int) : x coordinate of cell
            y (int) : y coordinate of cell
    """
    def __getCellColor(self, x: int, y: int) -> Color:
        return getColor(self._pic.getPixel(x * self._block_size,
                                           y * self._block_size))


    """ Private helper method for filling a cell at given coordinates with a
            specified color.

        Args:
            x (int)         : x coordinate of cell
            y (int)         : y coordinate of cell
            color (Color)   : color with which to fill cell
    """
    def __fillCell(self, x: int, y: int, color: Color):
        blockSize = self._block_size
        addRectFilled(self._pic, x * blockSize, y * blockSize, \
                      blockSize - 1, blockSize - 1, color)


    """ Private helper function to update color of cell, 
            pause for a bit, then repaint image

        Args:
            x (int)         : x coordinate of cell
            y (int)         : y coordinate of cell
            color (Color)   : color with which to fill cell
    """
    def __updateCell(self, x: int, y: int, color: Color):
        self.__fillCell(x, y, color)
        time.sleep(self._sleep_interval)
        repaint(self._pic)



# Run program #
if __name__ == "__main__":
    # process command line arguments
    parser = argparse.ArgumentParser(description='Maze Solver')
    parser.add_argument('-b', '--block_size', type=int, default=100)
    parser.add_argument('-s', '--sleep_interval', type=float, default=0.5)
    parser.add_argument('filename', help="txt containing M x N maze. \
                        '=' : wall | '-' : path | 's' : start | 'e' : end")
    args = parser.parse_args()

    # copy argument values to variables
    block_size = args.block_size
    sleep_interval = args.sleep_interval
    filename = args.filename

    # read in blueprint from file
    blueprint = ""
    with open(filename, 'r') as file:
        blueprint = file.read()

    controller = MazeController(blueprint, block_size, sleep_interval)
    controller.attemptSolve()

    input("Press enter to close...")