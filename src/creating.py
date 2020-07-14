from pymongo import MongoClient
from src.config import DBURL
from src.errorHandling import APIError
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask
from src.app import app



client = MongoClient("mongodb://localhost:27017/myapi")
db = client.get_database()


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
    res=user_collec.find_one({"username":username},{"username":1})
    return dumps(res)


@app.route("/chat/create/<chatname>")
def newChat(chatname):
    chats=chat_collec.distinct("chat_name")
    if chatname in chats:
        raise APIError ("Chat name already exists, please insert another one")
    else:
        infochat={"chat_name":chatname}
        chat_collec.insert_one(infochat)
        res=chat_collec.find_one({"chat_name":chatname},{"_id":1,"chat_name":1})
        return dumps(res)


@app.route("/chat/<chatname>/adduser/<user>")
def addUser(chatname,user):
    chat_id=chat_collec.find_one({"chat_name":chatname},{"_id":1})
    if len(chat_id)==0:
        raise APIError ("Chat doesn't exist, please check your spelling")
    else:
        user_id=user_collec.find_one({"username":user},{"_id":1})
        chat_collec.update({ "_id":chat_id["_id"]},{ "$push":{ "participants":user_id["_id"]}})
        res=chat_collec.find_one({"chat_name":chatname},{"participants":1})
        users=[user_collec.find_one({"_id":part},{"_id":0,"username":1})["username"] for part in res["participants"]]
        dic={"chat_name":chatname,"participants":users}
        return dumps(dic)
   


@app.route("/chat/<chatname>/user/<username>/addmessage/<message>")
def newMessage(chatname,username,message):
    chat_id=chat_collec.find_one({"chat_name":chatname},{"_id":1})
    if len(chat_id)==0:
        raise APIError ("Chat doesn't exist, please check your spelling")
    user_id=user_collec.find_one({"username":username},{"_id":1})
    if user_id==0:
        raise APIError ("Username doesn't exist, please check your spelling")
    else:
        message_info={"user":user_id["_id"],"username":username, "chat":chat_id["_id"],"chat_name": chatname, "message":message}
        mess_collec.insert_one(message_info)
        res=mess_collec.find_one({"message":message},{"_id":0})
        dic={"chat_name":chatname,"username":username,"message":res["message"]}
        return dumps(dic)


@app.route("/chat/<chatname>/list")
def getMessages(chatname):
    res=mess_collec.find({"chat_name":chatname},{"chat_name":1,"message":1})
    lista=list(res)
    a=[lista[i]["message"] for i in range(len(lista))]
    dic={"chat_name":chatname,"message":a}
    return dumps(dic)
   