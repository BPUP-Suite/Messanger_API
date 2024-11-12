# START COMMAND: uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.websockets import WebSocket,WebSocketDisconnect

from security.auth import check_api_key # remove (api used only in socket)
from typing import Dict, List
import traceback

import db.database as database
import db.object as object
from security.encrypter import generate_hash
from logger.logger import logAPIRequest, logWSConnection, toConsole, logWSMessage, logDebug
import db.jsonBuilder as json

app = FastAPI()

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
      logWSConnection(user_id,len(active_connections[user_id]),"Closed")
      await websocket.close(code=3000) # Not authorized

  # Add the websocket connection to the active connections for the room
  if user_id not in active_connections:
      active_connections[user_id] = []
    
  active_connections[user_id].append(websocket)

  await websocket.accept()
  logWSConnection(user_id,len(active_connections[user_id]),"Opened")

  await websocket.send_text("Connessione al socket effettuata")

  try:
    while True:
        data = await websocket.receive_text()

        if data != None:

            logWSMessage(user_id,"Message: "+json.dumps(data))

            try:
                type = json.getValue(data,"type")

                # togli api key check e usa lo user id della socket

                # INITIALIZE CLIENT DATABASE
                if(type == "init"):

                    apiKey = json.getValue(data,"apiKey")

                    response = database.clientDB_init(apiKey)
                
                # SEND MESSAGE TO EVERY SENDER AND RECEIVER DEVICES
                if(type == "send_message"):

                    response = {"send_message":False}
                    
                    chat_id = json.getValue(data,"chat_id")
                    text = json.getValue(data,"text")
                    receiverHandle = json.getValue(data,"receiver")

                    message = object.Message(chat_id,text,user_id,None)

                    message_id,json_message,receivers = database.send_message(message,receiverHandle)

                    if(message_id != False):

                        # SEND MESSAGE TO RECEIVER AND SENDER CLIENTS (excluded who send msg)

                        for receiver in receivers: #da vedere se crasha se non c'è anche solo un receiver nella list
                            try:
                                for connection in active_connections[receiver]:
                                    if connection != websocket: 
                                        logWSMessage(receiver,str(json_message))
                                        await connection.send_text(json.dumps(json_message))
                            except Exception as e:
                                logDebug("No users active for "+receiver+" or error: "+str(traceback.format_exc())) 
                            
                        response = {"send_message":True,"date":str(message.date),"message_id":message_id}

                # ACK (?) (NOT-TESTED) #confirm read of messages
                if(type == "ack"):
                    response = json.dumps('{"ack":"true"}')

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

            except Exception as e:
                logWSMessage(user_id,"Messaggio invalido: "+json.dumps(data)+" || con errore: "+str(traceback.format_exc()))
                pass

  except WebSocketDisconnect:
      active_connections[user_id].remove(websocket)
      pass


###
#DISCONNETTI DA TUTTE LE WEBSOCKET ALLO SHUTDOWN
#@app.on_event("shutdown")
#async def shutdown():
 #   for websocket in active_connections_set:
  #      await websocket.close(code=1001)
###


@app.get("/user/action/access")
async def main(email:str):

    # no api check needed

    type = "accessType"
    accessType = "signup"

    if database.check_userExistence_fromEmail(email):
        accessType = "login"

    logAPIRequest(email,type,accessType)

    return {type: accessType}



@app.get("/user/action/signup")

async def main(email:str,name:str,surname:str,handle:str,password:str,confirm_password:str):

    # no api check needed

    type = "signedUp"
    confirmation = False


    if(password==confirm_password):
        password = generate_hash(password) # hashed password
        user = object.User(email,name,surname,handle,password) # create User obj used in databases method
        confirmation = database.add_user_toDB(user) # return True: Signup OK | False: Some error occurred, retry
        logAPIRequest(user.handle,type,confirmation)

    return {type: confirmation} # ritorna true: registrazione effettuata | false: errore, per qualche motivo (non si sa quale)



@app.get("/user/action/login")
async def main(email:str,password:str):

    # no api check needed

    type = "api_key"

    loginUser = object.LoginUser(email,password) # create LoginUser obj used in databases method (using only email and password)

    api_key = database.user_login_check(loginUser) 
    # api-key: login approved | false: login failed

    return {type: api_key}



@app.get("/user/action/check-handle-availability")
async def main(handle:str):

    # no api check needed

    type = "handle_available"
    confirmation = False

    confirmation = database.check_handle_availability(handle)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}


@app.get("/user/action/get-user-id")
async def main(api_key:str):

    # no api check needed

    type = "user_id"
    
    userID = database.get_userID_from_ApiKey(api_key)

    logAPIRequest(userID,type,userID)

    return {type: userID}


# ADMIN REQUEST # 



## STARTING APPLICATION

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000) # ADD POSSIBILITY TO CHANGE IP + PORT FROM ENV FILE