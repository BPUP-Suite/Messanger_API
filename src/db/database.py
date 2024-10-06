import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import logger.logger as logger
import security.envManager as envManager
from security.encrypter import check_password_hash

POSTGRESQL_DB = envManager.read_postgresql_db()
POSTGRESQL_USER = envManager.read_postgresql_user()
POSTGRESQL_PASSWORD = envManager.read_postgresql_password()
POSTGRESQL_HOST = envManager.read_postgresql_host()
POSTGRESQL_PORT = envManager.read_postgresql_port()

conn = psycopg2.connect(dbname=POSTGRESQL_DB, user=POSTGRESQL_USER, password=POSTGRESQL_PASSWORD, host=POSTGRESQL_HOST, port=POSTGRESQL_PORT) 

def exist():
    
    cursor = conn.cursor()

    cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", ('users',))
    bool = cursor.fetchone()[0]

    cursor.close()

    return bool


def init(): # init del database

    cursor = conn.cursor()

    POSTGRESQL_INIT_SCRIPT = envManager.read_postgresql_init_script()

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)     

    logger.toConsole("INIT DEL DATABASE ESEGUITO")

    cursor.execute(POSTGRESQL_INIT_SCRIPT)

    cursor.close()

def check_api_key(apy_key):

    user_handle = None

    cursor = conn.cursor()

    QUERY = f"SELECT user_id FROM public.apiKeys WHERE api_key='{apy_key}'"
    
    # fetch database for api_key

    logger.toConsole(QUERY)

    try:
        cursor.execute(QUERY)
        result = cursor.fetchone()
        user_id = result[0]
        print(user_id)
    except:
        cursor.close()
        return None

    user_handle = user_group_channel_fromID_toHandle(user_id)

    cursor.close()

    # return handle to main (None = API_KEY non esiste [NON AUTORIZZATO] , negli altri casi ritorna l`handle dello user che ha eseguito la richiesta [viene anche utilizzato per il log] )

    print(user_handle)
    return user_handle

def user_group_channel_fromID_toHandle(id):

    cursor = conn.cursor()

    QUERY = f"SELECT handle FROM handles WHERE user_id = '{id}' OR group_id = '{id}' OR channel_id = '{id}'"

    logger.toConsole(QUERY)

    cursor.execute(QUERY)

    # fetch database for handle with id

    result = cursor.fetchone()
    handle = result[0]

    cursor.close()

    # return only handle of the requested id

    return handle

def user_group_channel_fromHandle_toID(handle):

    cursor = conn.cursor()

    QUERY = f"SELECT user_id,group_id,channel_id FROM handles WHERE handle = '{handle}'"

    logger.toConsole(QUERY)

    cursor.execute(QUERY)

    # fetch database for IDs with handle

    result = cursor.fetchone()

    cursor.close()

    # return only id of the requested handle

    try:
        if result[0] != None: # user_id
            return result[0]
        elif result[1] != None: # group_id
            return result[1]   
        elif result[2] != None: # channel_id
            return result[2]
    except:
        return None



def check_handle_availability(handle): # done

    cursor = conn.cursor()

    confirmation = False

    QUERY = f"SELECT handle FROM public.handles WHERE handle = '{handle}'"

    logger.toConsole(QUERY)

    cursor.execute(QUERY)

    # fetch database for handle (it should only be 1)
    result = cursor.fetchone()

    if result == None:
        confirmation = True
    
    cursor.close()

    # true: available | false: used

    return confirmation
    
def add_user_toDB(user): # aggiungi API key

    cursor = conn.cursor()

    confirmation = True

    QUERY = f"with new_user as (INSERT INTO public.users(email,name,surname,password) VALUES('{user.email}','{user.name}','{user.surname}','{user.password}') RETURNING user_id), new_handle AS (INSERT INTO public.handles(user_id,handle) VALUES((SELECT user_id FROM new_user),'{user.handle}')) INSERT INTO public.apiKeys(user_id,api_key) VALUES((SELECT user_id FROM new_user),'{user.api_key}')"
    logger.toConsole(QUERY)

    try:
        cursor.execute(QUERY)
        conn.commit()
    except:
        confirmation = False
    
    cursor.close()

    return confirmation

def check_userExistence_fromEmail(email):

    cursor = conn.cursor()

    confirmation = True

    QUERY = f"SELECT email FROM public.users WHERE email = '{email}'"

    logger.toConsole(QUERY)

    cursor.execute(QUERY)

    # fetch database for e-mails (it should only be 1)
    result = cursor.fetchone()

    if result == None:
        confirmation = False
    
    cursor.close()

    # true: email already used | false: email not used

    return confirmation

def user_login_check(loginUser):

    email = loginUser.email
    password = loginUser.password

    cursor = conn.cursor()

    confirmation = False

    # first query, find password
    QUERY = f"SELECT user_id,password FROM public.users WHERE email = '{email}'" 

    logger.toConsole(QUERY)

    cursor.execute(QUERY)

    # fetch database for password (it should only be 1)
    result = cursor.fetchone()

    if result != None:
        hash = result[1] # position 0: id_user | position 1: password_hash
        if check_password_hash(password,hash):
            
            user_id = result[0]
            # second query, find api key
            QUERY = f"SELECT api_key FROM public.apiKeys WHERE user_id = '{user_id}'"

            logger.toConsole(QUERY)

            cursor.execute(QUERY)

            # fetch database for apikey (it should only be 1)
            result = cursor.fetchone()

            confirmation = result[0]

    cursor.close()

    # api-key: login approved | false: login failed

    return confirmation

def send_message(message):

    chat_id = message.chat_id
    text = message.text
    sender = user_group_channel_fromHandle_toID(message.sender)
    date = message.date

    cursor = conn.cursor()

    confirmation = True

    ## FIRST PHASE: ADD MESSAGE TO DB

    QUERY = f"INSERT INTO public.messages (chat_id,text,sender,date) VALUES ('{chat_id}','{text}','{sender}','{date}')" 

    logger.toConsole(QUERY)

    try:
        cursor.execute(QUERY)
        conn.commit()
    except:
        confirmation = False
    
    cursor.close()

    ## SECOND PHASE: SEND MESSAGE TO USERS CLIENT (IDK WHAT TO DO HELP ME PLZ) ########## TBD ##########

    return confirmation