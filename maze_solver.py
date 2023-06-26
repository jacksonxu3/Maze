# Depth First Search and Breadth First Search 
# for solving a maze in the terminal

import maze_generator
from random import sample
from time import sleep

# 'new_maze' is already set to a direction from maze_generator.py
def start_and_end_marker(maze, x_size, y_size):
    start = maze[1][1]
    start.player = True
    if maze_generator.new_maze == 'bottom_right':
        end = maze[y_size-2][x_size-2]
    elif maze_generator.new_maze == 'top_right':
        end = maze[1][x_size-2]
    elif maze_generator.new_maze == 'bottom_left':
        end = maze[y_size-2][1]
    return start, end

def DFS(maze, start, end, StepByStep):
    # Helper function to determine if a node is a dead end

    def dead_end(node):
        # Iterate through every neighbor of the node
        node_list = [node.up, node.down, node.left, node.right]
        for neighbor in node_list:
            # If the neighbor has not been visited, return False
            if ((neighbor != None) and ((neighbor.type == 'path') or (neighbor.force_path)) and (not neighbor.visited)):
                return False
        # If every neighbor has been visited, return True
        return True
    
    # toReturn will be a list that gets edited as we search
    toReturn = []
    # Use a stack to know where to go to next
    stack = [start]
    # Search through the graph by using the stack
    while (len(stack) > 0):
        if StepByStep == True:
            sleep(1/4)
            print('\n')
            maze_generator.maze_printer(maze)
        # Last element of the stack is what will be scanned
        node = stack.pop()
        # If already seen, do not add to path
        if (node.visited == False):
            # Add the new node as a part of the last pathway
            toReturn.append(node)
        # Mark the node as visited
        node.visited = True
        # If t is found, then return
        if (node == end):
            # Setting path to be on_track
            for path_node in toReturn:
                path_node.on_track = True
            maze_generator.maze_printer_final(maze)
            return toReturn
        # If the node is a dead end, remove from path and go back onto the previous node
        if (dead_end(node)):
            deleted = toReturn.pop()
            previous = toReturn[-1]
            stack.append(previous)
        else:
            # Add the unvisited neighbors into the stack
            node_list = [node.up, node.down, node.left, node.right]
            number_list = sample(range(4), 4)
            for near_node in number_list:
                new_node = node_list[near_node]
                # If the node has not been visited, add it to the stack
                if (new_node != None) and ((not new_node.visited)):
                    if new_node.type == 'path' or new_node.force_path == True:
                        stack.append(new_node)

def BFS(maze, start, end, StepByStep):
    # Dictionary key is node and value is who previously called upon it
    dict_of_links = {}
    # Use a queue to know where to go to next
    queue = [start]
    # Search through the graph by using the queue
    while (len(queue) > 0):
        if StepByStep:
            sleep(1/4)
            print('\n')
            maze_generator.maze_printer(maze)
        # First element of the queue is what will be scanned
        node = queue.pop(0)
        # If already seen, skip over
        if (node.visited):
            continue
        # Mark the node as visited
        node.visited = True
        # If t is found, then return
        if (node == end):
            node_number = end
            toReturn = []
            # Place the chain of numbers into an array
            while (node_number != start):
                toReturn.append(node_number)
                node_number = dict_of_links[node_number]
            toReturn.append(start)
            # Do a reversal of the list and return
            toReturn.reverse()
            # Setting path to be on_track
            for path_node in toReturn:
                path_node.on_track = True
            maze_generator.maze_printer_final(maze)
            return toReturn
        # Add the unvisited neighbors into the stack
        node_list = [node.up, node.down, node.left, node.right]
        number_list = sample(range(4), 4)
        for near_node in number_list:
            # If the node has not been visited, add it to the queue, and in the dictionary
            new_node = node_list[near_node]
            if ((new_node != None) and (not new_node.visited) and (new_node not in queue)):
                if new_node.type == 'path' or new_node.force_path == True:
                    queue.append(new_node)
                    dict_of_links[new_node] = node
    return []

def run_game():
# Maze Generation
    size = None
    size = input('Enter the desired maze size. ')
    while type(size) != int:
        try:
            size = int(size)
        except ValueError:
            size = input('Please enter a valid number. ')
    maze = maze_generator.maze_template(size, size)
    maze_generator.recursive_divider(maze, size, size)
    maze_generator.maze_printer(maze)

    # Maze Solving
    start, end = start_and_end_marker(maze, size, size)

    search = None
    print('\nWould you like the solution to use DFS or BFS search?')
    search = input('Please enter < DFS > or < BFS >. \n')
    while search != 'DFS' and search != 'BFS':
        print('\nInvalid input. ')
        search = input('Enter < DFS > or < BFS >. \n')

    print('\nWould you like to see the algorithm\'s process?')
    step = input('Please enter < Yes > or < No >. \n')
    while step != 'Yes' and step != 'No':
        print('\nInvalid input. ')
        step = input('Enter < Yes > or < No >. \n')
    if step == 'Yes':
        StepByStep = True

    if search == 'DFS':
        DFS(maze, start, end, StepByStep)
    elif search == 'BFS':
        BFS(maze, start, end, StepByStep)

# run_game()

# cd documents/CS-Projects/Maze
# python maze_solver.py