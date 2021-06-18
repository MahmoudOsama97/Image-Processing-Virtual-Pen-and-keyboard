import cv2
import numpy as np
import time

def canvas():
    load = True
    if load:
        penval = np.load('setupObject.npy')

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    kernel = np.ones((5,5),np.uint8)

    # Initializing the plane on which we will draw upon
    plane = None

    # Initilize x1,y1 points
    x1,y1=0,0

    # Threshold for noise
    noiseThreshold = 800

    while(1):
        _, frame = cap.read()
        frame = cv2.flip( frame, 1 )
        
        # Initialize the plane as a black image of the same size as the frame.
        if plane is None:

            #plane = cv2.resize(cv2.imread('c://Users//osama//Desktop//image//pen.jpg',1), (1280, 720))

            plane = np.zeros_like(frame)
            plane[np.where((plane==[0,0,0]).all(axis=2))] = [0,128,128]


        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #In case of loading the upper and lower ranges from memory
        if load:
            lowerRange = penval[0]
            upperRange = penval[1]
                
        #Otherwise define your own values
        else:             
            lowerRange  = np.array([26,80,147])
            upperRange = np.array([81,255,255])
        
        mask = cv2.inRange(hsv, lowerRange, upperRange)
        
        #get rid of the noise by performing morphological operations
        mask = cv2.erode(mask,kernel,iterations = 1)
        mask = cv2.dilate(mask,kernel,iterations = 2)
        
        # Find Contours
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #check that contour is bigger than noise threshold
        if contours and cv2.contourArea(max(contours, 
                                    key = cv2.contourArea)) > noiseThreshold:
                    
            bound = max(contours, key = cv2.contourArea)    
            x2,y2,w,h = cv2.boundingRect(bound)
            
            # If no earlier points were found, save the detected x2,y2 coordinates as  x1,y1 
            # # This happens when writing for the first time or when writing again when the pen had disappeared from view.
            if x1 == 0 and y1 == 0:
                x1,y1= x2,y2
                
            else:
        
                plane = cv2.line(plane, (x1,y1),(x2,y2), [128,128,0], 4)
            
            #the new points become the previous points.
            x1,y1= x2,y2

        else:

            #if no contours decteced then x1,y1=0
            x1,y1 =0,0
        
        cv2.imshow('Trackbars',cv2.resize(plane,None,fx=0.6,fy=0.6))

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
            # press 'p' to print this array
        if k == ord('p'):
            print(type(plane))
            cv2.imwrite('./save//EI.jpg',plane)
            break
        # When c is pressed clear the plane
        if k == ord('c'):
            plane = None

    cv2.destroyAllWindows()
    cap.release()