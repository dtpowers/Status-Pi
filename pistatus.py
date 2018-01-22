from picamera import PiCamera
from time import sleep
import boto3




def init():
	print("initializing PiCam.")
	global camera
	global s3
	#initialize camera object
	camera = PiCamera()
	#initialize and connect to AWS
	s3 = boto3.resource('s3')
	takePicture('test')


def takePicture(name):
	camera.start_preview()
	sleep(5)
	camera.capture('pics/' + name + '.png')
	#upload to AWS instead of writing to file
	s3.Bucket('my-bucket').put_object(Key=(name + '.png'), Body=data)
	camera.stop_preview()
	print ('took picture')


def uploadPhotoAWS(buffer)











init()
