#======================================#
# Virtual Keyboard with Color Tracking #
#  using Python and OpenCV library     #
#--------------------------------------#
#        Konstantinos Thanos           #
#         Mathematician,MSc            #
#               2020                   #
#======================================#

# Import packages
import cv2
import numpy as np
import math
import pyglet

from print_message import *

load_from_disk = True
if load_from_disk:
    penval = np.load('penval.npy')


# Set beep sound from wav file
sound = pyglet.media.load("c://Users//osama//Desktop//Virtual-on-screen-keyboard-main//beep.wav", streaming=False)

# Video Capture
cap = cv2.VideoCapture(0)

# Capture and save the very first frame
_, video = cap.read()
video = cv2.resize(video, (1280,720)) # Resize video capture to desired dimensions

# Set width and height for rectangle (key) size
width, height = 65, 65
# Set distance between two consecutive rectangles
dist = 15

# Initial position of text in frame
start_x = int((video.shape[1] - (10*width + 9*dist))/2)
start_y = 50

# Text settings
font = cv2.FONT_HERSHEY_PLAIN  # Font
fontThickness = 4              # Font weight
fontScale = 4                  # Font scale

# Strings used in basic-'command' buttons
symbol_strings = ["BACK", "DELETE", "ENTER", "Aa", "SPACE", "NUM2SYM"]    

# Set a string with letters, numbers and symbols
numbers = "1234567890" # String containing 10 numbers (0-9)
alphabet = "1234567890QWERTYUIOP:ASDFGHJKL?ZXCVBNM,.<->[_]"
#                    !          !         !        !
# position          10          21        31       40   45
letters = "1234567890QWERTYUIOP:ASDFGHJKL?ZXCVBNM,.<->[_]"
alpha_len = len(alphabet)

symbols = "!@#$%^&*()"
# Meaning of extra symbols :
#==============================================
#              Delete one character (BACK) : <
#                      Delete all (DELETE) : -
#                Newline character (ENTER) : >
#   Change between capitals/lowercase (Aa) : [ 
#        Leave one character empty (SPACE) : _
# Change between numbers/symbols (NUM2SYM) : ]

# Function for drawing rectangles and set(draw) character(text) inside them
def draw_letters(let_index, text):
    width, height = 65,65
    for i in range(alpha_len):
        if i < 10:
            if let_index == i:
                x, y = start_x + i*(width + dist), start_y
        elif i >= 10 and i < 21:
            if let_index == i:
                x, y = start_x - int(start_x/1.5) + (i-10)*(width + dist), start_y + (height + dist)
        elif i >= 21 and i < 31:
            if let_index == i:
                x, y = start_x + (i-21)*(width + dist), start_y + 2*(height + dist) 
        elif i >= 31 and i < 40:
            if let_index == i:
                x, y = 2*start_x + (i-31)*(width + dist), start_y + 3*(height + dist)
        elif i==40:
            if let_index == i:
                x, y = start_x - 3*dist, start_y + 4*(height + int(1.5*dist))
                width += 30
        elif i==41:
            if let_index == i:
                x, y = start_x, start_y + 5*(height + int(1.5*dist))
                width += 70
        elif i==42:
            if let_index == i:
                x, y = start_x + 11*width - dist, start_y + 4*(height + int(1.5*dist))
                width += 50
        elif i==43:
            if let_index == i:
                x, y = start_x + 11*width + int(dist/2), start_y + 5*(height + int(1.5*dist))
        elif i==44:
            if let_index == i:
                x, y = start_x + 5*width, start_y + 4*(height + int(1.5*dist))
                width += 200
        elif i==45:
            if let_index == i:
                x, y = start_x + 3*width - int(width/2), start_y + 4*(height + int(1.5*dist))
                width += 80

    cv2.rectangle(frame, (x, y), (x + width, y + height), (255), 2)

    # Find the size of each character based on font, font-scale and font-weight
    text_size = cv2.getTextSize(text, font, fontScale, fontThickness)
    text_width = text_size[0][0]
    text_height = text_size[0][1]

    # Text position for each character
    text_x = int((width - text_width)/2) + x
    text_y = int((height + text_height)/2) + y

    text_color = (0,255,255)

    # Add text in frame
    if let_index < 10:
        cv2.putText(frame, text, (text_x-10, text_y), font, fontScale, text_color, fontThickness-1)
    elif let_index < alpha_len - 6:
        cv2.putText(frame, text, (text_x, text_y), font, fontScale, text_color, fontThickness-1)
    elif let_index==40:
        cv2.putText(frame, symbol_strings[0], (text_x-18, text_y-5), font, 2, text_color, 3)
    elif let_index==41:
        cv2.putText(frame, symbol_strings[1], (text_x-32, text_y-5), font, 2, text_color, 3)
    elif let_index==42:
        cv2.putText(frame, symbol_strings[2], (text_x-25, text_y-5), font, 2, text_color, 3)
    elif let_index==43:
        cv2.putText(frame, symbol_strings[3], (text_x-13, text_y-5), font, 3, text_color, 3)
    elif let_index==44:
        cv2.putText(frame, symbol_strings[4], (text_x-30, text_y-5), font, 2, text_color, 3)
    elif let_index==45:
        cv2.putText(frame, symbol_strings[5], (text_x-53, text_y-5), font, 1.8, text_color, 3)

