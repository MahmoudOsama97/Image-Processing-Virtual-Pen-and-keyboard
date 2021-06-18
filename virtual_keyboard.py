import cv2
import numpy as np
import math
import pyglet

from print_message import *

def keyboard():

    load_from_disk = True
    if load_from_disk:
        penval = np.load('setupObject.npy')

    #set to keyboard's buttons
    sound = pyglet.media.load("./beep.wav", streaming=False)

    cap = cv2.VideoCapture(0)

    
    _, video = cap.read()
    # Resize video
    video = cv2.resize(video, (1280,720))  

    # Set width and height 
    width, height = 65, 65
    
    #distanceance between two consecutive rectangles
    distance = 15

    # Initial position of text in frame
    xPosition = int((video.shape[1] - (10*width + 9*distance))/2)
    yPosition = 50

    #Text style
    font = cv2.FONT_HERSHEY_PLAIN  # Font type
    fontThickness = 4              # Font thickness
    fontScale = 4                  # Font scale

    #Special buttons
    specialButtons = ["BACK", "DELETE", "ENTER", "Aa", "SPACE", "NUM2SYM"]    

    # Set a string with letters, numbers and symbols
    numbers = "1234567890" 
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

    
    def draw_letters(let_index, text):
        width, height = 65,65
        for i in range(alpha_len):
            if i < 10:
                if let_index == i:
                    x, y = xPosition + i*(width + distance), yPosition
            elif i >= 10 and i < 21:
                if let_index == i:
                    x, y = xPosition - int(xPosition/1.5) + (i-10)*(width + distance), yPosition + (height + distance)
            elif i >= 21 and i < 31:
                if let_index == i:
                    x, y = xPosition + (i-21)*(width + distance), yPosition + 2*(height + distance) 
            elif i >= 31 and i < 40:
                if let_index == i:
                    x, y = 2*xPosition + (i-31)*(width + distance), yPosition + 3*(height + distance)
            elif i==40:
                if let_index == i:
                    x, y = xPosition - 3*distance, yPosition + 4*(height + int(1.5*distance))
                    width += 30
            elif i==41:
                if let_index == i:
                    x, y = xPosition, yPosition + 5*(height + int(1.5*distance))
                    width += 70
            elif i==42:
                if let_index == i:
                    x, y = xPosition + 11*width - distance, yPosition + 4*(height + int(1.5*distance))
                    width += 50
            elif i==43:
                if let_index == i:
                    x, y = xPosition + 11*width + int(distance/2), yPosition + 5*(height + int(1.5*distance))
            elif i==44:
                if let_index == i:
                    x, y = xPosition + 5*width, yPosition + 4*(height + int(1.5*distance))
                    width += 200
            elif i==45:
                if let_index == i:
                    x, y = xPosition + 3*width - int(width/2), yPosition + 4*(height + int(1.5*distance))
                    width += 80

        cv2.rectangle(frame, (x, y), (x + width, y + height), (255), 2)

        # Find the size of each character based on font, font-scale and font-weight
        textSize = cv2.getTextSize(text, font, fontScale, fontThickness)
        textWidth = textSize[0][0]
        textHeight = textSize[0][1]

        # Text position for each character
        text_x_position = int((width - textWidth)/2) + x
        text_y_position = int((height + textHeight)/2) + y

        text_color = (0,255,255)

        # Add text in frame
        if let_index < 10:
            cv2.putText(frame, text, (text_x_position-10, text_y_position), font, fontScale, text_color, fontThickness-1)
        elif let_index < alpha_len - 6:
            cv2.putText(frame, text, (text_x_position, text_y_position), font, fontScale, text_color, fontThickness-1)
        elif let_index==40:
            cv2.putText(frame, specialButtons[0], (text_x_position-18, text_y_position-5), font, 2, text_color, 3)
        elif let_index==41:
            cv2.putText(frame, specialButtons[1], (text_x_position-32, text_y_position-5), font, 2, text_color, 3)
        elif let_index==42:
            cv2.putText(frame, specialButtons[2], (text_x_position-25, text_y_position-5), font, 2, text_color, 3)
        elif let_index==43:
            cv2.putText(frame, specialButtons[3], (text_x_position-13, text_y_position-5), font, 3, text_color, 3)
        elif let_index==44:
            cv2.putText(frame, specialButtons[4], (text_x_position-30, text_y_position-5), font, 2, text_color, 3)
        elif let_index==45:
            cv2.putText(frame, specialButtons[5], (text_x_position-53, text_y_position-5), font, 1.8, text_color, 3)

    # Function to draw the extra symbols(characters) close to numbers of first keys' row
    def draw_extra_chars(let_index, text):
        for i in range(len(symbols)):
            if let_index == i:
                x, y = xPosition + i*(width + distance), yPosition

        # Find the size of each character based on style
        textSize = cv2.getTextSize(text, font, fontScale-3, fontThickness-2)    
        
        # Text position in x and y
        text_x_position = int((width - textSize[0][0])/2) + x + distance
        text_y_position = int((height + textSize[0][1])/2) + y + int((3*distance)/2)
        # Add text
        cv2.putText(frame, text, (text_x_position, text_y_position), font, fontScale-2, (0,0,255), fontThickness-2)

    #create new frame to put in typed message
    board = np.zeros((250,1000,3), np.uint8)
    cv2.namedWindow("board")

    # Starting position of text in "board" frame
    start_write_x = 5
    start_write_y = 35
    
    count_cl = 1
    count_ns = 1
    my_text = ""
    frames = 0
    lines = ['']
    line_count = 0

    while True:
        _, frame = cap.read()
        # Resize original frame
        frame = cv2.resize(frame, (1280,720))
        #Flip original frame
        frame = cv2.flip(frame, 1) 

        let_index = -1
        frames += 1 

        # Apply Gaussian Blur filter on frame
        blurFrame = cv2.GaussianBlur(frame, (5,5), 5)

        # Apply HSV format
        hsv_frame = cv2.cvtColor(blurFrame, cv2.COLOR_BGR2HSV)


        # Color settings for Green (this color can be changed to the desired one)
        # Define lower and upper color
        if load_from_disk:
            lower_color = penval[0]
            upper_color = penval[1]


        # Apply mask on the hsv frame
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Find contours
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            #each time find max contour for each frame
            contour = max(contours, key=cv2.contourArea)      
            M = cv2.moments(contour)

            # Draw each contour
            cv2.drawContours(frame, [contour], -1, (0,255,0), 2)

            # Find each contour center
            if int(M["m00"])!=0:
                centerX = int(M["m10"] / M["m00"])
                centerY = int(M["m01"] / M["m00"])
                # Draw center for  each contour
                cv2.circle(frame, (centerX, centerY), 2, (0,0,255), 2) 

                # Check if center is inside a letter box per row of rectangles in frame
                if centerY > yPosition and centerY < yPosition + height:
                    for k in range(10):
                        if centerX > xPosition + k*(width+distance) and centerX < xPosition + k*(width+distance) + width:
                            let_index = k
                elif centerY > yPosition + height + distance and centerY < yPosition + 2*height + distance:
                    for k in range(10, 21):
                        if centerX > xPosition - int(xPosition/1.5) + (k-10)*(width + distance) and centerX < xPosition - int(xPosition/1.5) + (k-10)*(width + distance) + width:
                            let_index = k
                elif centerY > yPosition + 2*height + 2*distance and centerY < yPosition + 3*height + 2*distance:
                    for k in range(21, 31):
                        if centerX > xPosition + (k-21)*(width + distance) and centerX < xPosition + (k-21)*(width + distance) + width:
                            let_index = k
                elif centerY > yPosition + 3*height + 3*distance and centerY < yPosition + 4*height + 3*distance:
                    for k in range(31, 40):
                        if centerX > 2*xPosition + (k-31)*(width + distance) and centerX < 2*xPosition + (k-31)*(width + distance) + width:
                            let_index = k
                elif centerY > yPosition + 4*height + 6*distance and centerY < yPosition + 5*height + 6*distance:
                    if centerX > xPosition - 3*distance and centerX < xPosition - 3*distance + width + 30:
                        let_index = 40
                    elif centerX > xPosition + 11*width - distance and centerX < xPosition + 11*width - distance + width + 50:
                        let_index = 42
                    elif centerX > xPosition + 5*width and centerX < xPosition + 5*width + width + 200:
                        let_index = 44
                    elif centerX > xPosition + 3*width - int(width/2) and centerX < xPosition + 3*width - int(width/2) + width + 80:
                        let_index = 45
                elif centerY > yPosition + 5*height + 7*distance and centerY < yPosition + 6*height + 7*distance:
                    if centerX > xPosition and centerX < xPosition + width + 70:
                        let_index = 41
                    elif centerX > xPosition + 11*width + int(distance/2) and centerX < xPosition + 11*width + int(distance/2) + width:
                        let_index = 43

        new_line = False
        let_sound = False

        # Every 20 frames let user to add a new letter-character
        if frames == 20:
            let_sound = True
            frames = 0

        for i in range(alpha_len):
            draw_letters(i, letters[i]) 
            if (let_index == i) and (let_sound is True):
                #play the sound when character is choosen
                sound.play()
                # Operations of the special symbols-characters
                # Delete one (1) character
                if i == letters.index("<"):
                    if line_count >= 1:
                        if len(my_text) == 0:
                            line_count -= 1
                            my_text = lines[line_count] 
                            start_write_y -= 40
                    board[line_count*30 + 15:, 5:] = (0)
                    my_text = my_text[:-1]
      
                elif i == letters.index("_"):
                    my_text += ' '
                # Erase everything that was written before (delete)
                elif i == letters.index("-"):
                    line_count = 0
                    board[:] = (0,0,0)
                    my_text = ''
                    lines = ['']
                    start_write_y = 35
                # Go to the next line (newline) (enter)
                elif i == letters.index(">"):
                    line_count += 1
                    new_line = True
                    lines.append('')
                    my_text = ''
                    board[start_write_y+5:start_write_y+15, :750] = (0)
                # Change between capitals and lower case letters (Caps Lock)
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

        # Add text to "board" frame
        lines[line_count] = my_text
        cv2.putText(board, lines[line_count], (start_write_x, start_write_y), font, 2, (255,255,255), 1)

        if new_line is True:
            start_write_y += 40 # User select the new line 'button'

        # Text size
        textSize = cv2.getTextSize(my_text, font, 2, 1)
        textWidth = textSize[0][0]

        # Define a blinking underscore in the place of the next to input character
        if frames%20==0:
            cv2.putText(board, '_', (textWidth, start_write_y+10), font, 2, (255,255,255), 1)
        else:
            board[start_write_y+5:start_write_y+15, :750] = (0)

  
        if count_cl%2!=0:
            cv2.putText(board, 'A', (730,195), font, 5, (100,200,150), 2)
            cv2.putText(board, 'a', (780,195), font, 5, (200,200,200), 2)
        else:
            cv2.putText(board, 'A', (730,195), font, 5, (100,200,150), 2)
            cv2.putText(board, 'a', (780,195), font, 5, (200,200,200), 2)

  
        board[20:50, 910:] = (0)
        board[70:197, 840:948] = cv2.imread('./Images/pencil.jpg')
        cv2.putText(board, 'Current Line : '+str(line_count+1), (750, 40), font, 1.5, (1000,100,200), 2)
        cv2.putText(board, "Press 'p' or 'P' to print your text in file", (480, board.shape[0]-15), font, 1.5, (200,200,200), 2)

        cv2.imshow("Frame", frame)
        cv2.imshow("board", board)

        key = cv2.waitKey(25)
        if key==27:
            break
    
        #press P on real keyboard to save typed message from virual keyboard on file 
        message = ""
        if key==ord('p') or key == ord('P'):
            for line in lines:
                message += line + '\n'
            export_message(message)

    cap.release()
    cv2.destroyAllWindows() 
