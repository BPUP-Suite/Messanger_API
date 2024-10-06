# START COMMAND: uvicorn main:app --reload

from fastapi import FastAPI, Request 
from security.auth import get_user_handle
import secrets # api key

import db.database as database
import db.object as object
from security.auth import generate_hash
from logger.logger import logAPIRequest 

app = FastAPI()

if not(database.exist()):
    database.init()

# get /docs for all request documentation

# 

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

    #user_id = APICHECK

    type = "send_message"
    confirmation = False

    #handle = database.user_group_channel_fromID_toHandle(user_id)
    #confirmation = database.send_message(handle)

    #logAPIRequest(handle,type,confirmation)

    return {type: confirmation}




@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.get("/hellos/ciao")
async def say_hello(request: Request):
    
    handle = get_user_handle(request.headers.get('BPUP-API-KEY'))

    logAPIRequest(handle,"hello","test")

    return {"message": f"Hello {handle} {request.headers.get('BPUP-API-KEY')}"}



# ADMIN REQUEST # 