from picamera import PiCamera
from time import sleep
import boto3
import datetime
import io
import json
import pprint




def init():
	print("initializing PiCam.")
	global camera
	global mostRecentStatusID
	global DATABASE
    global pp
    pp = pprint.PrettyPrinter(indent=4)
    DATABASE = loadDB()
    mostRecentStatusID = len(DATABASE)
    print('Previous Status #: ' + str(mostRecentStatusID))
	#initialize camera object
	camera = PiCamera()
	print("Server initialized...")
	takePicture()


#takes pictures, returns aws key for file
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
	s3 = boto3.resource('s3')
	s3.Bucket('pistatus').put_object(Key=(name), Body=data)
	print ('uploaded picture: ' + name)
	return name




def generateFilename():
	time = datetime.datetime.now()
	return str(mostRecentStatusID) + '.' + time.strftime("%Y-%m-%d.%H.%M.%S") 



##################SERVER LOGIC

def serverInit():
    

def shutdownServer():
    saveDB()


def recStatus(status):
    prevStatus += 1
    DATABASE = status


def getLastStatus():
    status = DATABASE[str(prevStatus)]
    return status
    

def getStatus(id):
    return DATABASE[id]

##########################DB OPERATIONS#################################


#read database from disk into memory
def loadDB():
    print('Loading Database...')
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket='pistatus', Key='data.json')
    database = json.loads(response['Body'].read().decode("UTF-8"))
    pp.pprint(database)
    DATABASE = database
    print('Finished Loading ')
    return database


#write db from memory to disk
def saveDB():
    buf = json.dumps(DATABASE).encode('UTF-8')
    s3 = boto3.resource('s3')
    s3.Bucket('pistatus').put_object(Key='data.json', Body=buf)
    print('Wrote DB to disk...')



############################################## tests






init()
loadDB()
sleep(5)
shutdownServer()
