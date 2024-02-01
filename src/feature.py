from Node import nodes
from Node.diffs import changed_pixel_return_dict as cprd
from utils.Pixels import image_to_array as itoa
from utils.Pixels import is_image_changed as iic
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



def add_new_node(imageGraph_instance:nodes.imageGraph,
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
    stores changes in the image in dict format

    returns a nodes.graphImage object, 
    doesn't save the new graph
    '''

    _image_head=imageGraph_instance.return_np_image_at_head()
    _head=imageGraph_instance.Head
    # _image=imageGraph_instance.return_np_image_at_head()
    if(iic(_image_head, image)):
        _change_dict=cprd(_image_head,image)

        new_node=nodes.graphNode(
                                change=_change_dict,
                                author=author,
                                in_nodes=_head,
                                commit_message=commit_message)
        
        _head.out_nodes.append(new_node)
        imageGraph_instance.Head=new_node
        imageGraph_instance.log.append(new_node)
        return imageGraph_instance
    else:
        raise Exception(f"Image has not been changed with respect to the current location of the HEAD in the graphImage")
        


def revert_head_by_one_return_imageGraph(imageGraph_instance:nodes.imageGraph):
    current_head=imageGraph_instance.Head
    if(current_head.in_nodes is None):
        raise Exception(f'The Head is already pointing at the root node there are no previous versions.')
    else:
        reverted_head=current_head.in_nodes

        imageGraph_instance.Head=reverted_head

        print(f"The head has been reverted to \n unique_id: {reverted_head.unique} \n message: {reverted_head.commit_message} \n author :{reverted_head.author}\n time: {reverted_head.time}")
        
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
    if(len(_head.out_nodes) == 1):
        imageGraph_instance.Head=_head.out_nodes[0]
        print(f"\n The head has been forwarded to \n unique_id: {imageGraph_instance.Head.unique} \n message: {imageGraph_instance.Head.commit_message} \n author :{imageGraph_instance.Head.author} \n time :{imageGraph_instance.Head.time}")
    elif(len(_head.out_nodes)>1):
        print(f"\nThere are multiple nodes going out from the current HEAD location \n")
        print(f"The outgoing nodes are : \n")

        for i in range(len(_head.out_nodes)):
            print(i+1, ' Node \n' )
            _print_details(_head.out_nodes[i])

        print(f" To shift the head on any of the graphNode, Use shift command with the respective unique id")
    else:
        raise Exception(f"There are no outgoing nodes from current HEAD")
    
def forward_head_by_one_save_imageGraph(image_path:str):
    _imageGraph_path=image_path.split('/')[-1].split('.')[0]
    _imageGraph_instance=load_graph(_imageGraph_path)
    _imageGraph_path=forward_head_by_one_return_imageGraph(_imageGraph_instance)
    save_graph(_imageGraph_instance)

def show_image_(_graph_name:str):
    _imageGraph=load_graph(_graph_name)
    _imageGraph.show_image()

def _print_details(_head):
    print(f" \n {type(_head)}\n unique id : {_head.unique} \n Commit Message : {_head.commit_message}\n Author : {_head.author} \n Time : {_head.time} \n ")
    

@click.group()
def cli():
    pass

@cli.command()
@click.argument("graph_name")
def locate(graph_name):
    print(f"\n The Head is currrently pointing to the following graphNode :\n")
    gr_=load_graph(graph_name)
    _head=gr_.Head
    _print_details(_head)

@cli.command()
@click.argument("image_path")
def logs(image_path):
    _graph_name=image_path.split('/')[-1].split('.')[0]
    _gr=load_graph(_graph_name)
    for i in range(len(_gr.log)):
        _print_details(_gr.log[i])

# @click.argument('IMAGE_PATH')
@cli.command()
@click.argument("graph_name")
def show(graph_name):
    print(f"The image is loading")
    show_image_(graph_name)


@cli.command()
# @click.option("--paths", help="Path of the Image")
@click.argument('PATHS')
@click.option("--author", help="Author Name")
def add(paths,author):
    if paths is None or not os.path.isfile(paths):
       click.echo("Error: Invalid image path.")
       return
    else:
        create_root_node(image_path=paths,
                        author=author)
        

@cli.command()
@click.argument('IMAGE_PATH')
@click.option('--author',help="Author Name")
@click.option('--message',help="Commit Message")
def commit(image_path,author,message):

    if image_path is None or not os.path.isfile(image_path):
       click.echo("Error: Invalid image path.")
       return
    else:
        add_version(image_path=image_path,commit_message=message,author=author)
        print("Added a new version.")
        

@cli.command()
@click.argument('IMAGE_PATH')
def revert(image_path):
    
    if image_path is None or not os.path.isfile(image_path):
       click.echo("Error: Invalid image path.")
       return
    else:
        revert_by_one_save_imageGraph(image_path=image_path)
        print("The head has been reverted by one position")


@cli.command()
@click.argument('IMAGE_PATH')
def forward(image_path):
    
    if image_path is None or not os.path.isfile(image_path):
       click.echo("Error: Invalid image path.")
       return
    else:
        forward_head_by_one_save_imageGraph (image_path=image_path)


@cli.command()
@click.argument('IMAGE_PATH')
def original(image_path):
    
    if image_path is None or not os.path.isfile(image_path):
       click.echo("Error: Invalid image path.")
       return
    else:
        _name_graph=image_path.split('/')[-1].split('.')[0]
        _gr=load_graph(_name_graph)
        show_image(_gr)


@cli.command()
@click.argument('IMAGE_PATH')
@click.option('--id', help="unique id of the node you want to locate")
def shift(image_path,id):
    
    if image_path is None or not os.path.isfile(image_path):
       click.echo("Error: Invalid image path.")
       return
    else:
        _name_graph=image_path.split('/')[-1].split('.')[0]
        _gr=load_graph(_name_graph)
        _gr.shift_head_by_unique(id)
        save_graph(_gr)



if __name__ == "__main__":
    cli()
