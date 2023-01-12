import cv2
import numpy as np

def get_pixels (img, lower, higher):
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, higher)
    bmask = mask > 0
    color_pic = np.zeros_like(img, np.uint8)
    color_pic[bmask] = img[bmask]

    return color_pic, bmask



## Read
img = cv2.imread("red_16.jpg")



## slice the green
green, green_mask = get_pixels(img, (37, 32, 79), (80, 255,255))
print ("green", np.count_nonzero(green_mask))
## save 


white, white_mask = get_pixels(img, (100,45,182), (111,255,255))
print ("white", np.count_nonzero(white_mask))



red, red_mask = get_pixels(img, (0,89,0), (179,255,255))
print ("red", np.count_nonzero(red_mask))

