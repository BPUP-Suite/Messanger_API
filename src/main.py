# START COMMAND: uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.websockets import WebSocket,WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from typing import Dict, List
import traceback

import db.database as database
import db.object as object
from security.encrypter import generate_hash,generate_password_hash
from logger.logger import logAPIRequest, logWSConnection, toConsole, logWSMessage, logDebug, toStream, logAPIError
import db.jsonBuilder as json
import db.validator as validator

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permette richieste da qualsiasi dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permette tutte le richieste HTTP (GET, POST, ecc.)
    allow_headers=["*"],  # Permette tutti gli header
)

toConsole("----------------------------------------------------------")
toConsole("API started!")

if not(database.exist()):
    toConsole("Creating database...")
    database.init()
    toConsole("Database created!")

# get /docs for all request documentation
# da fare i docs relativi ai sockets


# WEB SOCKET MANAGER

active_connections: Dict[str, List[WebSocket]] = {} # array of active connection of every user

@app.websocket("/ws/{user_id}/{api_key}")

async def websocket_endpoint(user_id:str, api_key:str, websocket: WebSocket): # user_id used for connection, api_key to check if user is valid

  confirmation = (database.get_userHandle_from_apiKey(api_key) == database.user_group_channel_fromID_toHandle(user_id))

  if not confirmation:
      logDebug("Connessione chiusa per "+user_id+". Non dispone delle autorizzazioni per entrare")
      logWSConnection(user_id,len(active_connections[user_id]),"Closed")
      await websocket.close(code=3000) # Not authorized

  # Add the websocket connection to the active connections for the room
  if user_id not in active_connections:
      logDebug("Primo utente ws per "+user_id)
      active_connections[user_id] = []
    
  active_connections[user_id].append(websocket)

  await websocket.accept()
  logWSConnection(user_id,len(active_connections[user_id]),"Opened")
  try:
    while True:
        
        data = await websocket.receive_text()

        if data != None:
            logDebug( user_id+" -WS> "+json.dumps(data))
            try:
                type = json.getValue(data,"type")
                # INITIALIZE CLIENT DATABASE
                if(type == "init"):
                    response = database.clientDB_init(user_id)
                
                # SEND MESSAGE TO EVERY SENDER AND RECEIVER DEVICES
                if(type == "send_message"):

                    response = {"type":"send_message","send_message":False}
                
                    text = json.getValue(data,"text")

                    # da gestire bene l'errore nella generazione della risposta e da aggiungere anche in caso di testo mancante,chat_id e salt mancante, ...
                    print(len(text))
                    if len(text) > 2056:
                       raise Exception("Message too long")

                    chat_id = json.getValue(data,"chat_id")

                    try:
                        salt = json.getValue(data,"salt")
                    except Exception as e:
                        salt = False
                        logDebug("No salt provided OR error: "+str(traceback.format_exc())) 

                    message = object.Message(chat_id,text,str(user_id),None)

                    response_sender,response_receiver,receivers = database.send_message(message)

                    if(response_sender != False):

                        # SEND MESSAGE TO RECEIVER AND SENDER CLIENTS (excluded who send msg)

                        count = 0
                        for receiver in receivers:
                            try:
                                logDebug("Receivers: "+str(receivers))
                                if receiver != None:
                                    for connection in active_connections[receiver]:
                                        if str(connection) != str(websocket): 
                                            count+=1
                                            logDebug(" receive_message :" + "  Receiver: "+receiver + "  Risposta: "+ str(response_receiver))
                                            await connection.send_text(json.dumps(response_receiver))
                            except Exception as e:
                                logDebug("No users active for "+str(receiver)+" or error: "+str(traceback.format_exc())) 
                            finally:
                                logDebug("MESSAGGI DI RISPOSTA: "+str(count))

                        if salt != False:
                            response_sender.update({'hash': generate_hash(text,salt)})

                        response = response_sender
                    
                if(type == "create_chat"):
                    response = {"type":"create_chat","create_chat":"False"}

                    chatType = json.getValue(data,"chatType")

                    if(chatType == "personal"):
                        handle_receiver = json.getValue(data,"handle")
                        user_id_receiver = database.user_group_channel_fromHandle_toID(handle_receiver)
                        sender_response = database.create_personalChat(user_id,user_id_receiver)
                    else:
                        sender_response = False

                    if(sender_response != False):
                        response = sender_response

                # ACK (?) (DA MODIFICARE) (NOT-TESTED) #confirm read of messages
                if(type == "ack"):
                    response = {"type":"ack","ack":True}

                    message_id = json.getValue(data,"message_id")
                    
                    # datetime needed ??
                    
                    json_message,receivers = database.ack(user_id,message_id)

                    if(json_message != False):

                        ### MOVE IN A METHOD
                        # SEND ACK TO RECEIVER AND SENDER CLIENTS (excluded who send msg)

                        for receiver in receivers:
                            try:
                                for connection in active_connections[receiver]:
                                    if connection != websocket:
                                        await connection.send_text(json_message)
                            except:
                                logDebug("No users active for "+receiver) 

                logWSMessage(user_id,"Risposta inviata: "+json.dumps(response)+" \n Per richiesta: "+json.dumps(data))
                await websocket.send_text(json.dumps(response))
            except:
                logDebug(str(traceback.format_exc()))
                logWSMessage(user_id,"Messaggio invalido: "+json.dumps(data))
                pass

  except WebSocketDisconnect:
      active_connections[user_id].remove(websocket)
      logDebug("Websocket disconnessa per "+user_id+" oppure errore "+str(traceback.format_exc()))
      pass


