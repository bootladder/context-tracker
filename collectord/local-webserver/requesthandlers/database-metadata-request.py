#!/usr/local/bin/python


# Input is JSON to stdin
# Output is JSON to stdout

# Connects to mongo with the module imported
# in the current directory

import sys
import os
from bson import json_util
import json
import mongoconnector

def main():

  try:
    requestobject = dict()
  except Exception as e:
    print("Failed to parse stdin to JSON")

  try:
    queryobject = convert_to_query_object(requestobject)
  except Exception as e:
    print("Fail to convert to query object")
    sys.exit(1)


  try:
    queryresults = run_the_query(queryobject)
  except Exception as e:
    print("Fail to run the query")
    sys.exit(1)

  print(queryresults)


def convert_to_query_object(requestobject):
  entire_query_object = \
    {
      "$and":
        [
          {"source":"ash_collector_daemon.py"}
          ,
          {
            "$or":
              [
                {
                  "$and": and_queries
                } if and_queries else {}
                ,
                {
                  "$or": or_queries
                } if or_queries else {}
              ]
          }
        ]
    }
  return {}




def run_the_query(entire_query_object):

  # CONNECT TO MONGODB
  collection = mongoconnector.connect_and_return_collection()

  betterresults = collection.find(
    entire_query_object
  ) \
    .limit(10)

  return betterresults


def run_test():
  requestobject = dict()
  requestobject['command'] = "ssh"
  requestobject['pwd'] = "home"
  process_request_object(requestobject)

  # requestobject = {'$and': [{'$and': [{'source': 'ash_collector_daemon.py'}]}, {'$or': [{'command': {'$regex': '.*gszzz.*'}}, {'pwd': {'$regex': '.*szteve.*'}}]}]}
  # run_the_query(requestobject)
  print("wat popy")

if __name__ == "__main__":
  if True:
    main()
  else:
    run_test()
