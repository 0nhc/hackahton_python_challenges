from maze import RectangularMaze
from RRT_solver import RRTSolver

maze = RectangularMaze()
maze.load_from_image_with_random_start_and_goal("maps/img.png")

rrt_solver = RRTSolver(maze, delta=7)
rrt_solver.find_the_goal()
rrt_solver.find_the_shortest_path()
