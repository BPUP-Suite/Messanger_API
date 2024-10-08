# START COMMAND: uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, Response
from security.auth import get_userHandle_from_apiKey
import secrets # api key

import db.database as database
import db.object as object
from security.encrypter import generate_hash
from logger.logger import logAPIRequest 

app = FastAPI()

if not(database.exist()):
    database.init()

# get /docs for all request documentation

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

    api_key = secrets.token_urlsafe(256)

    if(password==confirm_password):
        password = generate_hash(password) # hashed password
        user = object.User(email,name,surname,handle,api_key,password) # create User obj used in databases method
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



@app.get("/user/action/send-message")
async def main(api_key:str,chat_id:str,text:str):

    ## DB INFO

#   message_id bigint NOT NULL,                     generated in database
#   chat_id bigint NOT NULL,                        from API request
#   text text NOT NULL,                             from API request
#   sender bigint NOT NULL,                         from api_key for API request
#   date timestamp without time zone NOT NULL,      generated in databse

    ##

    # API CHECK

    handle = get_userHandle_from_apiKey(api_key)

    type = "send_message"
    confirmation = False

    message = object.Message(chat_id,text,handle)
    confirmation = database.send_message(message)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}



@app.get("/chat/create/personal-chat")
async def main(api_key:str,receiver:str):

    ## DB INFO

#   chat_id bigint NOT NULL,                        generated based on both users handles 
#                                                   example:  sender: giorgio  receiver: antonio  chat_id = giorgio-antonio

    ##

    # API CHECK

    handle = get_userHandle_from_apiKey(api_key)

    type = "create_personal-chat"
    confirmation = False

    ### CHECK IF RECEIVER IS AN HANDLE OR A USER ID 

    ## WE NEED HANDLE NOT USERID

    chat = object.Chat(handle,receiver)
    confirmation = database.create_personalChat(chat)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}

@app.get("/chat/create/group")
async def main(api_key:str,name:str,description:str):

    ## DB INFO  

    # chat_id bigint NOT NULL,                generated in db
    # members bigint[] NOT NULL,              first element is user_id from api_key (api_key->handle->user_id)
    # admins bigint[] NOT NULL,               //
    # description text,                       from request
    # group_picture_id bigint[]               ????? da rivedere

    # API CHECK

    handle = get_userHandle_from_apiKey(api_key)

    type = "create-group"
    confirmation = False

    group = object.Group(handle,name,description)
    confirmation = database.create_group(group)

    logAPIRequest(handle,type,confirmation)

    return {type: confirmation}

@app.get("/upload")
async def main(api_key:str,type:str,fileA: UploadFile = File(...)):  # da sostituire type con utilizzo delle cartelle

    # API CHECK

    handle = get_userHandle_from_apiKey(api_key)

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

    handle = get_userHandle_from_apiKey(api_key)

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

# ADMIN REQUEST # 