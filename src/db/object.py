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
  def __init__(self,chat_id,text,sender):
    self.chat_id = chat_id
    self.text = text
    self.sender = sender
    self.date = datetime.now()

class Chat:
  def __init__(self,user1,user2):
    self.user1 = user1
    self.user2 = user2

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
  