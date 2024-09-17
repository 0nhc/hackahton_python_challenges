from data_structure import GraphNode
from state_define import *
import numpy as np
import random
from PIL import Image


class RectangularMaze:
    """
    Retangular Maze
    
    Attributes:
        self.num_rows: The number of rows in this 2D matrix maze
        self.num_columns = The number of columns in this 2D matrix maze
        self.num_nodes = The number of grapgh nodes in this 2D matrix maze
        self.state = The node's state for visualizing
        self.score The node's score for finding the shortest path
    """
    def __init__(self, num_rows=1, num_columns=1) -> None:
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_nodes = self.num_rows * self.num_columns
        self.start_node_index = 0
        self.goal_node_index = 0
        self.position_to_node_index_table = {}
        self.init_node_to_be_wall_posibility = random.random()
        
        self.nodes = []
        
        
        # Initialize a 2D graph with Node data structure
        node_index = 0
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                p = [i,j]
                neighbours = [[p[0]-1,p[1]], [p[0],p[1]+1], [p[0]+1,p[1]], [p[0],p[1]-1]]
                neighbours = self._neighbours_filter(neighbours)
                new_node = GraphNode(position=p, index=node_index, neighbours=neighbours, state=INIT)
                self.position_to_node_index_table[str(p)] = node_index
                self.nodes.append(new_node)
                node_index += 1
            
                
    def as_matrix(self):
        matrix = np.zeros((self.num_rows, self.num_columns))
        node_index = 0
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                matrix[i,j] = self.nodes[node_index].state
                node_index += 1
        return matrix
    
    
    def as_nodes(self):
        return self.nodes
    
    
    def init_random_maze_map(self):
        # Generate a random start node
        random_position = self._generate_random_position_within_matrix()
        start_node_index = self.position_to_node_index_table[str(random_position)]
        self.nodes[start_node_index].state = START
        self.start_node_index = start_node_index
        
        # Walk random steps and set FREE nodes
        num_steps = random.randint(1, self.num_rows*self.num_columns-1)
        current_node_index = self.nodes[start_node_index].index
        for i in range(num_steps):
            # Move to a random neighbour
            neighbour_positions = self.nodes[current_node_index].neighbours
            random_neighbour_choice_index = random.randint(0, len(neighbour_positions)-1)
            random_neighbour_position = neighbour_positions[random_neighbour_choice_index]
            random_neighbour_index = self.position_to_node_index_table[str(random_neighbour_position)]
            if(self.nodes[random_neighbour_index].state == INIT or self.nodes[random_neighbour_index].state == FREE):
                current_node_index = random_neighbour_index
                self.nodes[current_node_index].state = FREE
        
        # Set the end node
        self.nodes[current_node_index].state = GOAL
        self.goal_node_index = current_node_index
        
        # Set other nodes from INIT state to WALL and FREE randomly
        for i in range(self.num_nodes):
            if(self.nodes[i].state == INIT):
                choice = random.random()
                if(choice < self.init_node_to_be_wall_posibility): # Is wall
                    self.nodes[i].state = WALL
                else: # Is FREE
                    self.nodes[i].state = FREE
        
    
    def load_from_image_with_random_start_and_goal(self, image_path):
        # Reset all nodes
        self.nodes = []
        # Open the image and convert it into numpy format
        with Image.open(image_path) as img:
            grayscale_array = img.convert('L') # Convert the image to grayscale
            grayscale_array = np.array(grayscale_array)
        
        # Re-initialize a 2D graph with Node data structure
        self.num_rows = grayscale_array.shape[0]
        self.num_columns = grayscale_array.shape[1]
        self.num_nodes = self.num_rows * self.num_columns
        node_index = 0
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                p = [i,j]
                neighbours = [[p[0]-1,p[1]], [p[0],p[1]+1], [p[0]+1,p[1]], [p[0],p[1]-1]]
                neighbours = self._neighbours_filter(neighbours)
                # Set state for every node
                state = INIT
                if(grayscale_array[i,j] == 255):
                    state = FREE
                elif(grayscale_array[i,j] == 0):
                    state = WALL
                new_node = GraphNode(position=p, index=node_index, neighbours=neighbours, state=state)
                self.position_to_node_index_table[str(p)] = node_index
                self.nodes.append(new_node)
                node_index += 1
        
        # Give random start and goal point
        while(True):
            random_position = self._generate_random_position_within_matrix()
            start_node_index = self.position_to_node_index_table[str(random_position)]
            if(self.nodes[start_node_index].state == FREE):
                self.nodes[start_node_index].state = START
                self.start_node_index = start_node_index
                break
        
        while(True):
            random_position = self._generate_random_position_within_matrix()
            goal_node_index = self.position_to_node_index_table[str(random_position)]
            if(self.nodes[goal_node_index].state == FREE):
                self.nodes[goal_node_index].state = GOAL
                self.goal_node_index = goal_node_index
                break
    
    
    def is_position_within_matrix_boundary(self, position):
        if(position[0] < 0):
            return False
        elif(position[0] > self.num_rows):
            return False
        
        if(position[1] < 0):
            return False
        elif(position[1] > self.num_columns):
            return False
        
        return True
        
                
            
    def _neighbours_filter(self, position_list):
        # Remove positions out of the maze boundary
        valid_positions = []
        for position in position_list:
            if(position[0] < 0):
                continue
            if(position[0] >= self.num_rows):
                continue
            if(position[1] < 0):
                continue
            if(position[1] >= self.num_columns):
                continue
            valid_positions.append(position)
        return valid_positions
            
            
    def _generate_random_position_within_matrix(self):
        row_index = random.randint(0,self.num_rows-1)
        column_index = random.randint(0,self.num_columns-1)
        return [row_index, column_index]
    
    
class HexagonalMaze:
    """
    Hexagonal Maze
    
    Attributes:
        self.num_rows: The number of rows in this 2D matrix maze
        self.num_columns = The number of columns in this 2D matrix maze
        self.num_nodes = The number of grapgh nodes in this 2D matrix maze
        self.state = The node's state for visualizing
        self.score The node's score for finding the shortest path
    """
    def __init__(self, num_rows=1, num_columns=1) -> None:
        self.num_rows = num_rows
        self.num_columns = num_columns
        
        if(self._is_even(self.num_rows)):
            self.num_nodes = self.num_rows * self.num_columns + self.num_rows/2
        else:
            self.num_nodes = self.num_rows * self.num_columns + (self.num_rows-1)/2
        
    def _is_even(self, number):
        return number % 2 == 0
    
    def _is_odd(self, number):
        return number % 2 != 0
            