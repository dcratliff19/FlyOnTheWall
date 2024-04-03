import mediapipe as mp
import numpy as np
import asyncio
import websockets
import numpy as np
import pickle
from math import log10
import time
import audioop
from logo import LOGO
import mysql.connector

cnx = mysql.connector.connect(user='root', password='password', host='127.0.0.1', database='sound')
mycursor = cnx.cursor()

SERVER = "localhost"
PORT = 5000
#Device ID 
current_user = 0
DEVICE_MASTER = [{"device_id": 0, "password": "password"}, {"device_id": 1, "password": "password"}]

def calculate_decibel(audio):

    rms = audioop.rms(audio, 1) / 32767
    db = 20 * log10(rms)

    return db

def create_record(audio, class_result_list):
    
    insert_values = [audio]
   
    class_list = []
    class_percent = []

    #collect data we need. 
    for result in class_result_list:

        class_list.append(result.category_name)
        class_percent.append(result.score)

    sql = """INSERT INTO raw_sounds (raw_audio_bytes, 
                                    class_1, 
                                    class_2, 
                                    class_3, 
                                    class_4, 
                                    class_5, 
                                    class_1_percent, 
                                    class_2_percent, 
                                    class_3_percent, 
                                    class_4_percent, 
                                    class_5_percent, 
                                    decibel_reading, 
                                    record_datetime,
                                    device_id) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    #Add the class list to the insert value array.
    insert_values += class_list
    #Add the percentages to the insert value array
    insert_values += class_percent
    #Calculate the decibel level
    db = calculate_decibel(audio)
    #add it to the insert array
    insert_values.append(db)

    ##Add the logging info.
    insert_values.append(time.strftime('%Y-%m-%d %H:%M:%S'))
    insert_values.append(current_user)

    try:
        #Insert the data
        mycursor.execute(sql, insert_values)
        cnx.commit()
        return True
    
    except Exception as e:
        print(e)
        return False


def login(username, password):
    if not any(x['device_id'] == username for x in DEVICE_MASTER) and not any(x['password'] == password for x in DEVICE_MASTER):
        print("Client login failed:", username)
        return False
        
    else:
        current_user = username
        print("Client connected:", username)
        return True

# create handler for each connection
async def handler(websocket):

    ##Create the classifier.
    AudioClassifier = mp.tasks.audio.AudioClassifier
    AudioClassifierOptions = mp.tasks.audio.AudioClassifierOptions
    AudioRunningMode = mp.tasks.audio.RunningMode
    BaseOptions = mp.tasks.BaseOptions
    AudioData = mp.tasks.components.containers.AudioData
    #classifier
    options = AudioClassifierOptions(
        base_options=BaseOptions(model_asset_path='soundModel.tflite'),
        max_results=5,
        running_mode=AudioRunningMode.AUDIO_CLIPS)

    #One big try except. This isn't commerical grade.
    try:
        #Grab the client IP
        client_ip = websocket.remote_address
        print("-- NEW CLIENT CONNECTION FROM " + str(client_ip))
        ##Get the username password
        results = await websocket.recv()
        username, password = results.split(":")
        #Try login
        if login(username, password):  
            await websocket.send("1")
        else:
            await websocket.send("0")
            return
        #Loop it. We don't care if it crashes,
        #no money or customers on the line here.
        while True:
                #Get the websocket data
                data = await websocket.recv()
                #Send a success message
                await websocket.send("Success")
                print("-- NEW AUDIO RECIEVED --")
                #Load the data from the pickle object
                audio_buffer = pickle.loads(data)
                #Convert to numpy array
                numpydata = np.frombuffer(audio_buffer, dtype=np.int16)
                #Create the classifier from the options above
                with AudioClassifier.create_from_options(options) as classifier:
                    #Convert to the proper AudioData type.
                    audio_data = AudioData.create_from_array(numpydata.astype(float) / np.iinfo(np.int16).max, 44100)
                    #CLASSIFY!
                    audio_classifier_result_list = classifier.classify(audio_data)
                    #Process and save the results.
                    results = audio_classifier_result_list[0].classifications[0].categories
                    create_record(audio_buffer, results)
                    print("Results:")
                    for result in results:

                        print(result.category_name, str(result.score * 100) + '%')
                                    
                    print("-- END AUDIO --")
            
    except Exception as e:
        print(e)
        print("Client disconnected:", str(client_ip))

        return

#Fly Away!
if __name__ == "__main__":

    #Print the logo and details to connect.
    print(LOGO)
    print("-- Audio Processing Server Started --")
    print("IP:", SERVER)
    print("PORT:", PORT)

    start_server = websockets.serve(handler, SERVER, PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
