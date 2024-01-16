import os
from datetime import datetime
import uuid

import numpy as np
from PIL import Image

class graphNode:
    def __init__(self,
                 image:list,
                 in_nodes,
                 author:str,
                 commit_message=None,
                 version_name=None
                 ) :
        self.image=image
        self.version_name=version_name
        self.out_nodes=None
        self.in_nodes=in_nodes
        self.time=datetime.now()
        self.commit_message=commit_message
        self.author=author
        self.unique=uuid.uuid4()
    
    def dictNode(self):
        node_dict = {
            "image": self.image,
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
                 image:list,
                 author:str,
                 version_name:str,
                 in_nodes=None,
                 commit_message=None,
                 ):
        super().__init__(image=image,version_name=version_name,author=author,in_nodes=in_nodes,commit_message=commit_message,out_nodes=None)



class imageGraph:
    def __init__(self,image,author,graph_name):
        self.root_node=rootNode(image=image,author=author,version_name=graph_name)
        self.Head=self.root_node #head kaha point kar raha hai
        self.graph_name=graph_name



# path="/Users/somshekharsharma/Downloads/tsh.jpg"

# graph1=imageGraph(image=pixels.image_to_array(path),author="som")
# node2
# graph1.root_node.out_nodes=

# print(graph1.root_node)