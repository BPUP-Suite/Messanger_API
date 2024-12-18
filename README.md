# Messanger_API

    DOCUMENTAZIONE NON AGGIORNATA (aggiornata oggi il 03/12/24 ma ancora non completa)
    da togliere tutta la documentazione del codice, solo docker, nginx,(nella parte di installation)  api e WEBSOCKET, massimo il database

    Aggiornamento:
    PGADMIN E NGINX RIMARRANNO SOLO PER LA FASE DI TESTING
    successivamente si utilizzerà una soluzione client e una vpn per accedere al db
                                  e nginx su una soluzione più estesa vista la presenza di più servizi

# INDICE

- [To-dos](#TODO)
- [Docs](#DOCS)
    - [Docker](#DOCKER)
    - [Database](#DATABASE)
    - [API](#API)
      - [access](#access)
      - [signup](#signup)
      - [login](#login)
      - [check-handle-availability](#check-handle-availability)
      - [get-user-id](#get-user-id)
    - [WebSocket](#WebSocket)
      - [init](#init)
      - [send_message](#send_message)
      - [receive_message](#receive_message)
      - [create_chat](#create_chat)
      - [ack](#ack)
      - [update](#update)
    - [Admin][#Admin]



     
## TODO

aggiungi conn.rollback() a tutti gli statement di insert into che potrebbe dare problemi
sistema la documentazione sottostante con le cosine nuove

inserisci tantissime tipologie di controlli:
  1) su campi mancanti necessari (che restituisce la tipologia di errore in "reason" e magari vedere se impementere dei codici di errore personalizzati per l'app o usare quelli html)
  2) payload troppo grandi
  3) testi troppo lungi (send_message -> text, signup -> qualsiasi campo, login -> user | pass, check-handle )
    da capire i limiti, per ora:
      text: 2056
      psw: 256 
      handle: 64
      nome,cognome,... ???

  DA MODIFICARE LA DOCUMENTAZIONE CON L'AGGIUNTA DI UN DIZIONARIO FINALE PER EVITARE CONTINUE RIPETIZIONI NELLA DEFINIZIONE DEI PARAMETRI (+ IP ADDRESS NEGLI EXAMPLE DI API)

##

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


## DATABASE


Entitá:

    - users
    - ...
    (anche questo da completare ma non ricordo db :D )

## CODICE (da togliere)


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

## API

LA SEGUENTE DOCUMENTAZIONE ANCHE SE PARZIALMENTE AGGIORNATA NON RISPECCHIO IL CODICE ATTUALE IN QUANDO SONO NECESSARIE ULTERIORI MODIFICHE PER GARANTIRE UN'OMOGENIETA' DEI TITOLI USATI PER LE VARIABILI MA ANCHE UNA GESTIONE PIU' ACCURATA DEGLI ERRORI (CON ANCHE MESSAGGIO DI ERRORE INCLUSO)

### access

Permette di capire se una determinata e-mail è stata già utilizzata, ritornando il tipo di azione che l'utente deve compiere per accedere alla piattaforma.

#### Richiesta

```
{
  "email": {email}
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {email} = indirizzo e-mail della forma name@domain.example

#### Risposta

##### - 1. Errore

```
{
  "access_type": false
}
```

Richista fallita per uno dei seguenti motivi:

+ Internal Server Error

##### - 2. 

```
{
  "access_type": {access_type}
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {access_type} = tipo di accesso che dovrà eseguire l'utente:
 1) signup
 2) login

### signup

Permette la registrazione dell'utente sulla piattaforma.

#### Richiesta

```
{
  "email": {email},
  "name": {name},
  "surname": {surname},
  "handle": {handle},
  "password": {password}
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {email} = indirizzo e-mail della forma name@domain.example
+ {name} = nome dell'utente
+ {surname} = cognome dell'utente
+ {handle} = nickname UNICO dell'utente (da usare #check-handle-availability per verificare che sia disponibile)
+ {password} = !!!!DA INSERIRE I PARAMETRI MINIMI PER AVERE UNA PASS SICURA!!! (con conseguente aggiunta di tutti gli errori possibili specifici per ogni richiesta)

#### Risposta

##### - 1. Errore

```
{
  "signed_up": false
}
```

Richista fallita per uno dei seguenti motivi:

+ E-mail già registrata
+ Handle già utilizzato
+ Password non abbastanza sicura
+ Internal Server Error

##### - 2. 

```
{
  "signed_up": true
}
```

### login

Permette l'accesso dell'utente già registrato sulla piattaforma.

#### Richiesta

```
{
  "email": {email},
  "password": {password}
}
```

Esempio: 

```
{}/user/action/login?email=name@domain.example&password=Password123!
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {email} = indirizzo e-mail della forma name@domain.example
+ {password} = password associata all'indirizzo e-mail

#### Risposta

##### - 1. Errore

```
{
  "logged_in": false,
  "api_key": None
}
```

Richista fallita per uno dei seguenti motivi:

+ E-mail non registrata
+ Combinazione e-mail e password non esiste
+ Internal Server Error

##### - 2. 

```
{
  "logged_in": true,
  "api_key": {api_key}
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {api_key} = stringa unica di caratteri per ogni utente che permette l'accesso al websocket

### check-handle-availability

Permette di capire se un determinato handle è già stato utilizzato o meno.

#### Richiesta

```
{
  "handle": {handle}
}
```

Esempio: 

```
{}/user/action/check-handle-availability?handle=example
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {handle} = nickname UNICO dell'utente

#### Risposta

##### - 1. 

```
{
  "handle_available": {handle_available}
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {handle_available} = valore booleano con i seguenti significati:
  1) true: handle NON utilizzato e quindi DISPONIBILE
  2) false: handle UTILIZZATO e quindi NON disponibile (inoltre potrebbe anche indicare la presenza di errori lato server)

### get-user-id

Permette l'accesso dell'utente già registrato sulla piattaforma.

#### Richiesta

```
{
  "api_key":{api_key}
}
```

Esempio: 

```
{}/user/action/get-user-id?api_key=63iuhgfs7yUHBFYID79gfdskjnsd89...
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {api_key} = api key dell'utente ottenuta tramite il metodo [login](#login)

#### Risposta

##### - 1. Errore

```
{
  "user_id": None
}
```

Richista fallita per uno dei seguenti motivi:

+ api key non esiste
+ Internal Server Error

##### - 2. 

```
{
  "user_id": {user_id}
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {user_id} = id unico dell'utente (permette l'accesso al [websocket](#Websocket))

## WebSocket

#### Connessione

Usare l'indirizzo:

```
wss://{indirizzo}/ws/{user_id}/{api_key} 
```
(richiede ovviamente un certificato SSL, altrimenti usare il l'alternativa ws [NON SICURA] )

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {indirizzo} = bpup.messanger.it (ufficiale)
+ {user_id} = sequenza di numeri ottenuta da [get_user_id](#get_user_id)
+ {api_key} = sequenza di caratteri ottenuta da [login](#login)

### init

Per inizializzare il database locale del client, ritorna una file json con tutte le informazioni relative all'utente (basiche[come handle,nome,cognome,...], chats(tutte le chat personali, gruppi e canali con i relativi chat_id, membri, ...), messages (per ogni chat analizzata))

#### Richiesta

```
{
  "type": "init",
  "api_key":{api_key}
}
```

#### Risposta

##### - 1. Errore

```
{
  "type": "init",
  "init": "False"
}
```

Richista fallita per uno dei seguenti motivi:

+ api_key errata
+ Internal Server Error

##### - 2. 

```
{
  "type": "init",
  "init": "True",
  "localUser": "True", ... TBD (NON COMPLETA)
}
```

### send_message

Per mandare un messaggio ad una qualsiasi chat (può anche creare una chat privata con un altro utente nel caso non esista se specificato il receiver [handle] )

#### Richiesta

```
{
  "type": "send_message",
  "text":{text},
  "chat_id":{chat_id},
  "salt":{salt} # OPTIONAL
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {text} = semplicissimo testo (max 2056 caratteri)
+ {chat_id} = sequenza di numeri ottenuta da [init](#init), da [update](#update)/da questo stesso metodo, alla creazione di una nuova chat
+ {salt} = utilizzato per calcolare l'hash del messaggio (utilizzando il testo) e ritornandolo al client per verificare che il messaggio riferito alle informazioni sia lo stesso

#### Risposta

##### - 1. Errore

```
{
  "type": "send_message",
  "send_message": "False"
}
```

Richista fallita per uno dei seguenti motivi:

+ testo troppo lungo
+ chat_id non esiste
+ non si ha accesso alla chat richiesta
+ Internal Server Error

##### - 2. 

```
{
  "type": "send_message",
  "send_message": "True",
  "date": {date_time},
  "message_id": {message_id},
  "hash": {hash}
}
```

I campi contrassegnati da {valore} saranno sostituiti secondo l'esempio:

+ {date_time} = ora locale (ottenuta server-side) della forma AAAA-MM-GG HH-MM-SS.MSMSMS (esempio: 2024-11-20 14:06:08.116420)
+ {message_id} = sequenza di numeri ottenuta da [init](#init), da [update](#update)/da questo stesso metodo, all'invio di un nuovo messaggio
+ {hash} = valore calcolato a partire dal testo del messaggio per identificare univocamente il messaggio quando viene mandata la conferma di invio del messaggio con relativi dati extra forniti dal server al client (in pratica è un message_id temporaneo usato dal client generato sia lato client che lato server). Viene calcolato solo se il {salt} nella richiesta viene mandato.

### receive_message

Riceve messaggi mandati sia da altri utenti che da un'altra websocket attiva dello stesso utente

#### Richiesta

No

#### Risposta

##### - 1. 

```
{
  "type": "receive_message",
  "message_id": {message_id}
  "chat_id":{chat_id},
  "text":{text},
  "sender":{sender},
  "date": {date_time}
}
```

I campi contrassegnati da {valore} saranno sostituiti secondo l'esempio:

da fare perchè sincero no voglia (al massimo conviene fare tipo un dictionary alla fine con la spiegazione generale e rimandare a quello ogni volta che viene nominato uno di questi termini, cosa molto frequente)

### create_chat

Per creare una qualsiasi chat (che sia personale, un gruppo o un canale [per ora funzionano solo le personali!!!!!!!!!!])

#### Richiesta

```
{
  "type": "create_chat",
  "chatType":{chatType},
  "handle":{handle} # OPTIONAL
}
```

I campi contrassegnati da {valore} devono essere sostituiti secondo l'esempio:

+ {chatType} = tipologia della chat da create, può essere:
  + personal -> per le chat personali (NECESSITA DEL CAMPO {handle} per identificare il secondo utente)
  + group -> non 
  + channel -> esistono (per ora)

#### Risposta

##### - 1. Errore

```
{
  "type": "create_chat",
  "create_chat": "False"
}
```

Richista fallita per uno dei seguenti motivi:

+ Internal Server Error
+ ???

##### - 2. 

```
{
  "type": "create_chat",
  "create_chat": "True",
  "chat_id": {chat_id}
}
```

I campi contrassegnati da {valore} saranno sostituiti secondo l'esempio:

+ {chat_id} = da fare il mega dictionary

### ack

TDB

### update

TDB

## Admin

DA aggiornare, conterrà tutte le pagine e credeziali di accesso per gli amministratori


