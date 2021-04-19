#================================================#
# Function to save text-string inside a txt file #
#    and save this file to a specific folder     #
#================================================#

# Packages
import os, os.path
from datetime import datetime

# Current date and time as in string format
date_time = datetime.now().strftime("%d-%m-%y_%H:%M")
# %d-%m-%y_%H:%M : day-month-year_hours:minutes

# Directory (folder) of messages
dir_name = 'messages'
if not os.path.exists(dir_name):
    os.mkdir(dir_name) # Create folder if not exists

# Count the number of the saved messages
number_of_messages = len([messages for messages in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, messages))])

# Name of new message : "message(number)_day-month-year_hour:minutes.txt"
new_message = 'message' + str(number_of_messages+1) + '_' + date_time + '.txt'

def export_message(text):
    with open(dir_name+'/'+new_message, 'w') as myfile:
        myfile.write(text)
