from PIL import Image
import numpy as np

def image_to_array(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    return image_array



def is_image_changed(image1,image2):

    if(image1==image2):
        return True
    else:
        return False