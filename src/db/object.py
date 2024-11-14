from datetime import datetime

class User:
  def __init__(self,email,name,surname,handle,password):
    self.email = email
    self.name = name
    self.surname = surname
    self.handle = handle
    self.password = password

class LoginUser:
  def __init__(self,email,password):
    self.email = email
    self.password = password

class Message:
  def __init__(self,chat_id,text,sender,date):
    self.chat_id = chat_id
    self.text = text
    self.sender = sender
    if date == None:
      self.date = datetime.now()
    else:
      self.date = date

class MessageJson:
  def __init__(self,message_id,chat_id,text,sender,date):
    self.message_id = message_id
    self.chat_id = chat_id
    self.text = text
    self.sender = sender
    self.date = date

class Chat:
  def __init__(self,user1,user2):
    self.user1 = user1
    self.user2 = user2

class ChatJson:
  def __init__(self,chat_id,user,messages):
    self.chat_id = chat_id
    self.user = user
    self.messages = messages

class Group:
  def __init__(self,handle,name,description):
    self.handle = handle
    self.name = name
    self.description = description

class FileUpload:
  def __init__(self,handle,type,file):
    self.handle = handle
    self.type = type
    self.file = file

class FileDownload:
  def __init__(self,data,name,type):
    self.data = data
    self.name = name+"."+type
    self.type = type
  