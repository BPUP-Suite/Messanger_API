import os

def read_postgresql_password():

    POSTGRES_PASSWORD = None

    # search for env variables

    if len(POSTGRES_PASSWORD) == 0:
        POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

    if POSTGRES_PASSWORD is None:
        raise ('Postgres password must be provided (POSTGRES_PASSWORD variable)') # se ti parte sta eccezione, mi spiace per te
    return POSTGRES_PASSWORD

def read_postgresql_init_script():

    POSTGRES_INIT_SCRIPT = None

    # search for init.sql files

    if len(POSTGRES_INIT_SCRIPT) == 0:
        file = os.open("init.sql","r")
        POSTGRES_INIT_SCRIPT = file.read()

    if POSTGRES_INIT_SCRIPT is None:
        raise ('Postgres init script must be provided (POSTGRES_INIT_SCRIPT variable)') # se ti parte sta eccezione, mi spiace per te pt.2
    return POSTGRES_INIT_SCRIPT