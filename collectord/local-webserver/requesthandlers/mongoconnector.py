from pymongo import MongoClient

import os

mongourl = ""
with open('mongourl.txt') as f:
    mongourl = f.read()

mongodbname = ""
with open('mongodbname.txt') as f:
    mongodbname = f.read()

mongocollectionname = ""
with open('mongocollectionname.txt') as f:
    mongocollectionname = f.read()


# ""
# ''
# ""

def connect_and_return_collection():
    try:
        client = MongoClient(mongourl)
        db = client[mongodbname]
        collection = db[mongocollectionname]
        return collection
    except Exception as e:
        print("fail to connect to mongodb")
        print(e)