import psycog

import envManager

POSTGRESQL_PASSWORD = envManager.read_postgresql_password()

conn = psycog.connect(dbname="BPUP_DB", user="bpup", password=POSTGRESQL_PASSWORD, host="localhost", port="5432") 

def init(): # init del database

    cursor = conn.cursor()

    POSTGRESQL_INIT_SCRIPT = envManager.read_postgresql_init_script()
    cursor.execute(POSTGRESQL_INIT_SCRIPT)

    cursor.close()