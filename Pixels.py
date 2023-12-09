from PIL import Image
import numpy as np

def extract_pixel_values(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to a NumPy array
    pixel_array = np.array(image)
    height = pixel_array.shape[0]
    width = pixel_array.shape[1]
    channels = pixel_array.shape[2]

    return pixel_array

class ImageProcessor:
    @staticmethod
    def Imgshape(pixel_array):
        height, width, channels = pixel_array.shape
        return height, width, channels 

#######

# # Example usage:
# image_path = "path/to/your/image.jpg"
# pixels = extract_pixel_values(image_path)
# processor = ImageProcessor()
# height, width, channels = processor.Imgshape(pixels)

