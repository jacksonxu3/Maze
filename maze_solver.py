# Depth First Search and Breadth First Search 
# for solving a maze in the terminal

import maze_generator as mg
from random import sample

# Setting the start and end point
# Start and End global variables
Start = None
End = None

# 'new_maze' is already set to a direction from maze_generator.py
def start_and_end_marker(maze, x_size, y_size):
    global Start
    global End
    Start = maze[1][1]
    if mg.new_maze == 'bottom_right':
        End = maze[y_size-2][x_size-2]
    elif mg.new_maze == 'top_right':
        End = maze[1][x_size-2]
    elif mg.new_maze == 'bottom_left':
        End = maze[y_size-2][1]

# Depth First Search
# Uses the Stack data structure (append, pop)
# Last In, First out
# Only finds a path, no guarantees about best
def DFS(maze, start, end):
    node = None
    stack = DLList()
    stack.append(start)
    start.lined_up = True
    while node != end:
        node = stack.pop()
        node.visited = True
        node_list = [node.up, node.down, node.left, node.right]
        number_list = sample(range(4), 4)
        for number in number_list:
            node_object = node_list[number]
            if node_object.type == 'path' or node_object.force_path == True:
                if node_object.lined_up == False:
                    stack.append(node_object)
                    node_object.lined_up = True
        _ = input('Enter anything to see the next step.')
        print('\n')
        mg.maze_printer(maze)
        stack.printer()
    if node == end:
        return

# Breadth First Search
# Uses Queue data structure (enqueue, dequeue)
# First in, First out
# Finds many paths, with shortest one included
def BFS(maze, start, end):
    node = None
    queue = DLList()
    queue.enqueue(start)
    start.lined_up = True
    while node != end:
        node = queue.dequeue()
        node.visited = True
        node_list = [node.up, node.down, node.left, node.right]
        number_list = sample(range(4), 4)
        for number in number_list:
            node_object = node_list[number]
            if node_object.type == 'path' or node_object.force_path == True:
                if node_object.lined_up == False:
                    queue.enqueue(node_object)
                    node_object.lined_up = True
        _ = input('Enter anything to see the next step.')
        print('\n')
        mg.maze_printer(maze)
        queue.printer()
    if node == end:
        return

# Doubly Linked Lists will be composed of Node objects
# that each have references to 2 connected Nodes 

# Sentinel Node Class for the edges of the Doubly Linked List
class Sentinel_Node:
    def __init__(self, terrain):
        self.terrain = terrain
        self.next = None
        self.prev = None

# Doubly Linked List Class
class DLList:
    def __init__(self):
        self.top = Sentinel_Node('top_sentinel')
        self.bot = Sentinel_Node('bot_sentinel')
        self.top.next = self.bot
        self.bot.prev = self.top
    
    # Check if the DLList is empty or not
    def is_empty(self):
        if self.top.next == self.bot and self.bot.prev == self.top:
            return True
        else:
            return False
    
    # Prints number of objects in line
    def printer(self):
        tracker = 0
        node = self.top.next
        while node != self.bot:
            tracker += 1
            node = node.next
        print(f'Paths in line: {tracker}')

    # Adds to bottom of stack
    def append(self, node):
        self.bot.prev.next = node
        node.prev = self.bot.prev
        self.bot.prev = node
        node.next = self.bot
        return
    
    # Removes from bottom of stack
    def pop(self):
        if self.is_empty() == True:
            print('Stack is empty')
            return
        else:
            node = self.bot.prev
            self.bot.prev = node.prev
            node.prev.next = self.bot
            node.next = None
            node.prev = None
            return node
    
    # Adds to top of queue
    def enqueue(self, node):
        self.top.next.prev = node
        node.next = self.top.next
        self.top.next = node
        node.prev = self.top
        return

    # Removes from bottom of queue
    def dequeue(self):
        if self.is_empty() == True:
            print('Queue is empty.')
            return
        else:
            node = self.bot.prev
            self.bot.prev = node.prev
            node.prev.next = self.bot
            node.next = None
            node.prev = None
            return node

# Maze Generation
size = None
size = input('Enter the desired maze size. ')
while type(size) != int:
    try:
        size = int(size)
    except ValueError:
        size = input('Please enter a valid number. ')
maze = mg.maze_template(size, size)
mg.recursive_divider(maze, size, size)
mg.maze_printer(maze)

# Maze Solving
start_and_end_marker(maze, size, size)
search = None
print('Would you like DFS or BFS search? ')
search = input('Please enter DFS or BFS. ')
while search != 'DFS' and search != 'BFS':
    print('Invalid input. ')
    search = input('Enter DFS or BFS. ')
if search == 'DFS':
    DFS(maze, Start, End)
elif search == 'BFS':
    BFS(maze, Start, End)
print('\nCompleted.')

# cd documents/CS Projects/Maze
# python maze_solver.py