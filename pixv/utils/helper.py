import pickle
from datetime import datetime
import matplotlib.pyplot as plt
import os

def  save_graph(object_instance):
    graphs_dir = os.path.dirname(__file__)
    parent_dir = os.path.join(os.path.dirname(graphs_dir),'Graphs')

    name=object_instance.graph_name
    path=parent_dir+"/"+name+".pkl"

    with open(path, 'wb') as output:
       pickle.dump(object_instance,output,pickle.HIGHEST_PROTOCOL)


def load_graph(graph_name):

    '''
    function to load imageGraph object from pickle file

    input-> graph_name , graph_name attribute of imageGraph instance
    output-> imageGraph object
    '''
    graphs_dir = os.path.dirname(__file__)
    parent_dir = os.path.join(os.path.dirname(graphs_dir),'Graphs')

    path=parent_dir+'/'+graph_name+".pkl"
    
    with open(path,'rb') as input:
        graph=pickle.load(input)
    return graph


def show_image(obj):
   image_array= obj.image

   plt.imshow(image_array)
   plt.title("Displayed Image")
   plt.show()


