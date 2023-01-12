import cv2
import numpy as np
import datetime
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import sys
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")

colorinfo = config_object["COLORINFO"]

image_source = ""
if len(sys.argv) == 2:
    image_source = sys.argv[1]
else:
    image_source = ''

def get_bitwise (img, lower, higher, height_lower, height_higher, width_lower, width_higher):
    """Let a certain color of the image stand out.

    Args:
      img: A openCV image.
      lower: The lower HSV bound of the color.
      higher: The higher HSV bound of the color.
      height_lower: The lower bound of the height, above which pixels are considered. It is used to limit the whereabouts of the standards.
      height_higher: The higher bound of the height, below which pixels are considered. It is used to limit the whereabouts of the standards.
      width_lower: The lower bound of the width, above which pixels are considered. It is used to limit the whereabouts of the standards.
      width_higher: The higher bound of the width, below which pixels are considered. It is used to limit the whereabouts of the standards.

    Returns:
      The image in numpy array format with the color of interest.

    """
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, higher)

    result = cv2.bitwise_and(img, img, mask = mask)

    ## limit the whereabouts of the standards
    for h in range(result.shape[0]):
        if h > height_lower and h < height_higher:
            for w in range(result.shape[1]):
                if w > width_lower and w < width_higher:
                    pass
                else:
                    result[h, w, :] = 0
        else:
            result[h, :, :] = 0

    return result

#### Either use the webcamera to capture.
if image_source == "":
    camera = cv2.VideoCapture(0)
    ret, img = camera.read()
    camera.release()

#### or use a static picture
else:
    img = cv2.imread(image_source)

current_time = str(datetime.datetime.now()).replace(":", "_").replace(".", "_")

cv2.imwrite(f"processed_img/{current_time}_original.png", img)
## Read


## slice the green
green = get_bitwise(img, (int(colorinfo["GREEN_HMin"]), int(colorinfo["GREEN_SMin"]), int(colorinfo["GREEN_VMin"])), (int(colorinfo["GREEN_HMax"]), int(colorinfo["GREEN_SMax"]), int(colorinfo["GREEN_VMax"])), 0, 480, 0, 640)
cv2.imwrite(f"processed_img/{current_time}_green.png", green)
green_mask = green > 0
green_pixels = np.count_nonzero(green_mask)
## save 


## do the same for white and red standards
white = get_bitwise(img, (int(colorinfo["WHITE_HMin"]), int(colorinfo["WHITE_SMin"]), int(colorinfo["WHITE_VMin"])), (int(colorinfo["WHITE_HMax"]), int(colorinfo["WHITE_SMax"]), int(colorinfo["WHITE_VMax"])), 400, 480, 200, 400)
cv2.imwrite(f"processed_img/{current_time}_white.png", white)
white_mask = white > 0
white_pixels = np.count_nonzero(white_mask)



red = get_bitwise(img,  (int(colorinfo["RED_HMin"]), int(colorinfo["RED_SMin"]), int(colorinfo["RED_VMin"])), (int(colorinfo["RED_HMax"]), int(colorinfo["RED_SMax"]), int(colorinfo["RED_VMax"])), 400, 480, 150, 320)
cv2.imwrite(f"processed_img/{current_time}_red.png", red)
red_mask = red > 0
red_pixels = np.count_nonzero(red_mask)


pixel_density_for_1_square_cm = (white_pixels + red_pixels)/2

green_area = green_pixels/pixel_density_for_1_square_cm


awsinfo = config_object["USERINFO"]

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC
ENDPOINT = awsinfo["ENDPOINT"]
CLIENT_ID = awsinfo["CLIENT_ID"]
PATH_TO_CERTIFICATE = awsinfo["PATH_TO_CERTIFICATE"]
PATH_TO_PRIVATE_KEY = awsinfo["PATH_TO_PRIVATE_KEY"]
PATH_TO_AMAZON_ROOT_CA_1 = awsinfo["PATH_TO_AMAZON_ROOT_CA_1"]

TOPIC = f'device/{awsinfo["DEVICE_ID"]}/data'

MESSAGE = {"green_area": green_area}

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTClient.connect()
print('Begin Publish')


myAWSIoTMQTTClient.publish(TOPIC, json.dumps(MESSAGE), 1) 
print("Published: '" + json.dumps(MESSAGE) + "' to the topic: " + f"{TOPIC}")

print('Publish End')
myAWSIoTMQTTClient.disconnect()