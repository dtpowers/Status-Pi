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
    camera.resolution = (2592, 1944)
    print("Server initialized...")
    shutdown = input("If you want to take a status press anything other than q. To shutdown, press q")
    while shutdown != 'q':
        takeStatus()
        shutdown = input("If you want to take a status press anything other than q. To shutdown, press q")
    #shutdown server
    shutdownServer()
    
        
def shutdownServer():
    print("Shutting down...")
    saveDB()
    quit()

def takeStatus():
    #increase count and generate new entry
    global mostRecentStatusID
    mostRecentStatusID += 1
    #populate with data
    metrics = getMetrics()
    time = datetime.datetime.now()
    metrics['Time'] = time.strftime("%A, %B %-d %Y, %-I:%M %p")
    

    #take picture, upload, get picture name
    print("Say cheese!")
    imageName = takePicture()
    metrics['image'] = imageName
    #Add status to db, and write db to disk
    DATABASE[mostRecentStatusID] = metrics
    saveDB()
    print("status added and uploaded!")


#ask user for key/value pairs for metrics
def getMetrics():
    metrics = {}
    doBase = input("do you want default metrics y/n")
    if (doBase != "n" and doBase != "q"):
        weight = input("Current weight?")
        sleep = input("how many hours of sleep did you get?")
        metrics['weight'] = weight    
        metrics['sleep'] = sleep

    nextMetric = input("Do you want to add any additional metrics? y/n")
    while (nextMetric != "q" and nextMetric != "n"):
        key = input("Please enter metric Key")
        if key == "q":
            return metrics
        value = input("Please enter value for " + key)
        if value == "q":
            return metrics
        metrics[key] = value
        nextMetric = input("Continue? y/n/q")
    return metrics




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

