import os

def read_variable(name):

    VARIABLE = None

    # search for env variables
    VARIABLE = os.environ.get(name)

    if VARIABLE is None:
        raise ValueError(f'{name} must be provided ( {name} variable)') # se ti parte sta eccezione, mi spiace per te
    
    return VARIABLE

def read_postgresql_db():

    return read_variable("POSTGRES_DB")

def read_postgresql_user():

    return read_variable("POSTGRES_USER")

def read_postgresql_password():

    return read_variable("POSTGRES_PASSWORD")

def read_postgresql_host():

    return read_variable("POSTGRES_HOST")

def read_postgresql_port():

    return read_variable("POSTGRES_PORT")

def read_postgresql_init_script():

    POSTGRES_INIT_SCRIPT = None

    # search for init.sql files
    with open("db/init.sql","r") as file:
        POSTGRES_INIT_SCRIPT = file.read()

    if POSTGRES_INIT_SCRIPT is None:
        raise ('Postgres init script must be provided (POSTGRES_INIT_SCRIPT variable)') # se ti parte sta eccezione, mi spiace per te pt.2
    return POSTGRES_INIT_SCRIPT