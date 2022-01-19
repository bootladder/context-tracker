from pymongo import MongoClient

def connect_and_return_collection():
    try:
        client = MongoClient("bootladder.com:9017")
        db = client['steve_context_tracker']
        collection = db["common_vectors"]
        return collection
    except Exception as e:
        print("fail to connect to mongodb")
        print(e)