import bcrypt # password hash

from security.envManager import read_salt
from security.envManager import write_salt

SALT = read_salt().decode('utf-8')
if(not(SALT)):
    SALT = bcrypt.gensalt(5) # penserò alla privacy in futuro :D
    write_salt(SALT)

def generate_hash(digest,salt):

    bytes = digest.encode('utf-8') 
    salt = salt.encode('utf-8')
    
    hash = bcrypt.hashpw(bytes,salt)

    hash = hash.decode('utf-8')

    return hash

def generate_password_hash(password):

    return generate_hash(password,SALT)


def check_password_hash(password,hash):
    
    confirmation = False

    if generate_password_hash(password) == hash:
        confirmation = True

    return confirmation