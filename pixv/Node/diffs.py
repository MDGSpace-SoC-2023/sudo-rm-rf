from PIL import Image
import numpy as np


def image_dimensions_return_list(image1:np.ndarray):
    '''
    Function to return the shape of the image in tuple
    '''
    return((np.shape(image1)))


def check_image_dimensions_return_bool(image1:np.ndarray,
                                       image2:np.ndarray):
    '''
    Function to check if the dimensions of the image are still same.
    Inputs->[image1:np.ndarray,image2:np.ndarray]
    ouput->bool
    '''

    return (image1.shape==image2.shape)

# print(check_image_dimensions_return_bool(image1,image2))



# zhape=(image_dimensions_return_list(image1))
# print(zhape)
# _i,_j,_k=zhape
# print(_i)

def changed_pixel_return_dict(head_image:np.ndarray,
                              new_image:np.ndarray):

    '''
    INPUT:-
    image1 and image2 both of np.ndarray dtype

    Function iterates over all the pixels and stores the pixels that have changed in dict

    OUTPUT:-
    the output of this function is a dictionary
    the key comprises of a list that specifies the location of the pixel that changed, and
    the value comprises of the decimal(float) value signifying the change in the pixel 

    '''


 

    if(check_image_dimensions_return_bool(image1=head_image,image2=new_image)):
        _shape=image_dimensions_return_list(head_image)
        changes_dict={}
        changes_count=0

        _i,_j,_k=_shape
        for i in range(_i):
            for j in range(_j):
                for k in range(_k):
                    # count2=count2+1
                    if(head_image[i][j][k]!=new_image[i][j][k]):
                        changes_count=changes_count+1
                        _change=(new_image[i][j][k])-head_image[i][j][k]
                        _list=(i,j,k)

                        changes_dict[_list]=_change
                    else:
                        continue
        return changes_dict
        # print(count2)
        # return count
    else:
        raise Exception(f"The dimensions of the image are not same. PixV isnt compatible with cropping and changing dimensions of image.")
    
# ert=changed_pixel_return_dict(image2,image4)
# print(ert)



