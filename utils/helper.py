import pickle
from PIL import Image
import numpy as np


#for saving the instance of ImageGraph class

'''input -> instance of ImageGraph object'''

class GraphSave:
   _instance = None

   def __new__(cls, *args, **kwargs):
       if cls._instance is None:
           cls._instance = super(GraphSave, cls).__new__(cls, *args, **kwargs)
       return cls._instance

   def __init__(self)->None:
       if not hasattr(self, 'counter'):
           self.counter = 0

   def savegraph(self, instance_ImageGraph):
       filename = f'../Graphs/instance_{self.counter}.pkl'

       with open(filename, 'wb') as f:
           pickle.dump(instance_ImageGraph, f)

       print(f"Graph : {str(instance_ImageGraph)} saved at {filename}")
       self.counter += 1

   def loadgraph(self,location):
        with open(location,'rb') as f:
            loaded_image_graph = pickle.load(f)
            return loaded_image_graph





# function to create image array from its path
def imp(path):
    image = Image.open(path)
    image_array = np.asarray(image)
    return image_array 
    #returns numpy array






