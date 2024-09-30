# START COMMAND: uvicorn main:app --reload

from fastapi import FastAPI, Request
from security.auth import get_user_handle
from logger.logger import logAPIRequest 
import db.database as database

app = FastAPI()

# get /docs for all request documentation

# 

@app.get("/user/action/access")
async def main(email:str):

    # no api check needed

    return {"response":database.check_userExistence_fromEmail(email)}

@app.get("/user/action/signup")

async def main(email:str,name:str,surname:str,username:str,handle:str,password:str,confirm_password:str):
# DA FARE: PASSWORD CRIPTATA NEL DB (che me son dimenticato)
    # no api check needed

    return {"message": email}

@app.get("/user/action/login")
async def main(email:str):

    # no api check needed

    return {"message": email}

@app.get("/user/action/check-handle")
async def main(handle:str):

    # no api check needed

    return {"message": handle}

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