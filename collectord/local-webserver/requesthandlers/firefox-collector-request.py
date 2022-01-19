#!/usr/bin/python

# frontend wants a list of rows

from pymongo import MongoClient
from bson import json_util

client = MongoClient("bootladder.com:9017")
db = client['steve_context_tracker']
collection = db["common_vectors"]

resultslist = []

betterresults = collection.find({"source":"firefox_collector_daemon.py"})
for result in betterresults:
    resultslist.append(result)
    # print(result)

try:
    responsestring = json_util.dumps(resultslist, indent=2)
except Exception as e:
    print(e)
    print("fail dumps")
# print("wat")
print(responsestring)
#print("hellowtf")

