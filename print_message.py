#function to string inside text file in specific folder 
import os, os.path

# Directory (folder) of messages
dirName = 'messages'
#if path dosen't exists then create new one
if not os.path.exists(dirName):
    os.mkdir(dirName) 

#calcualte the number of saved messages
number_of_messages = len([messages for messages in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, messages))])

# Name of new message : "message+number.txt"
new_message = 'message' + str(number_of_messages+1)+'.txt'

def export_message(text):
    with open(dirName+'/'+new_message, 'w') as myfile:
        myfile.write(text)
