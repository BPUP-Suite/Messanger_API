import json


def message(message_id,text,sender,date):

    jsonMessage = "{"

    jsonMessage +=f'"message_id":{message_id},"text":{text},"sender":{sender},"date":{date}'

    jsonMessage +="}"

    return json.dumps(jsonMessage)

def chat(chat_id,user,messages):

    members = []
    members.append(user)

    return group_channel(chat_id,"",members,messages)

def localUser(handle,email,name,surname):

    jsonMessage = "{"

    jsonMessage +=f'"handle":{handle},"email":{email},"name":{name},"surname":{surname}'

    jsonMessage +="}"

    return json.dumps(jsonMessage)


def group_channel(chat_id,name,members,messages):

    jsonMessage = "{"

    jsonMessage +=f'"chat_id":{chat_id},name":{name}'

    if len(members) != 0:
        jsonMessage += ',"users":'

        jsonMessage += '{'

        first = True
        for member in members:
            
            if first:
                jsonMessage += '{'
                first = False
            else:
                jsonMessage += ',{'
                
            jsonMessage += f'"handle":{member}'
            jsonMessage += '}'

        jsonMessage += '},'

    if len(messages) != 0:
        jsonMessage += ',"messages":'

        jsonMessage += '{'

        first = True
        for messageObj in messages:
            if not first:
                jsonMessage += ','
            else:
                first = False

            jsonMessage += message(messageObj.message_id,messageObj.text,messageObj.sender,messageObj.date)

        jsonMessage += '}'

    jsonMessage +="}"

    return json.dumps(jsonMessage)

def init_json(handle,email,name,surname,chats,groups,channels):

    jsonMessage = "{"

    # init initial message

    jsonMessage +=f'"init":true,'

    # local user

    jsonMessage += '"localuser":'
    jsonMessage += localUser(handle,email,name,surname)

    # chat
    
    if len(chats) != 0:
        jsonMessage += ','
        jsonMessage += '"chats":'
        first = True
        for chatObj in chats:

            if not first:
                jsonMessage += ','
            else:
                first = False

            jsonMessage += chat(chatObj.chat_id,chatObj.user,chatObj.messages)
        jsonMessage +="}"

    jsonMessage +="}"

    return json.dumps(jsonMessage).replace("\\","")

def getValue(data,title):

    jsonData = json.dumps(data)
    return jsonData[title]