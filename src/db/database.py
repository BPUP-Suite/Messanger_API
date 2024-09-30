import psycog

import src.security.envManager as envManager

POSTGRESQL_PASSWORD = envManager.read_postgresql_password()

conn = psycog.connect(dbname="BPUP_DB", user="bpup", password=POSTGRESQL_PASSWORD, host="localhost", port="5432") 

def init(): # init del database

    cursor = conn.cursor()

    POSTGRESQL_INIT_SCRIPT = envManager.read_postgresql_init_script()
    cursor.execute(POSTGRESQL_INIT_SCRIPT)

    conn.commit()

    cursor.close()

def check_api_key(apy_key):

    return "ok"

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
