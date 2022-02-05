#!/usr/local/bin/python

# Frontend wants a list of rows containing shell history
# By default it will be the last 10 entries

# Input is JSON to stdin
# Output is JSON to stdout

import sys
from bson import json_util
import json
import mongoconnector

# Check STDIN
data = sys.stdin.readlines()[0]

try:
  # print(data)
  requestobject = json.loads(data)
  # print(requestobject)
except Exception as e:
  print("Failed to parse stdin to JSON")

# CONNECT TO MONGODB
collection = mongoconnector.connect_and_return_collection()

# QUERY THE DB
try:

  commandquery = {}
  if 'commandsearchquery' in requestobject and \
    requestobject['commandsearchquery'] != "":
    commandquery = {"command":{"$regex":".*%s.*"%(requestobject['commandsearchquery'])}}

  pwdquery = {}
  if 'pwdsearchquery' in requestobject and \
        requestobject['pwdsearchquery'] != "":
    pwdquery = {"pwd": {"$regex":".*%s.*"%(requestobject['pwdsearchquery'])}}

  entire_query_object = \
    {
      "$and":
        [
          {"source":"ash_collector_daemon.py"}

        ]
      # ,
      # "$or":
      #   [
      #     # commandquery
      #     # ,pwdquery
      #   ]gw

    }

  # print(entire_query_object)

  resultslist = []
  betterresults = collection.find(
    entire_query_object
    )\
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


# Convert result list into JSON
# print it to stdout
try:
  responsestring = json_util.dumps(resultslist, indent=2)
  print(responsestring)
except Exception as e:
  print(e)
  print("fail dumps")


