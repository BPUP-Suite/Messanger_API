# Messanger_API

    DOCUMENTAZIONE NON AGGIORNATA (aggiornata oggi il 21/10/24 ma ancora non completa)
    DEVO DECISAMENTE SISTEMARLO IL 25 LO FACCIO

# INDICE

websocket docs : (websocket)
To-dos : (TO DO)

    
## TO DO ##

aggiungi conn.rollback() a tutti gli statement di insert into che potrebbe dare problemi
sistema la documentazione sottostante con le cosine nuove

sposta il metodo send messages dentro websocket
da capire come evitare che il file json sia pieno di backslash (giuro non capisco che qualcuno mi aiuti)

###########################################
# websocket

# init
# send_message
# ack
# update

...

###########################################
####

API per l`app di messaggistica

Se vuoi usarla ti basta clonare la repo, cambiare il nome a example.env in .env, cambiarne i valori e utilizzare docker-compose per inizializzare il tutto

*Configurazione di Nginx Proxy Manager* ??? ve la dò un giorno (anche perchè uso la versione web decisamente più facile da gestire, finirò probabilmente per mettere una semplice guida alla configurazione piuttosto che i file veri e propri)


# DOCS


## DOCKER


- PostgreSQL (database vero e proprio)
- PGAdmin (gestione del database visuale [l'SQL mi fa piangere]) DA CAMBIARE (giuro che non riesco ad usarlo, non capisco un cazzo)
- Nginx Proxy Manager (serve un certificato, fidati, l`HTTPS è sacro)
- Il programmino Python (per l'API e l'accesso al db)

I dati di tutti i container sono dentro /data/


## DB 


Entitá:

    - users
    - ...
    (anche questo da completare ma non ricordo db :D )


## API


Tutto dentro /src/


### DB


#### database.py


Gestisce l'intero reparto di accesso al database, dalla sua creazione, all'autenticazione e alla lettura, inserimento e modifica delle righe.
(da sistemare anche questo tropa roba e io no volia)


#### object.py


Qui sono definiti tutti gli oggetti utilizzati per passare parametri tra i vari script


#### jsonBuilder.py


Presenti tutti i metodi per la manipolazione di json:

    - trasformazione da oggetti messages,chats,groups,channels a file json
    - creazione del file gigantesco json che viene richiesto all'avvio dell'applicazione (che richiama i precedenti metodi)
    - metodo per l'ottenimento di singoli value data una stringa json e il suo nome


### LOGGER


Gestione e stampa dei log (fatta sia su main che su db) per facilitare il debugging (mi ha salvato la vita 24234 volte, siano lodati i log)
La stampa su file viene eseguita su file log.txt dentro /src/logs/ (anche se su docker non riesco a fare un bind della cartella, quindi per vedere il file bisogna leggere tramite linea di comando su terminal del container [se qualcuno sa risolvere sto bug, pls help sono stupido -UPDATE- ho sistemato, era un problema di percorso :D] )

Metodi:
DA AGGIUNGERE

### SECURITY


#### auth.py


Semplicemente cifra, decifra le password presenti nel db tramite la libreria bcrypt e controlla che l'API Key fornita, venga inserita ed esista nel db. (un giorno ti riscriverò meglio :( )


#### envManager.py


Recupera i valori delle variabili ambientali e dei file presenti all'interno del progetto:

    - .env:
        - POSTGRES_DB
        - POSTGRES_USER
        - POSTGRES_PASSWORD
        - POSTGRES_HOST
        - POSTGRES_PORT
        - PGADMIN_DEFAULT_EMAIL
        - PGADMIN_DEFAULT_PASSWORD
    - init.sql (dentro /src/db/), che contiene il codice SQL di inizializzazione del db

    - salt (dentro /src/db), che contiene un parametro di sicurezza per rendere più sicura la crittografia della password (viene generato una sola volta al primo start, senza questo file decifrare le password presenti nel database è impossibile [quindi attenzione a non perderlo] ) 

#### encrypter.py

Prima insieme alla classe envManager.py, poi separato per problemi di import.
    
    Recupera il salt dal file (usando envManager) e lo usa per cifrare le password richieste e confermare eventuali hash

### MAIN


Utilizzo principale della libreria di FastAPI (sia lodato il cielo che non mi tocca capire come sviluppare una RestAPI a manina :D )

Per la documentazione relativa a questa parte basta far partire il container ed entrare all'indirizzo localhost:8000/docs (indicativo, non è detto sia localhost per voi, potrebbe cambiare IP, porta, non la folder :D ) (penserò anche a lasciare disponibile la pagina html in qualche folder, così non me tocca far partire il container ogni volta -UPDATE 21/10/24 e ancora no fatto-)
Aggiunta anche la sezione relativa a websocket all'inizio del file
