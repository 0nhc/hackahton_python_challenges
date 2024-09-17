from maze import RectangularMaze
from BFS_solver import BFSSolver

maze = RectangularMaze(180,320)
maze.init_random_maze_map()

bfs_solver = BFSSolver(maze)
bfs_solver.find_the_goal()
bfs_solver.find_the_shortest_path()