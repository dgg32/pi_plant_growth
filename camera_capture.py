# import the opencv library
import cv2


# define a video capture object
camera = cv2.VideoCapture(0)
ret, image = camera.read()

camera.release()

cv2.imwrite("capture.png", image)
