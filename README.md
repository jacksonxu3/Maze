# Maze Game
Generate and solve mazes using the Pygame display.  
Uses a recursive maze generation algorithm and has two maze solving algorithms.  
The two maze solving algorithms are depth first search and breadth first search.  
    Depth first search simply finds a path from the start to the end.  
    Breadth first search takes more steps, but will show the best path.  
Includes a DFS script to allow users to watch a computer solve the maze step-by-step.  
Optimal solution to the maze uses BFS from the current position of the player.  

Only need to run the "maze_game.py" file to generate and solve mazes.  

Game Map Details:  
Green = Player  
Orange = Start & End  
Yellow = Endpoint  
Black = Path  
Grey = Wall  

Game Keybinds:  
wasd / arrows = Movement  
b = Watch a bot play (Uses Depth First Search)  
n = Show optimal solution (Uses Breadth First Search)  
m = Quit  
