from Node import nodes
from utils.pixels import image_to_array as itoa
from utils.pixels import is_image_changed as iic
from utils.helper import save_graph , load_graph, show_image
import argparse
import os
import numpy as np
import click



def check_graph_initialise(name):
    '''
    To check if the image already has a graph.pkl file
    cons:
        - image name should not be changed
    It searches name.pkl file in Graphs directory

    returns a bool value
    '''

    _path="Graphs/"+name+".pkl"
    check_file_existence=os.path.exists(_path)

    return check_file_existence


def create_root_node(image_path:str,
                     author:str):
    '''
    Function to add a root node and initalise the graph
    Takes image from image_path and convert into numpy.ndarray
    Initalises graphImage with graph_name as image name

    Also, saves the graph at IVCS/Graphs/ using helper.save_graph
    Checks if the same graph already exists

    inputs->[image_path,
             author]
    
    '''

    _graph_name=(image_path.split('/')[-1]).split('.')[0]
    _image=itoa(image_path)

    if(not check_graph_initialise(_graph_name)):
        gr=nodes.imageGraph(image=_image,author=author,graph_name=_graph_name)
        save_graph(gr)
        print(f"The imageGraph has been initialised for {image_path} at Graphs/{_graph_name}")


    else:
        raise Exception(f"The imageGraph for this image has already been initialised.")



def add_new_node(imageGraph_instance:nodes.graphNode,
                commit_message:str,
                author:str,
                image:np.ndarray):
    '''
    inputs->[imageGraph object, 
             commit message,
             author,
             image]

    Function to add a new node on the current head location in the nodes.imageGraph object
    Expects an established graph which has a nodes.graphNode object
    if the graph of the image has not been initalised, use create_root_node to initalise

    returns a nodes.graphImage object, 
    doesn't save the new graph
    '''

    head=imageGraph_instance.Head

    if(iic(head.image, image)):
        new_node=nodes.graphNode(
                                image=image,
                                author=author,
                                in_nodes=head,
                                commit_message=commit_message)
        
        head.out_nodes=(new_node)
        imageGraph_instance.Head=new_node

        return imageGraph_instance
    else:
        raise Exception(f"Image has not been changed with respect to the current location of the HEAD in the graphImage")
        


def revert_head_by_one_return_imageGraph(imageGraph_instance:nodes.imageGraph):
    current_head=imageGraph_instance.Head
    reverted_head=current_head.in_nodes

    imageGraph_instance.Head=reverted_head

    print(f"The head has been reverted to \n "
         "unique: {reverted_head.unique} \n "
         "message: {reverted_head.commit_message} by author :{reverted_head.author}")
    
    return imageGraph_instance


def revert_by_one_save_imageGraph(image_path:str):
    _imageGraph_path=image_path.split('/')[-1].split('.')[0]
    _imageGraph_instance=load_graph(_imageGraph_path)
    _imageGraph_instance=revert_head_by_one_return_imageGraph(_imageGraph_instance)
    save_graph(_imageGraph_instance)



def add_version(image_path:str,
                author:str,
                commit_message:str):
    _image=itoa(image_path)
    _graph_name=((image_path.split('/')[-1]).split('.'))[0]
    _imageGraph_instance=load_graph(_graph_name)
    _imageGraph_instance=add_new_node(imageGraph_instance=_imageGraph_instance,
                                      image=_image,author=author,
                                      commit_message=commit_message)
    save_graph(_imageGraph_instance)

def forward_head_by_one_return_imageGraph(imageGraph_instance:nodes.imageGraph):
    _head=imageGraph_instance.Head
    if(_head.out_nodes is not None):
        imageGraph_instance.Head=_head.out_nodes

    else:
        raise Exception(f"There are no outgoing nodes from current HEAD")
    
def forward_head_by_one_save_imageGraph(image_path:str):
    _imageGraph_path=image_path.split('/')[-1].split('.')[0]
    _imageGraph_instance=load_graph(_imageGraph_path)
    _imageGraph_path=forward_head_by_one_return_imageGraph(_imageGraph_instance)
    save_graph(_imageGraph_instance)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('IMAGE_PATH')
@click.option("--u", help="Author Name")
def add(IMAGE_PATH,AUTHOR):
    if IMAGE_PATH is None or not os.path.isfile(IMAGE_PATH):
       click.echo("Error: Invalid image path.")
       return
    else:
        create_root_node(image_path=IMAGE_PATH,
                        author=AUTHOR)
    

@cli.command()
@click.argument('IMAGE_PATH')
@click.option('--u',help="Author Name")
@click.option('--m',help="Commit Message")
def commit(IMAGE_PATH,AUTHOR,MESSAGE):

    if IMAGE_PATH is None or not os.path.isfile(IMAGE_PATH):
       click.echo("Error: Invalid image path.")
       return
    else:
        add_version(image_path=IMAGE_PATH,commit_message=MESSAGE,author=AUTHOR)
        

@cli.command()
@click.argument('IMAGE_PATH')
def revert(IMAGE_PATH):
    
    if IMAGE_PATH is None or not os.path.isfile(IMAGE_PATH):
       click.echo("Error: Invalid image path.")
       return
    else:
        revert_by_one_save_imageGraph(image_path=IMAGE_PATH)


@cli.command()
@click.argument('IMAGE_PATH')
def forward(IMAGE_PATH):
    
    if IMAGE_PATH is None or not os.path.isfile(IMAGE_PATH):
       click.echo("Error: Invalid image path.")
       return
    else:
        forward_head_by_one_save_imageGraph (image_path=IMAGE_PATH)

        

