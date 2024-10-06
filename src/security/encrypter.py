import bcrypt # password hash

from security.envManager import read_salt
from security.envManager import write_salt

SALT = read_salt()
if(not(SALT)):
    SALT = bcrypt.gensalt(5) # penserò alla privacy in futuro :D
    write_salt(SALT)

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