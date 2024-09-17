from data_structure import TreeNode
from maze import RectangularMaze
from tree import Tree
from state_define import *
from maze_visualizer import MazeVisualizer

import numpy as np
import random

class RRTSolver:
    def __init__(self, maze=RectangularMaze(), delta=5) -> None:
        self.maze = maze
        init_tree_node = TreeNode(position=self.maze.nodes[self.maze.start_node_index].position, 
                                  index=0, 
                                  parent=-1, 
                                  state=START)
        self.visited_tree = Tree(init_tree_node)
        self.visualizer = MazeVisualizer()
        
        self.delta = delta
            

    def find_the_goal(self):
        while(True):
            # Check if any node meets the goal point
            meet_the_goal = False
            meet_the_goal_node_index = 0
            for index, node in enumerate(self.visited_tree.nodes):
                if(self._calc_distance_2d(node.position, self.maze.nodes[self.maze.goal_node_index].position)
                    < self.delta):
                    meet_the_goal = True
                    meet_the_goal_node_index = node.index
                    break
            if(meet_the_goal == True):
                end_node = TreeNode(position=self.maze.nodes[self.maze.goal_node_index].position,
                                    parent=meet_the_goal_node_index,
                                    state=GOAL)
                self.visited_tree.add_node(end_node)
                self.visualizer.draw_single_state_with_tree(self.maze.as_matrix(), self.visited_tree, interval=3.0)
                break
            
            # Generate a random position (whihin th eboundary) that satisfy the distance
            # from the nearest point to the random point equals self.delta
            x = random.random()*self.maze.num_rows - 1
            y = random.random()*self.maze.num_columns - 1
            new_position = [x, y]
            
            # Calc the nearest point in current tree
            nearest_node_index = 0
            minimum_distance = np.inf
            for index, node in enumerate(self.visited_tree.nodes):
                position = node.position
                distance = self._calc_distance_2d(position, new_position)
                if(distance < minimum_distance):
                    nearest_node_index = node.index
                    minimum_distance = distance
            nearest_node_position = self.visited_tree.nodes[nearest_node_index].position
            
            # Reset new position in the same direction but specified distance
            new_x = float(nearest_node_position[0] + self.delta*((x-nearest_node_position[0])/minimum_distance))
            new_y = float(nearest_node_position[1] + self.delta*((y-nearest_node_position[1])/minimum_distance))
            new_position = [new_x, new_y]

            # Use linear representation y=k*x+b for the new line
            if(new_position[0] - nearest_node_position[0] != 0):
                k = (new_position[1] - nearest_node_position[1])/(new_position[0] - nearest_node_position[0])
                b = new_position[1] - k * new_position[0]
                # Calc every wall node's distance to this linear representation
                # in order to check if there's collision between the new path
                # and wall nodes
                has_collision = False
                d_threshold = np.sqrt(2*self.delta**2)
                for i in range(self.maze.num_nodes):
                    if(self.maze.nodes[i].state == WALL):
                        position = self.maze.nodes[i].position
                        # Check WALL points within the bounding box
                        if (self._is_point_within_the_bounding_box(position, nearest_node_position, new_position)):
                            # Only consider points inside bounding box between nearest point and the new point
                            d = np.abs(-k*position[0] + position[1] - b)/np.sqrt(k**2+1)
                            if(d < d_threshold):
                                has_collision = True
                                break
                        # Check distances between WALL points and the new two points
                        if(self._calc_distance_2d(position, nearest_node_position)<1
                           or
                           self._calc_distance_2d(position, new_position)<1):
                            has_collision = True
                            break
                if(has_collision == True):
                    # The generated random point has collisions with walls
                    # , thus continue to the next random point
                    continue
                else:
                    # No collision with walls
                    new_node = TreeNode(position=new_position,
                                        parent=nearest_node_index,
                                        state=VISITING)
                    self.visited_tree.add_node(new_node)
                    self.visualizer.draw_single_state_with_tree(self.maze.as_matrix(), self.visited_tree, interval=0.01)
            else:
                pass
                # I don't know, but we can do nothing
            
            
    
    def find_the_shortest_path(self):
        path_node_indices = []
        current_index = len(self.visited_tree.nodes)-1
        while(current_index != 0):
            path_node_indices.append(current_index)
            current_index = self.visited_tree.nodes[current_index].parent
            
        self.visualizer.draw_final_path_for_rrt(self.maze.as_matrix(), path_node_indices, self.visited_tree)
        
    
    def _calc_distance_2d(self, a, b):
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    def _is_point_within_the_bounding_box(self, p, b1, b2):
        px=p[0]
        py=p[1]
        b1x=b1[0]
        b1y=b1[1]
        b2x=b2[0]
        b2y=b2[1]
        
        # Because the WALL node position is int format,
        # but the tree nodes' positions are float format,
        # we have to make sure the space between two points 
        # is larger than 1 (the unit of one node in a 2D matrix)
        if(abs(b1x-b2x) < 1.1):
            if(b1x<b2x):
                b1x-=1
                b2x+=1
            elif(b1x>b2x):
                b1x+=1
                b2x-=1
            else:
                b1x-=1
                b2x+=1
                
        if(abs(b1y-b2y) < 1.1):
            if(b1y<b2y):
                b1y-=1
                b2y+=1
            elif(b1y>b2y):
                b1y+=1
                b2y-=1
            else:
                b1y-=1
                b2y+=1
            
        # Detect whether p is in the bounding box of b1 and b2
        result = (np.abs(px-b1x)+np.abs(px-b2x) == np.abs(b1x-b2x)
                  and
                  np.abs(py-b1y)+np.abs(py-b2y) == np.abs(b1y-b2y))
        return result