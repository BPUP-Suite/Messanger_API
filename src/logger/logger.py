# imported from another project and modified

import datetime

import logger.fileLogger as fileLogger

def toConsole(text): # print on console
    date = str(datetime.datetime.now())
    text = date + " - "+text
    print(text)
    toFile(text)

def toFile(text): # write to a log file
    fileLogger.write(text)

def logAPIRequest(username,resource,value):
    text = f"{username} -> {resource} -> {value}"
    toConsole(text)

def logWSConnection(user_id,wb_counter,message):
    text = f"WB -> {message} -> {user_id} ({wb_counter} wb attivi!)"
    toConsole(text)
    
def logWSMessage(user_id,data):
    text = f"WB -> {user_id} -> "+str(data)
    toConsole(text)

def fromDatabase(text):
    toConsole("DATABASE: "+text)
