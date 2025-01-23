import os
import hashlib

from security.envManager import read_salt
from security.envManager import write_salt

SALT = read_salt()
if(not(SALT)):
    SALT = os.urandom(16)
    SALT = SALT.hex()
    write_salt(SALT)

def generate_hash(digest,salt):

    digestBytes = digest.encode('utf-8') 
    saltBytes = bytes.fromhex(salt)

    salted_digest = saltBytes + digestBytes
    
    hash_object = hashlib.sha256(salted_digest)
    hash = hash_object.hexdigest()

    return hash

def generate_password_hash(password):

    return generate_hash(password,SALT)


def check_password_hash(password,hash):
    
    confirmation = False

    if generate_password_hash(password) == hash:
        confirmation = True

    return confirmation