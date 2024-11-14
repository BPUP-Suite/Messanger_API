import json

def getValue(data,title):

    jsonData = json.loads(data)
    return jsonData[title]

def dumps(dict):

    return json.dumps(dict)


def message(message_id,chat_id,text,sender,date):

    dict ={
        "message_id":message_id,
        "chat_id":chat_id,
        "text":text,
        "sender":sender,
        "date":str(date)
    }

    return dict

def chat(chat_id,user,messages):

    members = []
    members.append(user)

    return group_channel(chat_id,"",members,messages)

def localUser(handle,email,name,surname):

    dict={
        "handle":handle,
        "email":email,
        "name":name,
        "surname":surname
    }

    return dict


def group_channel(chat_id,name,members,messages):

    if name == "":
        dict ={
            "chat_id":chat_id
        }
    else:
        dict ={
            "chat_id":chat_id,
            "name":name
        }


    if len(members) != 0:

        list = []

        for member in members:
            
            dict_member ={
                "handle":member
            }
            list.append(dict_member)

        dict["users"] = list

    if len(messages) != 0:

        list = []

        for messageObj in messages:
            
            dict_message = message(messageObj.message_id,chat_id,messageObj.text,messageObj.sender,messageObj.date)

            list.append(dict_message)

        dict["messages"] = list

    return dict

def init_json(handle,email,name,surname,chats,groups,channels):

    dict ={
        'type':'init',
        "init":"True"
    }

    dict["localUser"] = localUser(handle,email,name,surname)

    # chat
    
    if len(chats) != 0:
        list = []

        for chatObj in chats:

            dict_chat = chat(chatObj.chat_id,chatObj.user,chatObj.messages)
            list.append(dict_chat)

        dict["chats"] = list

    return dict