# Function to draw the extra symbols(characters) close to numbers of first keys' row
def draw_extra_chars(let_index, text):
    for i in range(len(symbols)):
        if let_index == i:
            x, y = start_x + i*(width + dist), start_y

    # Find the size of each character based on font, font-scale and font-thickness
    text_size = cv2.getTextSize(text, font, fontScale-3, fontThickness-2)    
    # Text position
    text_x = int((width - text_size[0][0])/2) + x + dist
    text_y = int((height + text_size[0][1])/2) + y + int((3*dist)/2)
    # Add text
    cv2.putText(frame, text, (text_x, text_y), font, fontScale-2, (0,0,255), fontThickness-2)


# Create a new frame (black) of size (250x1000) of 3 channels
# This frame will be used to write down our text-message and some notes
paper = np.zeros((250,1000,3), np.uint8)
cv2.namedWindow("Paper")

# Starting position of text in "Paper" frame
start_write_x = 5
start_write_y = 35

# Basic initializations
count_cl = 1
count_ns = 1
my_text = ""
frames = 0
lines = ['']
line_count = 0

while True:
    _, frame = cap.read()
    # Resize and flip original frame
    frame = cv2.resize(frame, (1280,720))
    frame = cv2.flip(frame, 1) # This may not be necessary
    #frame = cv2.flip(frame, 0) # This may not be necessary

    let_index = -1
    frames += 1 # Increase number of frames by one

    # Apply Gaussian Blur on frame
    bframe = cv2.GaussianBlur(frame, (5,5), 5)

    # Apply HSV format
    hsv_frame = cv2.cvtColor(bframe, cv2.COLOR_BGR2HSV)


    # Color settings for Green (this color can be changed to the desired one)
    # Define lower and upper color
    if load_from_disk:
        lower_color = penval[0]
        upper_color = penval[1]
