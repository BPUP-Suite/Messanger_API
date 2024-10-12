import json


def message(chat_id,text,sender,date):

    jsonMessage = "{"

    jsonMessage +=f'"chat_id":{chat_id},"text":{text},"sender":{sender},"date":{date}'

    jsonMessage +="}"

    return json.dumps(jsonMessage)