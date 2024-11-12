# START COMMAND: uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.websockets import WebSocket,WebSocketDisconnect

from security.auth import check_api_key
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
                        logDebug("DFSSDFSDFDFS")
                        # SEND MESSAGE TO RECEIVER AND SENDER CLIENTS (excluded who send msg)
                        logDebug("KOSKDFSKDFSDFS"+str(receivers))
                        for receiver in receivers: #da vedere se crasha se non c'è anche solo un receiver nella list
                            logDebug("TOCCA TE "+str(receiver))
                            try:
                                for connection in active_connections[receiver]:
                                    if connection != websocket: 
                                        logWSMessage(receiver,json.dumps(json_message))
                                        await connection.send_text(json_message)
                            except Exception as e:
                                logDebug("No users active for "+receiver+"ERRORE  "+str(e)) 
                            
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

    type = "user_id"
    
    userID = database.get_userID_from_ApiKey(api_key)

    logAPIRequest(userID,type,userID)

    return {type: userID}























######################################################################## DA ELIMINARE

@app.get("/test")
async def main(user_id:str,message:str): # 1000000000000000000

    try:
        for connection in active_connections[user_id]:
            await connection.send_text(message)
    except:
        pass

    return {user_id:message}

@app.get("/user/action/send-message")
async def main(api_key:str,chat_id:str,text:str,receiver: str | None = None):

    ## DB INFO (da aggiornare)

#   message_id bigint NOT NULL,                     generated in database
#   chat_id bigint NOT NULL,                        from API request
#   text text NOT NULL,                             from API request
#   sender bigint NOT NULL,                         from api_key for API request
#   date timestamp without time zone NOT NULL,      generated in databse

    ##

    ## tries to create chat if chat_id doesnt exist (and is a personal chat, chat id for personal chat always starts with "2")

    # API CHECK

    handle = check_api_key(api_key)

    type = "send_message"
    confirmation = False

    message = object.Message(chat_id,text,handle,"")

    json_message,receivers = database.send_message(message,receiver)

    if(json_message != False):

        # SEND MESSAGE TO RECEIVER CLIENT

        for receiver in receivers:
            try:
                for connection in active_connections[receiver]:
                    await connection.send_text(json_message)
            except:
                logDebug("No users active for "+receiver)

        # SEND MESSAGE TO OTHER SENDER CLIENT

        try:
            for connection in active_connections[handle]:
                await connection.send_text(json_message)   
        except:
            logDebug("No users active for "+handle)   

        confirmation = True

    logAPIRequest(handle,type,confirmation)

    #return {type:confirmation}
    return json_message


# NOT NEEDED
@app.get("/chat/create/personal-chat")
async def main(api_key:str,receiver:str):

    ## DB INFOSELECT currval(pg_get_serial_sequence('persons','id'));

#   chat_id bigint NOT NULL,                        generated based on both users handles 
#                                                   example:  sender: giorgio  receiver: antonio  chat_id = giorgio-antonio

    ##

    # API CHECK

    handle = check_api_key(api_key)

    type = "create_personal-chat"
    confirmation = False

    ### CHECK IF RECEIVER IS AN HANDLE OR A USER ID 

    ## WE NEED HANDLE NOT USERID

    chat = object.Chat(handle,receiver)
    confirmation = database.create_personalChat(chat)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}

@app.get("/test2")
async def main(api_key:str):
    return database.clientDB_init(api_key)

@app.get("/chat/create/group")
async def main(api_key:str,name:str,description:str):

    ## DB INFO  

    # chat_id bigint NOT NULL,                generated in db
    # members bigint[] NOT NULL,              first element is user_id from api_key (api_key->handle->user_id)
    # admins bigint[] NOT NULL,               //
    # description text,                       from request
    # group_picture_id bigint[]               ????? da rivedere

    # API CHECK

    handle = check_api_key(api_key)

    type = "create-group"
    confirmation = False

    group = object.Group(handle,name,description)
    confirmation = database.create_group(group)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}

@app.get("/upload")
async def main(api_key:str,type:str,fileA: UploadFile = File(...)):  # da sostituire type con utilizzo delle cartelle

    # API CHECK

    handle = check_api_key(api_key)

    type="upload"+type
    confirmation = False

    file = object.File(handle,type,fileA)
    confirmation = database.upload_file(file)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}

@app.get("/download")
async def main(api_key:str,file_id:str):

    #DB INFO

    # API CHECK

    handle = check_api_key(api_key)

    type="download"

    ##DA VEDERE SE UTENTE HA ACCESSO AL FILE (è nel canale/gruppo/chat da cui deriva) fatto nella classe database
    file = database.download_file(handle,file_id) # file

    ## test download file
    #handle="test"
    #with open("requirements.txt","r") as filez:
    #        data = filez.read()
    #file = object.FileDownload(data,"test","txt")
    ##

    logAPIRequest(handle,type,file!=None)

    headers = {'Content-Disposition': f'inline; filename={file.name}',"content-type": "application/octet-stream"}
    return Response(file.data,media_type=f'application/{file.type}',headers=headers)


###############################################################################################



# ADMIN REQUEST # 



## STARTING APPLICATION

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000) # ADD POSSIBILITY TO CHANGE IP + PORT