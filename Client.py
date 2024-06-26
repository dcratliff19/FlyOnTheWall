import sys
import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import asyncio
import websocket
import pickle
from websocket import create_connection
import timeit 
from logo import LOGO
from dotenv import load_dotenv
import os

load_dotenv()

FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2

CHUNK = int(os.getenv('CHUNK'))
RATE = int(os.getenv('RATE'))
RECORD_SECONDS = int(os.getenv('RECORD_SECONDS'))
REMOTE_SERVER = "ws://" + os.getenv('SERVER') + ":" + os.getenv('PORT') + "/"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=1, rate=RATE, input=True)

def get_record():

    all = bytes()
    for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
        ##wf.writeframes(stream.read(CHUNK))
        all += stream.read(CHUNK)
        
    return all


#Fly Away!
if __name__ == "__main__":

  #Print the logo and details to connect.
  print(LOGO)
  print("-- Audio Transmission Client Started --")
  print("REMOTE SERVER:", REMOTE_SERVER)
  try:
     
    ws = create_connection(REMOTE_SERVER)

  except:
     print("Cannot establish connection to server.")
     exit(0)

  try:
    #print("Please login")
    #username = input("Device ID: ")
    #api_key = input("API Key: ")
  
    ws.send("0:password")
    status = ws.recv()
  
    if int(status) == 1:

      print("Login Successful")
      print('##-- Starting Recording/Transmission --##')
      print('- Remote Server:', REMOTE_SERVER)
      print('- Transmission Interval (seconds):', RECORD_SECONDS, "seconds")
      
      #Fire away!
      input("Press enter key to begin.")
      
      while True:
          
          audio = pickle.dumps(get_record())
          print("## Audio Transmission Start ##")
          #Start of send timer.
          tic = timeit.default_timer()
          ws.send(audio, opcode=websocket.ABNF.OPCODE_BINARY)
          #end timer
          toc=timeit.default_timer()
          print("- Transmission Status:", ws.recv())
            # Do Stuff
          print("- Transmission Time:",toc - tic)
          print("## Audio Transmission End ##")
      
  except KeyboardInterrupt:
    print(' -- Ending Recording/Transmission -- ')
    ws.close()
  


