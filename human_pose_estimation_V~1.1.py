# -*- coding: utf-8 -*-
"""Human Pose Estimation V~1.4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uTyv5ZhLaZikadHvx1WKZ-MaPRGuxOyz

## Human Pose Estimation
### Process where it estimates the position of human and detects all the parts available.
### We use Posenet for detecting poses.
### Process: 
Model detects the person first and then it detects the joints and parts. Posenet detects total of 18 parts right from feet to eyes, ears, nose etc.
### Result:
 Results would be in three formats.
 1. Heat map: Heat map co-ordinates are generated
 2. draw humans: Skeleton part of human image is generated.
 3. inference: We will get class of bodyparts which contains the co-ordinates of each body part and confidence of the respective body part

 ## Note: tf-pose is the library used for pose estimation. IT doesn't support the latest version of tf (2X), rather supports the older version (1x) make sure older version is installed. Else when tf-pose is installing, it will automatically downgrade tf to older version. tf-pose is working on compactibility on newer versions.

## Import Libraries
"""

!pip install tf-pose

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

## import estimators.
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import model_wh

## Image manipulation
import cv2
from PIL import Image

"""### Function to display image"""

def display_image(image):
  fig= plt.figure(figsize=(8,8))
  plt.grid(False)
  plt.imshow(image)
  plt.show()

"""### Load pose estimator 
### weights are pre downloaded and passed to TfPoseEstimator class
"""

weights_path='/content/drive/My Drive/Computer Vision Interview/Human Pose Estimation/graph_opt.pb'
w, h= 400, 400
model= TfPoseEstimator(weights_path, target_size=(400,400))

### Image loading
image_path='/content/drive/My Drive/Computer Vision Interview/Object Detection/goa.JPG'
pil_image= Image.open(image_path)
image= np.array(pil_image)

image.shape

"""### for much faster results, we will resize"""

image= cv2.resize(image, (600,400), interpolation= cv2.INTER_AREA)

display_image(image)

"""### Passing the image for inference"""

humans= model.inference(image, resize_to_default=True, upsample_size=5.0)

humans

"""#### Now we have got the co-ordinates of body parts and its confidence.
#### Generate heat map for the humans detected.
##### This can be done by taking heatMat class available in model, it is updated or generated when inference method is called.
"""

print(model.heatMat.shape)

"""## The last dimension of the heat map is 18 parts and confidence of the parts
## While marking points on the graph, we will take off the last value and plot first 18 values
"""

## Pickup the max values in the array
max_prob= np.amax(model.heatMat[:,:,:-1], axis=2)
print(max_prob.shape)

### Plot the values
plt.imshow(max_prob)

"""### Skeletons of the humans
#### Retrieving skeletal parts of humans
"""

skeletal_image= model.draw_humans(image, humans)

skeletal_image.shape

### Plot the image
plt.imshow(skeletal_image)

"""### Lets Draw only skeletal part of the image.
#### This can be done by passing an empty image to draw the skeletal part
"""

empty_img= np.zeros((image.shape))
skeletal= model.draw_humans(empty_img, humans, imgcopy=True)

plt.imshow(skeletal)

"""### Drawing the co-ordinates of joints/parts
inference rsult has all the co-ordinates of bodyparts aswell as the confidence of each bodypart
"""

humans

"""### the result is a list of classes.
### for each element in the list we will find the attributes which stores the docy part as well as the co-ordinates.
"""

bodyparts=getattr(humans[0], 'body_parts')

bodyparts

### Consider the attributes of co-ordinates
co_ordinates=[]
for part in bodyparts.keys():
  axis=[]
  x= getattr(bodyparts[part],'x')
  y= getattr(bodyparts[part], 'y')
  ##Store it in the axis
  axis.append(x)
  axis.append(y)
  co_ordinates.append(axis)

co_ordinates

### Convert Co-ordinates to array
co_ordinates= np.array(co_ordinates)

"""## The co-ordinates in array are the percentages of the shape of the image.
### Multiplying the image shape with co-ordinates will give the exact number to plot
"""

pixel_co_ordinate= co_ordinates * (image.shape[1], image.shape[0])

pixel_co_ordinate

## Lets plot the image of points
### Seperate x and y axis from the array
x,y= zip(*pixel_co_ordinate)
###Create a figure and set axis equal to image size
fig= plt.figure(figsize=(8,8))
plt.axis([0, image.shape[1], 0, image.shape[0]])
plt.scatter(x, y,marker='*' )

##3 the y axis is inverted. 
### Conversion
fig= plt.figure(figsize=(8,8))
plt.grid(False)
plt.axis([0, image.shape[1], 0, image.shape[0]])
##inverse the y-axis
### get current axis (gca)
ax= plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.scatter(x, y, marker='*')

"""## Above is for only one person.
## Looping the humans and process for all the persons.
"""

co_ordinates=[]
for person in humans:
  bodyparts= getattr(person, 'body_parts')
  ## Looparound body parts and get the co-ordinates
  for part in bodyparts.keys():
    axis=[]
    x= getattr(bodyparts[part], 'x')
    y= getattr(bodyparts[part], 'y')
    axis.append(x)
    axis.append(y)
    ##Append x and y axis into co-ordinates
    co_ordinates.append(axis)

### Convert co-ordinates to array and multiply with image shape
### The result of co-ordinates came with width and height so, multiplication happens with image shape accordingly
array_co_ordinates= np.array(co_ordinates)
array_co_ordinates= array_co_ordinates * (image.shape[1], image.shape[0])
### Split to co-ordinates
x, y= zip(*array_co_ordinates)

### Create plot graph
fig= plt.figure(figsize=(8,8))
plt.grid(True)
plt.axis([0, image.shape[1], 0, image.shape[0]])
## invert y-axis
ax= plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.scatter(x, y, marker='*')