@app.get("/user/action/access")
async def main(email:str):

    type = "access_type"

    if not validator.email(email):

        error = "Not a valid e-mail"
        logAPIError(email,type,error)

        return {type: False, "error" : error}

    try:    	
        if database.check_userExistence_fromEmail(email):
            accessType = "login"
        else:
            accessType = "signup"

    except:

        error = "Internal Server Error"
        logAPIError(email,type,error)

        return {type: False, "error" : error}

    logAPIRequest(email,type,accessType)

    return {type: accessType}



@app.get("/user/action/signup")

async def main(email:str,name:str,surname:str,handle:str,password:str):

    type = "signed_up"
    confirmation = False

    try:    	
        password = generate_password_hash(password) # hashed password
        user = object.User(email,name,surname,handle,password) # create User obj used in databases method
        confirmation = database.add_user_toDB(user) # return True: Signup OK | False: Some error occurred, retry  
    except:

        error = "Internal Server Error"
        logAPIError(email,type,error)

        return {type: False, "error" : error}

    logAPIRequest(user.handle,type,confirmation)

    return {type: confirmation} # ritorna true: registrazione effettuata | false: errore, per qualche motivo (non si sa quale :3)



@app.get("/user/action/login")
async def main(email:str,password:str):

    type = "logged_in"

    loginUser = object.LoginUser(email,password) # create LoginUser obj used in databases method (using only email and password)
    api_key = database.user_login(loginUser) 

    if not(api_key):
        return {type: False,"api_key":None}

    return {type: True,"api_key":api_key}



@app.get("/user/action/check-handle-availability")
async def main(handle:str):

    type = "handle_available"
    confirmation = False

    confirmation = database.check_handle_availability(handle)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}


@app.get("/user/action/get-user-id")
async def main(api_key:str):

    type = "user_id"
    
    userID = database.get_userID_from_ApiKey(api_key)

    logAPIRequest(userID,type,userID)

    return {type: userID}


# ADMIN REQUEST # 

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# ADMIN LOG PANEL

# Route to serve the webpage
@app.get("/admin/logs", response_class=HTMLResponse)
async def admin_page(request: Request):
    logs = load_logs_from_file()  # Load logs from the file
    return templates.TemplateResponse("admin/logs/index.html", {"request": request, "logs": logs})

# Stream logs to the admin page
@app.get("/admin/logs/stream")
async def stream():
    return StreamingResponse(toStream(), media_type='text/event-stream')


def load_logs_from_file(log_file: str = "logs/log.txt"):
    try:
        with open(log_file, "r") as file:
            logs = file.readlines()  # Legge tutte le righe nel file
        # Unisce tutte le righe in una singola stringa con un carattere di nuova linea
        return "".join(logs)
    except FileNotFoundError:
        return "Log file not found."
    except Exception as e:
        return f"Error loading logs: {str(e)}"

# Route to serve the webpage
@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("welcome/index.html", {"request": request})

# Action page

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})

# Reboot api

@app.get('/admin/api/methods/reboot')
def riavvia():
    import os,sys
    logDebug("Richiesta reboot")
    try:
        logDebug("fatto")
        os.execv(sys.executable, ['python'] + sys.argv)
        return json.dumps({'success': True})
    except Exception as e:
        logDebug(f"Errore durante il riavvio: {e}")
        return json.dumps({'success': False, 'error': str(e)})

@app.get('/admin/api/methods/close-ws')
def chiudi_ws():
    import os,sys
    logDebug("Chisura di tutti i websocket")
    try:
        logDebug("fatto, chiusura ws")
        for user_id, websockets in active_connections.items():
            for websocket in websockets:
                try:
                   websocket.close() 
                except Exception as e:
                    print(f"Errore durante la chiusura del WebSocket per {user_id}: {e}")

            active_connections[user_id] = []

        return json.dumps({'success ws': True})
    except Exception as e:
        logDebug(f"Errore durante la chiusura ws: {e}")
        return json.dumps({'success': False, 'error': str(e)})
    
## STARTING APPLICATION

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=80) # ADD POSSIBILITY TO CHANGE IP + PORT FROM ENV FILE