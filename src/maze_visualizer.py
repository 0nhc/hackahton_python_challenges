import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from tree import Tree

class MazeVisualizer:
    def __init__(self):
        # Define a discrete colormap
        self._colors = ['purple', 'black', 'white', 'blue', 'red', 'orange', 'green', 'yellow']
        self._cmap = mcolors.ListedColormap(self._colors)
        self._bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.6, 7.5]  # Define boundaries for each color
        self._norm = mcolors.BoundaryNorm(self._bounds, self._cmap.N)
        
        # Set matplotlib to full screen by default
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        
        # Record every scatter point
        self.scatter_points = []

            
    def display_single_state(self, maze, interval=1.0):
        plt.imshow(maze, cmap=self._cmap, norm=self._norm, interpolation='nearest')
        plt.pause(interval) # seconds
        plt.clf()
        
    
    def draw_single_state_with_tree(self, maze, tree=Tree(), interval=1.0):
        # Plot the maze
        plt.imshow(maze, cmap=self._cmap, norm=self._norm, interpolation='nearest')
        
        # Plot the tree points
        for index, node in enumerate(tree.nodes):
            if(index != 0 and index != (len(tree.nodes)-1)):
                plt.scatter(node.position[1], node.position[0], c="pink")
                
        # Plot the tree lines
        for index, node in enumerate(tree.nodes):
            if(index==0):
                # skip the start node because it has no parent node
                continue
            else:
                current_position = node.position
                parent_index = node.parent
                parent_position = tree.nodes[parent_index].position
                self._draw_line_between_two_points(current_position, parent_position)
        
        plt.pause(interval) # seconds
        plt.clf()
        plt.cla()
        
    
    def draw_final_path_for_rrt(self, maze, path_indices, tree=Tree(), interval=3.0):
        # Plot the maze
        plt.imshow(maze, cmap=self._cmap, norm=self._norm, interpolation='nearest')
        
        # Plot the tree points
        for index, node in enumerate(tree.nodes):
            if(index != 0 and index != (len(tree.nodes)-1)):
                plt.scatter(node.position[1], node.position[0], c="pink")
                
        # Plot the tree lines
        for index, node in enumerate(tree.nodes):
            if(index in path_indices):
                current_position = node.position
                parent_index = node.parent
                parent_position = tree.nodes[parent_index].position
                self._draw_line_between_two_points(current_position, parent_position, color_line="yellow")
            else:
                if(index==0):
                    # skip the start node because it has no parent node
                    continue
                else:
                    current_position = node.position
                    parent_index = node.parent
                    parent_position = tree.nodes[parent_index].position
                    self._draw_line_between_two_points(current_position, parent_position)
        
        plt.pause(interval) # seconds
        plt.clf()
        plt.cla()
    
    
    def _draw_line_between_two_points(self, p1, p2, color_line="purple"):
        plt.plot([p1[1], p2[1]], [p1[0], p2[0]], color=color_line, linewidth=2)
        plt.draw()  # Update the plot with the new line
        
        
    def _draw_a_point(self, position, color="orange"):
        plt.scatter(position[1], position[0], c=color)
        
        