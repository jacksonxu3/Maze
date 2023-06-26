import pygame
import maze_generator
import maze_solver
import maze_generator
from random import sample
from time import sleep

Map_Size = 0
Tile_Size = 20
Number_Of_Tiles = Map_Size // Tile_Size

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)

# Display the main menu, and take return a number for the map size
def main_menu():
    global Map_Size
    global Tile_Size
    global Number_Of_Tiles
    menu_size = 350
    half = menu_size // 2
    quarter = half // 2
    eighth = quarter // 2
    screen = pygame.display.set_mode((menu_size, menu_size))
    pygame.display.set_caption('Main Menu')
    font = pygame.font.Font('freesansbold.ttf', 20)

    menu_text1 = font.render('Keybinds will be shown above.', True, WHITE)
    menu_text2 = font.render('Enter in the size of the maze.', True, WHITE)
    menu_text3 = font.render('Press < ENTER > to generate maze.', True, WHITE)
    menu_text4 = font.render('Press < m > to quit.', True, WHITE)

    menutextRect1 = menu_text1.get_rect()
    menutextRect2 = menu_text2.get_rect()
    menutextRect3 = menu_text3.get_rect()
    menutextRect4 = menu_text4.get_rect()

    menutextRect1.center = (half, quarter - eighth)
    menutextRect2.center = (half, quarter)
    menutextRect3.center = (half, quarter + eighth)
    menutextRect4.center = (half, half)

    screen.blit(menu_text1, menutextRect1)
    screen.blit(menu_text2, menutextRect2)
    screen.blit(menu_text3, menutextRect3)
    screen.blit(menu_text4, menutextRect4)

    pygame.display.update()
    
    set = (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9)
    looping = True
    size = ""
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                input_key = event.key
                # Quit
                if (input_key == pygame.K_m):
                    pygame.quit()
                    exit()
                # Start
                elif (input_key == pygame.K_RETURN):
                    if (size == ""):
                        size = "0"
                    Map_Size = int(size) * Tile_Size
                    if (Map_Size < 5):
                        Map_Size = 5 * Tile_Size
                    Number_Of_Tiles = Map_Size // Tile_Size
                    looping = False
                # Backspace
                elif (input_key == pygame.K_BACKSPACE):
                    size = size[:-1]
                # Add numbers
                elif (input_key in set):
                    size += (pygame.key.name(input_key))
                
                screen.fill(pygame.Color("black"))
                screen.blit(menu_text1, menutextRect1)
                screen.blit(menu_text2, menutextRect2)
                screen.blit(menu_text3, menutextRect3)
                screen.blit(menu_text4, menutextRect4)
                text = font.render(size, True, WHITE)
                textRect = text.get_rect()
                textRect.center = (half, half + eighth)
                screen.blit(text, textRect)
                pygame.display.update()

def maze_search_reset(maze):
    for row in maze:
        for col in row:
            col.visited = False
            col.on_track = False

def display_generator(screen, maze, player_tile, End, show_solution):
    for (row, row_coord) in zip(maze, (range(0, Map_Size, Tile_Size))):
        for (col, col_coord) in zip(row, (range(0, Map_Size, Tile_Size))):
            square = pygame.Rect(row_coord, col_coord, Tile_Size, Tile_Size)
            if (col == player_tile):
                pygame.draw.rect(screen, GREEN, square)
            elif (col == End):
                pygame.draw.rect(screen, YELLOW, square)
            elif (col.type == "start/end"):
                pygame.draw.rect(screen, ORANGE, square)
            elif (show_solution and col.on_track):
                pygame.draw.rect(screen, WHITE, square)
            elif ((col.type == "path") or (col.force_path)):
                pygame.draw.rect(screen, BLACK, square)
            elif ((col.type == "wall") and (col.force_path == False)):
                pygame.draw.rect(screen, GRAY, square)
    pygame.display.update()

