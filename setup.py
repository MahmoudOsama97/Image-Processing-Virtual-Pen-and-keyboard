import cv2
import numpy as np
import time

# NULL operation
def NOP(x):
    pass
def setup():
    # Capture CAM object
    cap = cv2.VideoCapture(0)
    
    cv2.namedWindow("SETUP")

    #6 trackbars for HSV ranges
    cv2.createTrackbar("Lower - H", "SETUP", 0, 179, NOP)
    cv2.createTrackbar("Upper - H", "SETUP", 179, 179, NOP)
    cv2.createTrackbar("Lower - S", "SETUP", 0, 255, NOP)
    cv2.createTrackbar("Upper - S", "SETUP", 255, 255, NOP)
    cv2.createTrackbar("Lower - V", "SETUP", 0, 255, NOP)
    cv2.createTrackbar("Upper - V", "SETUP", 255, 255, NOP)
    
    while True:
    
        r, frame = cap.read()
        if not r:
            break
        # flip the frame 
        frame = cv2.flip( frame, 1 ) 
        
        # change BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #Readings from the trackbars 
        lowerH = cv2.getTrackbarPos("Lower - H", "SETUP")
        upperH = cv2.getTrackbarPos("Upper - H", "SETUP")
        lowerS = cv2.getTrackbarPos("Lower - S", "SETUP")
        upperS = cv2.getTrackbarPos("Upper - S", "SETUP")
        lowerV = cv2.getTrackbarPos("Lower - V", "SETUP")
        upperV = cv2.getTrackbarPos("Upper - V", "SETUP")
    
        # mask ranges 
        l_r = np.array([lowerH, lowerS, lowerV])
        u_r = np.array([upperH, upperS, upperV])
        
        #using lower and upper range to define mask
        mask = cv2.inRange(hsv, l_r, u_r)
    
        # apply the mask
        res = cv2.bitwise_and(frame, frame, mask=mask)
        
        # stack the two frames together
        stacked = np.hstack((frame,res))
        
        cv2.imshow('SETUP',cv2.resize(stacked,None,fx=0.8,fy=0.8))
        
        #if ESC is pushed then break
        key = cv2.waitKey(1)
        if key == 27:
            break
        
        # if 's' is pushed then save
        if key == ord('s'):
            
            thearray = [[lowerH,lowerS,lowerV],[upperH, upperS,upperV]]
            print(thearray)
 
            np.save('setupObject',thearray)
            break
           
    cap.release()
    cv2.destroyAllWindows()