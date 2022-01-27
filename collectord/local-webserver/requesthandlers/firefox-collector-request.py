#!/usr/local/bin/python

# frontend wants a list of rows

import mongoconnector
from bson import json_util

# CONNECT TO MONGODB
collection = mongoconnector.connect_and_return_collection()

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

