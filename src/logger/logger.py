# imported from another project and modified

import datetime

import logger.fileLogger as fileLogger

def toConsole(text): # print on console
    date = str(datetime.datetime.now())
    text = date + " - "+text
    print(text)
    toFile(text)
    addToQueue_Stream(text)

def toFile(text): # write to a log file
    fileLogger.write(text)

def logAPIRequest(username,resource,value):
    text = f"{username} -> {resource} -> {value}"
    toConsole(text)

def logWSConnection(user_id,wb_counter,message):
    text = f"WB -> {message} -> {user_id} ({wb_counter} wb attivi!)"
    toConsole(text)
    
def logWSMessage(user_id,data):
    text = f"WB -> {user_id} -> {data}"
    toConsole(text)

def fromDatabase(text):
    toConsole("DATABASE: "+text)

def logDebug(text):
    toConsole("######## DEBUG INFO: "+str(text))

import queue
log_queue = queue.Queue()

# Funzione per aggiungere un messaggio alla coda
def addToQueue_Stream(text):
    log_queue.put(text)

def toStream():
    while True:

        # Prendi il prossimo messaggio dalla coda
        message = log_queue.get()
        # Invia il messaggio come evento SSE
        yield f"data: {message}\n\n"
        log_queue.task_done()  # Segna il messaggio come processato
