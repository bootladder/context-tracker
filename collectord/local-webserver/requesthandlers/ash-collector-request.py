#!/usr/bin/python

# frontend wants a list of rows
# By default it will be the last 10 entries

# ONLY PRINT THE RESPONSE JSON !!!!

import sys
from bson import json_util
import json
import mongoconnector

# CHECK ARGS (first arg is search query TODO NO)
# print(sys.argv[1])
# sys.exit(0)
# searchquery = ""
# if len(sys.argv) > 1:
#   searchquery = sys.argv[1]


data = sys.stdin.readlines()[0]
# print(data)
requestobject = json.loads(data)
# print(requestobject)

# CONNECT TO MONGODB
collection = mongoconnector.connect_and_return_collection()

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
        {"command":{"$regex":".*%s.*"%(requestobject['commandsearchquery'])}}
        ,{"pwd": {"$regex":".*%s.*"%(requestobject['pwdsearchquery'])}}
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


