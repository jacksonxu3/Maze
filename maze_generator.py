# Uses recursion to generate a square maze of any size

from random import randint

# Terrain Class for maze path and walls
# Many attributes for maze_solver.py
class terrain:
    def __init__(self):
        self.type = 'path'
        self.force_path = False
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.next = None
        self.prev = None
        self.visited = False
        self.lined_up = False

# Maze Template Creator
def maze_template(x_size, y_size):
    # Maze will be a list of lists, 
    # where each list is a row 
    entire_maze = []
    # Number of lists that will be made
    for row_number in range(y_size):
        entire_maze.append([])
        # Number of items in each list
        for column_number in range(x_size):
            terrain_object = terrain_object_helper(entire_maze, row_number, column_number, x_size, y_size)
            entire_maze[row_number].append(terrain_object)
    return entire_maze

# Creates the objects and fills many attributes
def terrain_object_helper(maze, row, column, x_size, y_size):
    terrain_object = terrain()
    if row == 0 or (row == y_size-1) or column == 0 or (column == x_size-1):
        terrain_object.type = 'wall'
    # Setting nearby objects as attributes
    if row != 0:
        terrain_object.up = maze[row-1][column]
        maze[row-1][column].down = terrain_object
    if column != 0:
        terrain_object.left = maze[row][column-1]
        maze[row][column-1].right = terrain_object
    return terrain_object

# Prints out the maze
def maze_printer(maze):
    for row in maze:
        row_representation = []
        for one_column in row:
            if one_column.visited == True:
                row_representation.append('O')
            elif one_column.type == 'path' or one_column.force_path == True:
                row_representation.append('+')
            elif one_column.type == 'wall' and one_column.force_path == False:
                row_representation.append('-')
            elif one_column.type == 'start/end':
                row_representation.append('X')
            elif one_column.type == None:
                row_representation.append('?')
        print("".join(row_representation))

# Global Variable (that will be modified)
new_maze = True
# Creates the start and end of each maze
# Tries to make maze as long as possible
def start_and_end_func(maze, x_size, y_size, direction, hole):
    global new_maze
    if new_maze == True:
        # Start is always top left corner
        top_left_start(maze)
        # Endpoint is in other three corners
        # Bottom right corner is the end if first hole is above midpoint,
        # regardless of first direction
        if (hole+1) <= y_size//2 or (hole+1) <= x_size//2:
            end = bottom_right_end(maze, x_size, y_size)
            # End in top right corner, for first 'vertical'
        elif direction == 'vertical':
            if (hole+1) > y_size//2:
                end = top_right_end(maze, x_size, y_size)
            # End in bottom left corner, for first 'horizontal'
        elif direction == 'horizontal':
            if (hole+1) > x_size//2:
                end = bottom_left_end(maze, x_size, y_size)
        # Ensures only one start and one end
        new_maze = end
    return maze

# Helper functions that mark the start and end of the maze
def top_left_start(maze):
    maze[0][0].type = 'start/end'
    maze[0][1].type = 'start/end'
    maze[1][0].type = 'start/end'
    return None

def bottom_right_end(maze, x_size, y_size):
    maze[y_size-1][x_size-1].type = 'start/end'
    maze[y_size-1][x_size-2].type = 'start/end'
    maze[y_size-2][x_size-1].type = 'start/end'
    return 'bottom_right'

def top_right_end(maze, x_size, y_size):
    maze[0][x_size-1].type = 'start/end'
    maze[0][x_size-2].type = 'start/end'
    maze[1][x_size-1].type = 'start/end'
    return 'top_right'

def bottom_left_end(maze, x_size, y_size):
    maze[y_size-1][0].type = 'start/end'
    maze[y_size-2][0].type = 'start/end'
    maze[y_size-1][1].type = 'start/end'
    return 'bottom_left'

# Recursive function to divide the maze up
def recursive_divider(maze, x_size, y_size):
    # Location of wall and hole in wall
    # Base Case for size < 5
    if x_size < 5 and y_size < 5:
        return None
    # Recursive Case
    wall_location, direction = wall_picker(x_size, y_size)
    maze, hole = wall_maker(maze, x_size, y_size, wall_location, direction)
    maze = start_and_end_func(maze, x_size, y_size, direction, hole)
    # Saves future work if size <= 4
    if x_size <= 5 and y_size <= 5:
        return None
    sub_maze_one = []
    sub_maze_two = []
    # Makes new mazes for recursive case
    if direction == 'vertical':
        for row in range(y_size):
            sub_maze_one.append([])
            for column_one in range(0, wall_location+1):
                land_one = maze[row][column_one]
                sub_maze_one[row].append(land_one)
            sub_maze_two.append([])
            for column_two in range(wall_location, x_size):
                land_two = maze[row][column_two]
                sub_maze_two[row].append(land_two)
        recursive_divider(sub_maze_one, (wall_location+1), y_size)
        recursive_divider(sub_maze_two, (x_size-wall_location), y_size)
    elif direction == 'horizontal':
        for row_one in range(0, wall_location+1):
            sub_maze_one.append([])
            for column_one in range(0, x_size):
                land_one = maze[row_one][column_one]
                sub_maze_one[row_one].append(land_one)
        tracker = -1
        for row_two in range(wall_location, y_size):
            sub_maze_two.append([])
            tracker += 1
            for column_two in range(0, x_size):
                land_two = maze[row_two][column_two]
                sub_maze_two[tracker].append(land_two)
        recursive_divider(sub_maze_one, x_size, (wall_location+1))
        recursive_divider(sub_maze_two, x_size, (y_size-wall_location))

# Picks the location of wall and hole
# Initial maze must be square
def wall_picker(x_size, y_size):
    # Alternating direction of walls
    # and walls only on certain columns to prevent double pathing
    random = 1
    if x_size == y_size:
        direction = direction_picker()
        if direction == 'vertical':
            while random%2 == 1:
                random = randint(2, x_size-3)
            return random, direction
        elif direction == 'horizontal':
            while random%2 == 1:
                random = randint(2, y_size-3)
            return random, direction
    # Alternating wall directions with each recursive case
    elif x_size > y_size:
        direction = 'vertical'
        while random%2 == 1:
            random = randint(2, x_size-3)
        return random, direction
    elif y_size > x_size:
        direction = 'horizontal'
        while random%2 == 1:
            random = randint(2, y_size-3)
        return random, direction

# Picks the direction that a wall will go
# Probably will only be used in first recursive case
def direction_picker():
    direction = randint(1,2)
    if direction == 1:
        direction = 'vertical'
    elif direction == 2:
        direction = 'horizontal'
    return direction

# Picks the location of the hole in a wall
def hole_picker(size):
    return randint(1, size-2)

# Creates a wall with a hole in it in the maze
def wall_maker(maze, x_size, y_size, wall_location, direction):
    # Location of wall and hole in wall
    # Also ensures every maze is possible to solve
    if direction == 'vertical':
        hole = hole_picker(y_size)
        for row in range(y_size):
            maze[row][wall_location].type = 'wall'
        maze[hole][wall_location].force_path = True
        maze[hole][wall_location].right.force_path = True
        maze[hole][wall_location].left.force_path = True
    elif direction == 'horizontal':
        hole = hole_picker(x_size)
        for column in range(x_size):
            maze[wall_location][column].type = 'wall'
        maze[wall_location][hole].force_path = True
        maze[wall_location][hole].up.force_path = True
        maze[wall_location][hole].down.force_path = True
    return maze, hole