#   lower_color = np.array([74, 192, 0], np.uint8)
#   upper_color = np.array([96, 255, 255], np.uint8)

    # Apply mask on the hsv frame
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Find contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea) # Find the maximum contour each time (on each frame)        
        M = cv2.moments(contour)

        # Draw each contour
        cv2.drawContours(frame, [contour], -1, (0,255,0), 2)

        # Find each contour center
        if int(M["m00"])!=0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 2, (0,0,255), 2) # Draw center of each contour

            # Check if center is inside a letter box per row of rectangles in frame
            if cy > start_y and cy < start_y + height:
                for k in range(10):
                    if cx > start_x + k*(width+dist) and cx < start_x + k*(width+dist) + width:
                        let_index = k
            elif cy > start_y + height + dist and cy < start_y + 2*height + dist:
                for k in range(10, 21):
                    if cx > start_x - int(start_x/1.5) + (k-10)*(width + dist) and cx < start_x - int(start_x/1.5) + (k-10)*(width + dist) + width:
                        let_index = k
            elif cy > start_y + 2*height + 2*dist and cy < start_y + 3*height + 2*dist:
                for k in range(21, 31):
                    if cx > start_x + (k-21)*(width + dist) and cx < start_x + (k-21)*(width + dist) + width:
                        let_index = k
            elif cy > start_y + 3*height + 3*dist and cy < start_y + 4*height + 3*dist:
                for k in range(31, 40):
                    if cx > 2*start_x + (k-31)*(width + dist) and cx < 2*start_x + (k-31)*(width + dist) + width:
                        let_index = k
            elif cy > start_y + 4*height + 6*dist and cy < start_y + 5*height + 6*dist:
                if cx > start_x - 3*dist and cx < start_x - 3*dist + width + 30:
                    let_index = 40
                elif cx > start_x + 11*width - dist and cx < start_x + 11*width - dist + width + 50:
                    let_index = 42
                elif cx > start_x + 5*width and cx < start_x + 5*width + width + 200:
                    let_index = 44
                elif cx > start_x + 3*width - int(width/2) and cx < start_x + 3*width - int(width/2) + width + 80:
                    let_index = 45
            elif cy > start_y + 5*height + 7*dist and cy < start_y + 6*height + 7*dist:
                if cx > start_x and cx < start_x + width + 70:
                    let_index = 41
                elif cx > start_x + 11*width + int(dist/2) and cx < start_x + 11*width + int(dist/2) + width:
                    let_index = 43

    # Initializations
    new_line = False
    let_sound = False

    # Every 20 frames let user to add a new letter-character
    if frames == 20:
        let_sound = True
        frames = 0

    for i in range(alpha_len):
        draw_letters(i, letters[i]) # Use of draw_letters function
        if (let_index == i) and (let_sound is True):
            # Beep sound to know that character has been taken
            sound.play()
            # Operations of the extra symbols-characters
            # Delete one (1) character
            if i == letters.index("<"):
                if line_count >= 1:
                    if len(my_text) == 0:
                        line_count -= 1
                        my_text = lines[line_count] # Go to the previous line
                        start_write_y -= 40
                paper[line_count*30 + 15:, 5:] = (0)
                my_text = my_text[:-1]
            # Leave one empty (space) character
            elif i == letters.index("_"):
                my_text += ' '
            # Erase everything that was written before
            elif i == letters.index("-"):
                line_count = 0
                paper[:] = (0,0,0)
                my_text = ''
                lines = ['']
                start_write_y = 35
            # Go to the next line (newline)
            elif i == letters.index(">"):
                line_count += 1
                new_line = True
                lines.append('')
                my_text = ''
                paper[start_write_y+5:start_write_y+15, :750] = (0)
            # Change between capitals and lower case letters
            elif i == letters.index("["):
                if count_cl%2!=0:
                    letters = alphabet.lower()
                else:
                    letters = alphabet.upper()
                count_cl += 1
            # Change between numbers and extra symbols (first row of rectangles)
            elif i == letters.index("]"):
                if count_ns%2!=0:
                    letters = symbols + letters[10:]
                else:
                    letters = numbers + letters[10:]
                count_ns += 1         
            else:
                my_text += letters[i]

    if count_ns%2!=0:
        for j in range(10):
            draw_extra_chars(j," ")
            draw_extra_chars(j, symbols[j])
    else:
        for j in range(10):
            draw_extra_chars(j, " ")
            draw_extra_chars(j, alphabet[j])

    # Add text to "Paper" frame
    lines[line_count] = my_text
    cv2.putText(paper, lines[line_count], (start_write_x, start_write_y), font, 2, (255,255,255), 1)

    if new_line is True:
        start_write_y += 40 # User select the new line 'button'

    # Text size
    text_size = cv2.getTextSize(my_text, font, 2, 1)
    text_width = text_size[0][0]

    # Define a blinking underscore in the place of the next to input character
    if frames%20==0:
        cv2.putText(paper, '_', (text_width, start_write_y+10), font, 2, (255,255,255), 1)
    else:
        paper[start_write_y+5:start_write_y+15, :750] = (0)

    # Green color to the selected category (capitals/lowercase) of letters
    # Red color otherwise
    if count_cl%2!=0:
        cv2.putText(paper, 'A', (730,195), font, 5, (0,255,0), 2)
        cv2.putText(paper, 'a', (780,195), font, 5, (0,0,255), 2)
    else:
        cv2.putText(paper, 'A', (730,195), font, 5, (0,0,255), 2)
        cv2.putText(paper, 'a', (780,195), font, 5, (0,255,0), 2)

    # Some extra graphic settings
    paper[20:50, 910:] = (0)
    paper[70:197, 840:948] = cv2.imread('c://Users//osama//Desktop//Virtual-on-screen-keyboard-main//Images/pencil.jpg')
    cv2.putText(paper, 'Active Line : '+str(line_count+1), (750, 40), font, 1.5, (0,200,200), 2)
    cv2.putText(paper, "Press 'p' or 'P' to print your text in file", (480, paper.shape[0]-15), font, 1.5, (0,200,200), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Paper", paper)

    key = cv2.waitKey(25)
    if key==27:
        break
    # Option to print everything on a file if user press the (P or p) button from keyboard
    # In this cases use the export_message function from print_message file
    message = ""
    if key==ord('p') or key == ord('P'):
        for line in lines:
            message += line + '\n'
        export_message(message)

cap.release()
cv2.destroyAllWindows() 
