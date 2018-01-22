from picamera import PiCamera
from time import sleep




def init():
	print("initializing PiCam.")
	global camera
	camera = PiCamera()
	takePicture('test')


def takePicture(name):
	camera.start_preview()
	sleep(5)
	camera.capture('pics/' + name + '.png')
	camera.stop_preview()
	print ('took picture')













init()
