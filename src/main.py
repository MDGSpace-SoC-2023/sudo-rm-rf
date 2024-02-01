import numpy as np
from PIL import Image
from utils import helper
from matplotlib import pyplot as plt
import cv2 as cv

path = "/Users/somshekharsharma/Downloads/bkl2.png"
path_graph = "/Users/somshekharsharma/Desktop/SOC/src/Graphs/bkl2.pkl"

obj = helper.load_graph("bkl2")

# print(type(obj.Head.image))
# print(obj.Head.image.dtype)  # Check the data type of the image array

# # Convert image array to float32 if it's not already
# img = obj.Head.image.astype(np.float32)

# # Drop the fourth channel if present
# img = img[:, :, :3]

# Display the image
# plt.imshow(img)
# plt.show()
image2=Image.open(path)
image = cv.imread (path)
image2=np.array(image2,dtype=np.uint64)
image2=image2[:,:,:3]
# print(image)
print(image2)
# print(type(image))
# print(image.shape)
plt.imshow(image2)
print(image2.dtype)
plt.show()
# cv.imshow('Cristiano Ronaldo', image)
