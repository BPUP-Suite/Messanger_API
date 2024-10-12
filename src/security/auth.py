from fastapi import HTTPException, status
from db.database import get_userHandle_from_apiKey

# security measures

    # api key checker

def check_api_key(api_key_header):

    handle = get_userHandle_from_apiKey(api_key_header) 

    if handle != None:
        return handle
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
