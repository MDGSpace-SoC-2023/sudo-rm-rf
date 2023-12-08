from PIL import Image
import numpy as np

def extract_pixel_values(image_path):
    # Open the image
    image = Image.open(image_path)

    # Convert the image to a NumPy array
    pixel_array = np.array(image)

    return pixel_array

print(extract_pixel_values("/Users/somshekharsharma/Downloads/WhatsApp Image 2023-11-28 at 20.04.11 (1).jpeg").shape)