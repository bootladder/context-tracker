from pymongo import MongoClient

import os

mongourl = ""
with open('mongourl.txt') as f:
    mongourl = f.readline().strip()

mongodbname = ""
with open('mongodbname.txt') as f:
    mongodbname = f.readline().strip()

mongocollectionname = ""
with open('mongocollectionname.txt') as f:
    mongocollectionname = f.readline().strip()

print(f"Connecting to db...\nurl: {mongourl} dbname: {mongodbname} collectionname: {mongocollectionname}")
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
