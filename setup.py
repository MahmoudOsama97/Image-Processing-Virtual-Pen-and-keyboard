import cv2
import numpy as np
import time




# NULL operation
def NOP(x):
    pass

# Create CAM object
cap = cv2.VideoCapture(0)


# the window 
cv2.namedWindow("SETUP")

# Create 6 trackbars for the HSV ranges
cv2.createTrackbar("Lower - H", "SETUP", 0, 179, NOP)
cv2.createTrackbar("Upper - H", "SETUP", 179, 179, NOP)
cv2.createTrackbar("Lower - S", "SETUP", 0, 255, NOP)
cv2.createTrackbar("Upper - S", "SETUP", 255, 255, NOP)
cv2.createTrackbar("Lower - V", "SETUP", 0, 255, NOP)
cv2.createTrackbar("Upper - V", "SETUP", 255, 255, NOP)
 
 
while True:
    
    # take frame from cam
    r, frame = cap.read()
    if not r:
        break
    # mirror the frame 
    frame = cv2.flip( frame, 1 ) 
    
    #  BGR to HSV as we are using HSV system
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # take readings from the trackbars for hsv
    lower_h = cv2.getTrackbarPos("Lower - H", "SETUP")
    upper_h = cv2.getTrackbarPos("Upper - H", "SETUP")
    lower_s = cv2.getTrackbarPos("Lower - S", "SETUP")
    upper_s = cv2.getTrackbarPos("Upper - S", "SETUP")
    lower_v = cv2.getTrackbarPos("Lower - V", "SETUP")
    upper_v = cv2.getTrackbarPos("Upper - V", "SETUP")
 
    # define the mask ranges 
    l_r = np.array([lower_h, lower_s, lower_v])
    u_r = np.array([upper_h, upper_s, upper_v])
    
    # use the ranges to define the mask
    mask = cv2.inRange(hsv, l_r, u_r)
 
    # apply the mask
    res = cv2.bitwise_and(frame, frame, mask=mask)
      
    # put the two frames together
    stacked = np.hstack((frame,res))
    
    # show the frames
    cv2.imshow('SETUP',cv2.resize(stacked,None,fx=0.8,fy=0.8))
    
    # break if ESC
    key = cv2.waitKey(1)
    if key == 27:
        break
    
    # save if s
    if key == ord('s'):
        
        thearray = [[lower_h,lower_s,lower_v],[upper_h, upper_s,upper_v]]
        print(thearray)
        
        # Also save this array as penval.npy
        np.save('setupObject',thearray)
        break
    
# Close.    
cap.release()
cv2.destroyAllWindows()