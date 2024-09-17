from maze import RectangularMaze
from DFS_solver import DFSSolver

maze = RectangularMaze(20,42)
maze.init_random_maze_map()

bfs_solver = DFSSolver(maze)
bfs_solver.find_the_goal()
bfs_solver.find_the_shortest_path()