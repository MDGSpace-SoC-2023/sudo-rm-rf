import numpy
from utils import Pixels
import matplotlib.pyplot as plt


path1="/Users/somshekharsharma/Downloads/bkl.jpg"


image1=Pixels.image_to_array(path)


plt.imshow(image1)
plt.show()
