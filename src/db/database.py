import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import logger.logger as logger
import security.envManager as envManager

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

    cursor.execute(POSTGRESQL_INIT_SCRIPT)

    cursor.close()

def check_api_key(apy_key):

    user_handle = None

    cursor = conn.cursor()

    QUERY = f"SELECT user_id FROM api_key WHERE api_key={apy_key}"
    cursor.execute(QUERY)

    # fetch database for api_key

    result = cursor.fetchone()
    user_id = result.get[0]

    user_handle = user_group_channel_fromID_toHandle(user_id)

    cursor.close()

    # return handle to main (None = API_KEY non esiste [NON AUTORIZZATO] , negli altri casi ritorna l`handle dello user che ha eseguito la richiesta [viene anche utilizzato per il log] )

    return user_handle

def user_group_channel_fromID_toHandle(id):

    cursor = conn.cursor()

    QUERY = f"SELECT handle FROM handles WHERE id = {id}"
    cursor.execute(QUERY)

    # fetch database for handle with id

    result = cursor.fetchone()
    handle = result.get[0]

    cursor.close()

    # return only handle of the requested id

    return handle

def check_handle_availability(handle):

    cursor = conn.cursor()

    id = None

    QUERY = f"SELECT id FROM handles WHERE handle = {handle}"
    cursor.execute(QUERY)

    # fetch database for id (it should only be 1)

    result = cursor.fetchone()
    id = result.get[0]

    cursor.close()

    # true: available | false: used

    if id == None:
        return True
    else:
        return False
    
def add_user_toDB(user):

    cursor = conn.cursor()

    confirmation = False

    QUERY = f"with new_user as (INSERT INTO public.users(email,name,surname,password) VALUES('{user.email}','{user.name}','{user.surname}','{user.password}') RETURNING user_id) INSERT INTO public.handles(user_id,handle) VALUES((SELECT user_id FROM new_user),'{user.handle}')"
    logger.toConsole(QUERY)
    if(user.password == user.confirm_password):
        confirmation = cursor.execute(QUERY)
        # VEDI COME FUNZIONA COMMIT
    
    cursor.close()

    return confirmation