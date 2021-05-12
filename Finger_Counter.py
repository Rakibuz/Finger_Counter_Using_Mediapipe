import cv2
import mediapipe as mp
import time
import os


pTime=0
cTime=0
wCam, hCam = 640,480
cap=cv2.VideoCapture(1)
cap.set(3,wCam)
cap.set(4,hCam)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw= mp.solutions.drawing_utils

tipIds= [4,8,12,16,20]

folderPath="/Users/User/Finger_New"
myList= os.listdir(folderPath)
 
folderPath_new="/Users/User/Finger"
myList_new= os.listdir(folderPath_new)

Image_List=[]
Image_List_new=[]

for imPath in myList:
    image= cv2.imread(f'{folderPath}/{imPath}')
    Image_List.append(image)

for imPath_new in myList_new:
    image_new= cv2.imread(f'{folderPath_new}/{imPath_new}')
    Image_List_new.append(image_new)

def Hand_Finder(img,draw=True):
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
    return img

def Finger_Detector(img,handNo=0,draw=True):
    landmark_List=[]
    if results.multi_hand_landmarks:
        myHand=results.multi_hand_landmarks[handNo]

        for id, lm in enumerate(myHand.landmark):
            h,w,c =img.shape
            cx,cy =int(lm.x*w),int(lm.y*h)
            landmark_List.append([id,cx,cy])
            if draw:
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
    return landmark_List



while(cap.isOpened()):
    success, img = cap.read()

    #convert the image BGR2RGB
    converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(converted_image)

    #Calling the hand finder 
    # pass captured img and results
    img=Hand_Finder(img)
    #Calling Finger Detector
    #pass captured img and results
    landmark_List=Finger_Detector(img,draw=False)
    #print(lmList)

    if len(landmark_List)!=0:
        fingers=[]
        # Thumb
        if landmark_List[tipIds[0]][1]> landmark_List[tipIds[0]-1][1]:
            #print('Index finger open')
            fingers.append(1)
        else:
            fingers.append(0)

        #4 Fingers
        for id in range(1,5):
            if landmark_List[tipIds[id]][2]< landmark_List[tipIds[id]-2][2]:
                # actually lmList[landmark id][value of  x or y]
                # as for those four finger up and down is counting thats why y is in concern
                # -2 for checking 2 landmark position down
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers= fingers.count(1)  
        #print(totalFingers)
        #print(fingers)

        if(fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):
            #print('Index or one')
            img[0:200,0:200]=Image_List[0]
        elif(fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0):
            #print('TWO')
            img[0:200,0:200]=Image_List[1]
        elif(fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0):
            #print('Three')
            img[0:200,0:200]=Image_List[2]
        elif(fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1):
            #print('Four')
            img[0:200,0:200]=Image_List[3]
        elif(fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1):
            #print('Five')
            img[0:200,0:200]=Image_List[4]
        elif(fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):
            #print('Zero')
            img[0:200,0:200]=Image_List[5]   
        elif(fingers[1]==1 and fingers[4]==1 and fingers[2]==0 and fingers[3]==0 and fingers[0]==0):
            #print('Rock')
            img[0:200,0:200]=Image_List[6]
        elif(fingers[0]==0 and fingers[1]==0 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0):
            #print('Middle Finger')
            img[0:200,0:200]=Image_List[7]
        elif(fingers[0]==1 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):
            #print('Thumbs up')
            img[0:200,0:200]=Image_List[8]

        ############################new Image List#######################################
        elif(fingers[0]==1 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1):
        #print('Telephne')
            img[0:200,0:200]=Image_List_new[1]
        elif(fingers[0]==1 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0):
        #print('Smile')
            img[0:200,0:200]=Image_List_new[0]
        elif(fingers[0]==0 and fingers[1]==0 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1):
        #print('Ok')
            img[0:200,0:200]=Image_List_new[3]
        elif(fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1):
        #print('Wash Room')
            img[0:200,0:200]=Image_List_new[2]
         
        
        #Finger Counter Showing
        cv2.rectangle(img, (20,225), (170,425), (0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25) 

    
    #Frame Rate calculations
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(450,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    #Showing the window
    cv2.imshow("Hand Tracking",img)

    if cv2.waitKey(1)==113:
        break
 