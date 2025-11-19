#!/usr/bin/python3

import os
import sys
import serial
import time
import logging
from signal import signal, SIGINT
from sys import exit
from queue import Queue,Empty
from logging.handlers import TimedRotatingFileHandler



# Port Configuration
logFileName = "metData"
bufferFileName = "data-buffer/metData"
q = Queue(2)


#this part gets the logger to wrote logs to a specific file in this console
#TimedRotatingFileHandler is in charge of rotating to the log filer every 10 minutes with a max of n backup files.
def setupLogger(filename, backupNum):
        logger = logging.getLogger('Serial logger')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        #fh = logging.FileHandler(filename)
        fh = logging.handlers.TimedRotatingFileHandler(filename, when="midnight", interval = 1, backupCount=backupNum)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log levels
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s,%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        # Return the Created logger
        return logger

#uses the set up for the logger
#opens the serial connection to 'ttyUSB0'
#reads the data from the serial port 'ttyUSB0' and logs in in time specified
#helps exiting with the keyboard 'ctrl c'
def main(qSignal):
        ## Logger Configuration
        global logFileName
        global bufferFileName
        log = setupLogger(logFileName, 50)
        bufferLog = setupLogger(bufferFileName, 0)
        ## Begin
        log.info("Program Started")
        bufferLog.info("Program Started")
        ser = None
        try:
                ser = serial.Serial('/dev/ttyUSB0',9600,8,'N',1,timeout=1)
        except Exception as e:
                log.error("Got Fatal error - {}". format(e))
                exit(4)

        #Loop for Reception
        while 1:
                try:
                        squit = qSignal.get(block=False, timeout=0.1)
                except Empty as e:
                        squit = False
                if squit == True:
                        log.info("Exiting")
                        ser.close()
                        exit(0)
                # Get Data
                try:
                        data = (ser.readline()).decode('utf-8')

                        if len(data) > 0:
                                log.info(data)
                                bufferLog.info(data)

                except KeyboardInterrupt as e:
                        q.put(True)
                        log.info("Ctrl + C pressed")
                        bufferLog.info("Ctrl + C pressed")


#handles the signal and puts true into the queue to get it to keep looping
def handler(signal_received, frame):
        # Handle any cleanup here
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        q.put(True)

if __name__ == "__main__":
        signal(SIGINT, handler)
        print('Running. Press CTRL-C to exit.')
        main(q)

'''
while True:
        output = ''
        ser = serial.Serial('/dev/ttyUSB0',9600, 8, 'N', 1,timeout = 0.1)
        while output == '':
                output = ser.readline()
        if (output != b''):
                print(output)
                datafile.write(output.decode('utf-8'))
'''
'''
print(ser.get_settings())
data = ser.read(10)
print(data)


# Open datadirect.csv
file_data = open('ve_data.csv', 'w')
print("Reading data and writing to ve_data.csv")


output = ser.read(10) # Read 4 bytes from serial buffer
print(output)
print(output.decode('utf-8'))
# listen for the input, exit if nothing received in timeout period
#output = " "
#while output != "":
#       output = ser.readline()
#       print(output)
#output = ""

# Close file
print("Stopped writing to ve_data.csv")
file_data.close()
'''