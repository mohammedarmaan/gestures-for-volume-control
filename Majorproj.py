import cv2
#import mediapipe library
import mediapipe as mp
import math
import numpy

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#print("Get Mute" ,volume.GetMute())   #return 0 if not mute and 1 if system is mute
#print(volume.GetMasterVolumeLevel())
#print(volume.GetVolumeRange())
#volume.SetMasterVolumeLevel(-20.0, None)

#creating objects(copy-paste)
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


#To capture video 
cap = cv2.VideoCapture(0)
#To keep on updating the variable values
while True:
    #To read image from camera
    success , img = cap.read()
    #To show the captured image on screen
    cv2.imshow("Image", img)
    #Converted the image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    
    results = hands.process(img)
    #if palm is present
    if results.multi_hand_landmarks:  
        #It'll execute for all the hands  
        for handLms in results.multi_hand_landmarks:
            
            #To store the co-ordinates of the landmarks
            lmList = []
            
            #print(handLms.landmark)
            #id would range from 0 to 20
            #lm would have 3 values  x, y, z
            for id, lm in enumerate(handLms.landmark):
                
                h, w, c = img.shape
                #co-ordinates of landmarks
                cx, cy = int(lm.x*w) , int(lm.y*h)
                
                lmList.append([id, cx, cy])
                #print(id, lm)
            
            #mp_drawing.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            #print("Hi")
            #print(lmList)
            if lmList:
                #co-ordinates of thumb
                x1, y1 =lmList[4][1], lmList[4][2]
                #co-ordinates of for-finger
                x2, y2 = lmList[8][1], lmList[8][2]
                #circle around thumb
                #print(x1, y1)
                cv2.circle(img, (x1,y1) , 15 , (3,24,52) ,4 )
                length = math.hypot(x2-x1, y2-y1)
                #print(length)
            volRange = volume.GetVolumeRange()
            minVol = volRange[0]
            maxVol = volRange[1]
            vol = numpy.interp(length, [50,300], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)
    
                
#length = 50 to 300
#when length is 50, vol be zero
#when length i 300,  vol be 100
                
        
#System volume = 0 to 100
#Library volume = -65.25 to 0.0


#when my system volume is 0, library volume = -65.25
#When my system volume is 100 , library volumen = 0.0 
#When my system volume is 40, library volume = 
    
    
    cv2.waitKey(100)