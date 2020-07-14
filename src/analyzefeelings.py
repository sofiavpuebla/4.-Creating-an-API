from pymongo import MongoClient
from src.errorHandling import APIError, errorHandler
from src.app import app
from bson.json_util import dumps
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src.config import DBURL, PORT


nltk.download("vader_lexicon")

client = MongoClient(DBURL)
db = client.get_database()

user_collec=db["users"]
chat_collec=db["chats"]
mess_collec=db["messages"]


@app.route("/chat/<chatname>/sentiment")
@errorHandler
def getFeeling(chatname):
    chats=chat_collec.distinct("chat_name")
    if chatname not in chats:
        raise APIError ("Chat doesn't exist, please check your spelling.")
    else:
        res=list(mess_collec.find({"chat_name":chatname},{"_id":0,"message":1}))
        sia=SentimentIntensityAnalyzer()
        print(res)
        messages=[res[i]["message"] for i in range(len(res))]
        negative=sum([sia.polarity_scores(message)["neg"] for message in messages])/len(messages)
        positive=sum([sia.polarity_scores(message)["pos"] for message in messages])/len(messages)
        return dumps({"positive_sentiment":positive,"negative_sentiment":negative})
        
