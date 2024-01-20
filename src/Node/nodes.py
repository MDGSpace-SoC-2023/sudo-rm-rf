import os
from datetime import datetime
import uuid
from src.utils import Pixels
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
        self.version_name=version_name
        self.out_nodes=None
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

        return node_dict
    
    
class rootNode(graphNode):
    def __init__(self,
                 image:np.ndarray,
                 author:str,
                 version_name:str,
                 in_nodes=None,
                 commit_message=None,
                 ):
        self.image=image
        super().__init__(change=dict(),version_name=version_name,author=author,in_nodes=in_nodes,commit_message=commit_message,out_nodes=None)



class imageGraph:
    def __init__(self,
                 image:np.ndarray,
                 author:str,
                 graph_name:str):
        self.root_node=rootNode(image=image,author=author,version_name=graph_name)
        self.Head=self.root_node #head kaha point kar raha hai
        self.graph_name=graph_name
        self.image=image


    
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

                for key in _change.keys():
                    if(key in _all_changes.keys()):
                        _all_changes[key]+=_change[key]
                    else:
                        _all_changes[key]=_change[key]
                        
                _head=_head.in_nodes.Head


        else:
            _all_changes={}
        return _all_changes
    

    def return_np_image_at_head(self):

        '''

        Function to return complete image in np.ndarray dtype at Head of imageGraph
        this function is intended to be used to calculate the changes in the new version during a commit.
        return image in np.ndarray format.
        
        
        '''
        _all_changes=imageGraph._traverse_graph()
        image=self.image

        for key in _all_changes.keys():
            i,j,k=key
            image[i][j][k]+=_all_changes[key]  

        return image #np.ndarray



    def show_image(self):
        _all_changes=imageGraph._traverse_graph()
        image=self.image

        for key in _all_changes.keys():
            i,j,k=key
            image[i][j][k]+=_all_changes[key]   
        plt.imshow(image)
    



path="/Users/somshekharsharma/Downloads/tsh.jpg"
graph1=imageGraph(image=Pixels.image_to_array(path),author="som")

print(type(graph1.Head))
# node2
# graph1.root_node.out_nodes=

# print(graph1.root_node)