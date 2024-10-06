from fastapi import HTTPException, status
from db.database import check_api_key

# security measures

    # api key checker

def get_userHandle_from_apiKey(api_key_header):

    handle = check_api_key(api_key_header) 

    if handle != None:
        return handle
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )