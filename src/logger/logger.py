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

def logWSConnection(user_id):
    text = f"{user_id} new websocket"
    toConsole(text)

def logClosedWSConnection(user_id):
    text = f"Closed {user_id}, no auth"
    toConsole(text)