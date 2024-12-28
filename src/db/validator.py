import re

def email(email:str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

def password(password:str):
    # da fare
    return None