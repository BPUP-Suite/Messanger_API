import re

def email(email:str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

def password(password:str):

    # Password length should be between 6 and 12 characters
    if (len(password) < 8 or len(password) > 32):
        # Password should contain at least one lowercase letter
        if not re.search("[a-z]", password):
            return False
        # Password should contain at least one digit
        if not re.search("[0-9]", password):
            return False
        # Password should contain at least one uppercase letter
        if not re.search("[A-Z]", password):
            return False
        # Password should contain at least one special character among '$', '#', '@', '!', '?'
        if not re.search("[$#@!?]", password):
            return False
        # Password should not contain any whitespace character
        if re.search(r"\s", password):
            return False
        else:
            # If all conditions are met
            return True

