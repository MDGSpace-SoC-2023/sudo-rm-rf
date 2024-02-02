import os
from datetime import datetime
import uuid
from utils import Pixels
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

class graphNode:
    def __init__(self,
                 change:dict,
                 in_nodes,
                 author:str,
                 commit_message=None,
                 version_name=None
                 ) :
        self.change=change
        self.version_name=version_name
        self.out_nodes=list()
        self.in_nodes=in_nodes
        self.time=datetime.now()
        self.commit_message=commit_message
        self.author=author
        self.unique=uuid.uuid4()
    
    def dictNode(self):
        node_dict = {
            "Change": self.change,
            "version_name": self.version_name,
            "out_nodes": self.out_nodes,
            "in_nodes": self.in_nodes,
            "time": str(self.time),  # Convert datetime to string
            "commit_message": self.commit_message,
            "author": self.author,
            "unique": str(self.unique)  # Convert UUID to string
        }

        print(node_dict)
    
    
class rootNode(graphNode):
    def __init__(self,
                 image:np.ndarray,
                 author:str,
                 version_name:str,
                 in_nodes=None,
                 commit_message=None,
                 ):
        self.image=image
        self.out_nodes=list()
        super().__init__(change=None,version_name=version_name,author=author,in_nodes=in_nodes,commit_message=commit_message)
        super().dictNode()




class imageGraph:
    def __init__(self,
                 image:np.ndarray,
                 author:str,
                 graph_name:str):
        self.root_node=rootNode(image=image,author=author,version_name=graph_name)
        self.Head=self.root_node #head kaha point kar raha hai
        self.graph_name=graph_name
        self.image=image
        self.log=list()
        self.log.append(self.root_node)

    def find_node_by_unique(self, unique_id, node=None):
        """
        Find a graphNode with a given unique identifier using depth-first search (DFS).

        Args:
        unique_id (str): The unique identifier of the node to find.
        node (graphNode): The starting node for the search. Default is None (start from the root).

        Returns:
        graphNode or None: The node with the given unique identifier if found, else None.
        """
        unique_id=unique_id.strip()
        if node is None:
            node = self.root_node #will start searching from rootNode
            print(f"\nStarting search from rootNode")
        # Check if the current node matches the unique identifier
        if str(node.unique) == unique_id:
            print(f"graphNode found")
            return node

        # Recursively search in the children nodes
        if len(node.out_nodes)!=0:
            for child_node in node.out_nodes:
                result = self.find_node_by_unique(unique_id, child_node)
                if result:
                    return result

        return None
    
    def shift_head_by_unique(self, unique_id):
        """
        Shift the head location to the node with the given unique identifier if it exists.

        Args:
        unique_id (str): The unique identifier of the node to shift the head to.

        Returns:
        bool: True if the head location is shifted, False otherwise.
        """
        node = self.find_node_by_unique(unique_id)
        if node:
            self.Head = node
            print(f"Shifted HEAD to {unique_id} \n")
            return True
        else:
            print("Not a valid unique ID.")
            return False

    
    def _traverse_graph(self):

        '''
        Private function to climb up the graph from the current head location to rootNode.
        And calculate the total changes and return a dictionary for the changes.

        Isnt compatible when number of pixels in the nodes have been changed with respect to each other.
        '''
        if(type(self.Head) is not rootNode):
            _head=self.Head
            _all_changes={}
            _all_changes.update(_head.change)

            while(_head.in_nodes is not None):
                _change=_head.in_nodes.change
                if(_change is not None):

                    for key in _change.keys():
                        if(key in _all_changes.keys()):
                            _all_changes[key]+=_change[key]
                        else:
                            _all_changes[key]=_change[key]
                            
                    _head=_head.in_nodes
                else:
                    break
            # print(_all_changes)


        else:
            _all_changes={}
        return _all_changes
    

    def return_np_image_at_head(self):
        '''
        Function to return complete image in np.ndarray dtype at Head of imageGraph
        this function is intended to be used to calculate the changes in the new version during a commit.
        return image in np.ndarray format.
        
        '''

        _all_changes=self._traverse_graph()
        image_=self.image.copy()


        for key in _all_changes.keys():
            if len(key) == 3:
                i,j,k=key
                # print(f"keys are {key}")
                image_[i][j][k]+=_all_changes[key]  
            else:
                print("bhaii kya, 4 dimensions kaise image ke?")

        return image_ #np.ndarray


    def print_graph_tree(self,node,indent=''):
        """
        Recursively prints the tree structure of a graph starting from the specified node.

        Args:
        node (graphNode): The starting node from which to print the tree structure.
        indent (str): The indentation string to use for each level of the tree.
        """
        # Print the current node
        print(indent + '+-'+ str(node.unique) )
        child_indent = indent +'|' +' '*4

        # Iterate over each child node

        if(len(node.out_nodes)==0):
            return
        else:
            for child in node.out_nodes:
                self.print_graph_tree(node=child, indent=child_indent)



    def show_image(self):
        _all_changes=self._traverse_graph()
        image_=self.image.copy()

        for key in _all_changes.keys():
            i,j,k=key
            image_[i][j][k]+=_all_changes[key] 

        plt.imshow(image_)
        plt.show()

    