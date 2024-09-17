from data_structure import TreeNode
from state_define import *

class Tree:
    """
    Tree
    
    Attributes:
        TODO
    """
    def __init__(self, init_node = TreeNode()) -> None:
        self.start_node = init_node
        self.nodes = [self.start_node]
        self._node_index = self.start_node.index + 1
    
    
    def add_node(self, new_node):
        new_node.index = self._node_index
        parent_index = new_node.parent
        if(parent_index < self.start_node.index or parent_index >= (self.start_node.index + len(self.nodes))):
            print("Invalid parent node index. Not found in the tree.")
            return
        else:
            self.nodes.append(new_node)
            self.nodes[parent_index].add_a_child(new_node.index)
        self._node_index += 1
        
    def as_nodes(self):
        return self.nodes

            