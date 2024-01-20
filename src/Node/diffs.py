from PIL import Image
import numpy as np
from Node import nodes




def image_dimensions_return_list(image1:np.ndarray):
    '''
    Function to return the shape of the image in tuple
    '''
    return(list(np.shape))


def check_image_dimensions_return_bool(image1:np.ndarray,
                                       image2:np.ndarray):
    '''
    Function to check if the dimensions of the image are still same.
    Inputs->[image1:np.ndarray,image2:np.ndarray]
    ouput->bool
    '''

    return (image1.shape==image2.shape)


def changed_pixel_return_dict(image1:np.ndarray,
                              image2:np.ndarray):

    '''
    INPUT:-
    image1 and image2 both of np.ndarray dtype

    Function iterates over all the pixels and stores the pixels that have changed in dict

    OUTPUT:-
    the output of this function is a dictionary
    the key comprises of a list that specifies the location of the pixel that changed, and
    the value comprises of the decimal(float) value signifying the change in the pixel 
    '''

    if(check_image_dimensions_return_bool(image1=image1,image2=image2)):
        _shape=image_dimensions_return_list(image1)
        _dict={}
        _i,_j,_k=_shape
        for i in _i:
            for j in _j:
                for k in _k:
                    if(image1[i][j][k]!=image2[i][j][k]):
                        _change=(image2[i][j][k])-image1[i][j][k]
                        _dict.update({'pixel':(i,j,k),'change':_change})
                    else:
                        continue
        return _dict
    else:
        raise Exception(f"The dimensions of the image are not same. PixV isnt compatible with cropping and changing dimensions of image.")
    



def Add_diffs_from_head_till_root(imageGraph_instance:nodes.imageGraph):

    '''
    Input->[nodes.imageGraph]

    Function to add all the diffs at each node from head till root.
    This function calculates the final image array at the current head.
    However right now this function wont support any version wont have the same dimensions.

    output->[numpy.ndarray]
    '''

    _current_head_location=imageGraph_instance.Head
    while(imageGraph_instance.in_nodes is not None):
        

    pass