def movement(maze, input_key, player_tile, end, show_solution):
    next_tile = None
    if (input_key == pygame.K_m):
        pygame.quit()
        exit()
    # Show the solution instantly
    elif (input_key == pygame.K_n):
        maze_search_reset(maze)
        opt_solution(maze, player_tile, end)
        show_solution = not show_solution
        return player_tile, show_solution
    # Show a bot running the maze (in other part of code)
    elif (input_key == pygame.K_b):
        pass

    # Movement commands
    elif ((input_key == pygame.K_UP) or (input_key == pygame.K_w)):
        next_tile = player_tile.left
    elif ((input_key == pygame.K_DOWN) or (input_key == pygame.K_s)):
        next_tile = player_tile.right
    elif ((input_key == pygame.K_LEFT) or (input_key == pygame.K_a)):
        next_tile = player_tile.up
    elif ((input_key == pygame.K_RIGHT) or (input_key == pygame.K_d)):
        next_tile = player_tile.down
    # if next_tile is none, an invalid key was pressed
    if next_tile == None: 
        return player_tile, show_solution
    # Set the next tile to be current tile
    if ((next_tile.type == "path") or (next_tile.force_path)):
        return next_tile, show_solution
    else:
        return player_tile, show_solution

def opt_solution(maze, start, end):
    maze_search_reset(maze)
    dict_of_links = {}
    queue = [start]
    while (len(queue) > 0):
        node = queue.pop(0)
        if (node.visited):
            continue
        node.visited = True
        if (node == end):
            nodes_to_add = end
            path = set()
            while (nodes_to_add != start):
                path.add(nodes_to_add)
                nodes_to_add = dict_of_links[nodes_to_add]
            path.add(start)
            for item in path:
                item.on_track = True
            return True
        node_list = [node.up, node.down, node.left, node.right]
        number_list = sample(range(4), 4)
        for near_node in number_list:
            new_node = node_list[near_node]
            if ((new_node != None) and (not new_node.visited) and (new_node not in queue)):
                if new_node.type == 'path' or new_node.force_path == True:
                    queue.append(new_node)
                    dict_of_links[new_node] = node
    return False

def bot_solution(maze, start, end, screen):
    maze_search_reset(maze)

    def dead_end(node):
        node_list = [node.up, node.down, node.left, node.right]
        for neighbor in node_list:
            if ((neighbor != None) and ((neighbor.type == 'path') or (neighbor.force_path)) and (not neighbor.visited)):
                return False
        return True

    toReturn = []
    stack = [start]
    while (len(stack) > 0):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                input_key = event.key
                if (input_key == pygame.K_b):
                    maze_search_reset(maze)
                    display_generator(screen, maze, start, end, False)
                    return False

        node = stack.pop()

        sleep(1/10)
        display_generator(screen, maze, node, end, True)

        if (node.visited == False):
            toReturn.append(node)
            node.on_track = True
        node.visited = True
        if (node == end):
            return True
        if (dead_end(node)):
            node.on_track = False
            deleted = toReturn.pop()
            previous = toReturn[-1]
            stack.append(previous)
        else:
            node_list = [node.up, node.down, node.left, node.right]
            number_list = sample(range(4), 4)
            for near_node in number_list:
                new_node = node_list[near_node]
                # If the node has not been visited, add it to the stack
                if (new_node != None) and ((not new_node.visited)):
                    if new_node.type == 'path' or new_node.force_path == True:
                        stack.append(new_node)
    return False

def game_running():
    global Map_Size
    global Tile_Size
    global Number_Of_Tiles

    # Initialize the screen
    pygame.init()
    main_menu()
    screen = pygame.display.set_mode((Map_Size, Map_Size))
    pygame.display.set_caption('Buttons: {wasd & arrows} = Movement; b = Bot; n = Solution; m = Quit;')
    # Make the maze
    maze = maze_generator.maze_template(Number_Of_Tiles, Number_Of_Tiles)
    maze_generator.recursive_divider(maze, Number_Of_Tiles, Number_Of_Tiles)
    start, end = maze_solver.start_and_end_marker(maze, Number_Of_Tiles, Number_Of_Tiles)
    player_tile = start
    show_solution = False
    # Add maze to the screen
    display_generator(screen, maze, player_tile, end, show_solution)
    pygame.display.flip()

    # Run the game until it ends
    while player_tile != end:
        # Take in any input
        for event in pygame.event.get():
            # Only take in keys
            if event.type == pygame.KEYDOWN:
                # Use movement keys
                input_key = event.key
                if (input_key == pygame.K_b):
                    show_solution = bot_solution(maze, player_tile, end, screen)
                    display_generator(screen, maze, player_tile, end, show_solution)
                else:
                    player_tile, show_solution = movement(maze, input_key, player_tile, end, show_solution)
                    display_generator(screen, maze, player_tile, end, show_solution)
    pygame.quit()
    exit()

game_running()

# cd documents/CS-Projects/Maze
# python maze_game.py