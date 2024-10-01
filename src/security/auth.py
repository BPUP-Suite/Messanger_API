from fastapi import HTTPException, status
import bcrypt # password hash

import importlib # fixed circular import with database.py 

from security.envManager import read_salt
from security.envManager import write_salt

# security measures

    # api key checker

SALT = read_salt()
if(not(SALT)):
    SALT = bcrypt.gensalt(5) # i dont want to store this, penserò alla privacy in futuro :D
    write_salt(SALT)

def get_user_handle(api_key_header):

    check_api_key = importlib.import_module('db.database.check_api_key')
    handle = check_api_key(api_key_header) 

    if handle != None:
        return handle
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )

def generate_hash(password):
    bytes = password.encode('utf-8') 
    hash = str(bcrypt.hashpw(bytes,SALT))

    # remove b' ' (che causano molti problemi nel database e mi fanno bestemmiare :D)
    hash = hash[2:]
    hash = hash[:-1]

    return hash

def check_password_hash(password,hash):
    
    confirmation = False

    if generate_hash(password) == hash:
        confirmation = True

    return confirmation