from picamera import PiCamera
from time import sleep
import boto3
import datetime
import io




def init():
	print("initializing PiCam.")
	global camera
	global s3
	global mostRecentStatusID
	mostRecentStatusID = 1
	#initialize camera object
	camera = PiCamera()
	#initialize and connect to AWS
	s3 = boto3.resource('s3')
	takePicture()
	#get most recent server info
	update()


def takePicture():
	#initialize buffer
	data = io.BytesIO()
	camera.start_preview()
	sleep(5)
	camera.capture(data, 'png')
	name = generateFilename() + ".png"
	camera.stop_preview()
	print ('took picture')
	#upload to AWS
	data.seek(0)
	s3.Bucket('pistatus').put_object(Key=(name), Body=data)
	print ('uploaded picture: ' + name)
	#update webserver
	#submitStatus()



def generateFilename():
	time = datetime.datetime.now()
	return str(mostRecentStatusID) + '.' + time.strftime("%Y-%m-%d.%H.%M.%S") 



#query server to get most recent values
#mostRecentStatus
def update():
	return 1

def submitStatus():
	return 1





init()
