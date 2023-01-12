# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC
ENDPOINT = "a1diza7g7cdhlr-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "basicPubSub"
PATH_TO_CERTIFICATE = "./aws_key/pi_capture.cert.pem"
PATH_TO_PRIVATE_KEY = "./aws_key/pi_capture.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./aws_key/root-CA.crt"
MESSAGE = {"green_area":150}
TOPIC = "device/5/data"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTClient.connect()
print('Begin Publish')


myAWSIoTMQTTClient.publish(TOPIC, json.dumps(MESSAGE), 1) 
print("Published: '" + json.dumps(MESSAGE) + "' to the topic: " + f"{TOPIC}")

print('Publish End')
myAWSIoTMQTTClient.disconnect()