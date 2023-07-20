import mediapipe as mp
import cv2
import cvzone
import numpy as np
import uuid
import os
from pynput.keyboard import Key, Controller
from cvzone.HandTrackingModule import HandDetector

W1=cv2.imread("wheel1.png",cv2.IMREAD_UNCHANGED)
W1=cv2.resize(W1,(280,280))
W1=cvzone.rotateImage(W1,45)

keyboard=Controller()

cap=cv2.VideoCapture(1)
cap.set(3,900)
cap.set(4,820)
detector=HandDetector(detectionCon=0.8,maxHands=1)
flag=True
while True:
    _,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)

    if hands:
       hand=hands[0]['lmList']
       arm1=hand[8]
       arm2=hand[5]
       org=hand[0]
       radians=np.arctan2(org[1]-arm2[1],org[0]-arm2[0])-np.arctan2(arm1[1] - arm2[1], arm1[0] - arm2[0])
       angle=round(np.abs(radians*180/np.pi),2)
       cvzone.putTextRect(img,f'{angle}',(org[1]+10,org[0]+10),1,2)
       
       if angle<=180 and flag==True:
         W1=cvzone.rotateImage(W1,-90)
         flag=False
       elif angle>180 and flag==False:
         W1=cvzone.rotateImage(W1,90)
         flag=True
       
       if angle<=180:
         keyboard.press(Key.right)
         keyboard.release(Key.right)
       else :
         keyboard.press(Key.left)
         keyboard.release(Key.left)
      
    img=cvzone.overlayPNG(img,W1,[180,200])
    
    cv2.imshow('Hand Tracking', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
     break