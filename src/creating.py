from pymongo import MongoClient
from src.config import DBURL
from src.errorHandling import APIError
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask
from src.app import app



client = MongoClient("mongodb://localhost:27017/myapi")
db = client.get_database()

"""
client = MongoClient(DBURL)
print(f"connected to {DBURL}")
db = client.get_database()
"""

user_collec=db["users"]
chat_collec=db["chats"]
mess_collec=db["messages"]
print("hello")
print(DBURL)

@app.route("/")
def hello():
    return f"Welcome to my api"


@app.route("/user/create/<username>")
def newUser(username):
    users=user_collec.distinct("username")
    if username in users:
        raise APIError ("User already exists")
    else:
        user={"username":username}
        user_collec.insert_one(user)
    res=user_collec.find_one({"username":username})
    return dumps(res)


@app.route("/chat/create/<chatname>")
def newChat(chatname):
    chats=chat_collec.distinct("chat_name")
    if chatname in chats:
        raise APIError ("Chat name already exists, please insert another one")
    else:
        infochat={"chat_name":chatname}
        chat_collec.insert_one(infochat)
        res=chat_collec.find_one({"chat_name":chatname},{"chat_name":1,"_id":1})
        return dumps(res)


@app.route("/chat/<chatname>/adduser/<user>")
def addUser(chatname,user):
    chat_id=chat_collec.find_one({"chat_name":chatname},{"_id":1})
    if len(chat_id)==0:
        raise APIError ("Chat doesn't exist, please check your spelling")
    else:
        user_id=user_collec.find_one({"username":user},{"_id":1})
        print(user_id)
        chat_collec.update({ "_id":chat_id["_id"]},{ "$push":{ "participants":user_id["_id"]}})
        res=chat_collec.find_one({"chat_name":chatname},{"participants":1})
        return dumps(res)
   


@app.route("/chat/<chatname>/user/<username>/addmessage/<message>")
def newMessage(chatname,username,message):
    chat_id=chat_collec.find_one({"chat_name":chatname},{"_id":1})
    print(chat_id)
    if len(chat_id)==0:
        raise APIError ("Chat doesn't exist, please check your spelling")
    user_id=user_collec.find_one({"username":username},{"_id":1})
    print(user_id)
    if user_id==0:
        raise APIError ("Username doesn't exist, please check your spelling")
    else:
        message_info={"user":user_id["_id"], "chat_name": chatname, "chat":chat_id["_id"], "message":message}
        mess_collec.insert_one(message_info)
        res=mess_collec.find_one({"message":message})
        return dumps(res)


@app.route("/chat/<chatname>/list")
def getMessages(chatname):
    res=mess_collec.find({"chat_name":chatname},{"chat_name":1,"message":1})
    lista=list(res)
    
    a=[]
    for i in range(len(lista)):
        a.append(lista[i]["message"])
    return dumps(a)
   