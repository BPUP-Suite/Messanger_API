import os

SALT_PATH = "data/salt"

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

### SALT ###

def read_salt():

    SALT = None

    # search for SALT file
    try:
        with open(SALT_PATH,"r") as file:
            SALT = file.read()
    except Exception as e:
        print(str(e))
        return False
    
    if SALT is None:
        return False
    
    return SALT # return hex string

def write_salt(SALT):

    # write SALT file
    os.makedirs(os.path.dirname(SALT_PATH),exist_ok=True)
    with open(SALT_PATH,"w+") as file: # create a file
        file.write(SALT) # writes a hex string
