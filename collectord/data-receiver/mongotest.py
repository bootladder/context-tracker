#!/usr/bin/python

from pymongo import MongoClient

client = MongoClient("bootladder.com:9017")

a = client.server_info()
print(a)

db = client['steve_context_tracker']

collection = db["common_vectors"]

item_1 = {
"_id" : "U1IT00003",
"item_name" : "Blender",
"max_discount" : "10%",
"batch_number" : "RR450020FRG",
"price" : 340,
"category" : "kitchen appliance"
}

item_2 = {
"_id" : "U1IT00005",
"item_name" : "Egg",
"category" : "food",
"quantity" : 12,
"price" : 36,
"item_description" : "brown country eggs"
}

try:
  collection.insert_many([item_1,item_2])
except Exception as e:
  print(e)

print('doine')



item_details = collection.find()
for item in item_details:
    # This does not give a very readable output
    print(item)


betterresults = collection.find({"_id":"U1IT00003"})
for results in betterresults:
  print(results)
