#!/usr/bin/python

# frontend wants a list of rows
# By default it will be the last 10 entries

# ONLY PRINT THE RESPONSE JSON !!!!

import sys
from pymongo import MongoClient
from bson import json_util

# CHECK ARGS (first arg is search query TODO NO)
searchquery = ""
if len(sys.argv) > 1:
  searchquery = sys.argv[1]

# CONNECT TO MONGODB
try:
  client = MongoClient("bootladder.com:9017")
  db = client['steve_context_tracker']
  collection = db["common_vectors"]
except Exception as e:
  print("fail to connect to mongodb")
  print(e)

# QUERY THE DB
try:
  resultslist = []
  betterresults = collection.find(
    {
      "$and":
        [
          {"source":"ash_collector_daemon.py"}

        ]
      ,
      "$or":
      [
        {"command":{"$regex":".*%s.*"%(searchquery)}}
        ,{"pwd": {"$regex":".*%s.*"%(searchquery)}}
      ]

    })\
    .limit(10)
  for result in betterresults:

    #  KLUDGE VALIDATE THIS DATA CLEAN THE DAMN DATA
    if 'timestamp' not in result:
      result['timestamp'] = 0
    resultslist.append(result)
    # print(result)
except Exception as e:
  print("fail to query db")
  print(e)



try:
  responsestring = json_util.dumps(resultslist, indent=2)
  print(responsestring)
except Exception as e:
  print(e)
  print("fail dumps")


