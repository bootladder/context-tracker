#!/usr/local/bin/python

# Frontend wants a list of rows containing shell history
# By default it will be the last 10 entries

# Input is JSON to stdin
# Output is JSON to stdout

# Connects to mongo with the module imported
# in the current directory

import sys
from bson import json_util
import json
import mongoconnector

def main():
  # Check STDIN
  data = sys.stdin.readlines()[0]

  try:
    # print(data)
    requestobject = json.loads(data)
    # print(requestobject)
  except Exception as e:
    print("Failed to parse stdin to JSON")


  process_request_object(requestobject)


def process_request_object(requestobject):

  # CONSTRUCT THE QUERY FROM THE REQUEST OBJECT
  try:


    if 'command' in requestobject and \
            requestobject['command'] != "":
      commandquery = {"command":{"$regex":".*%s.*"%(requestobject['command'])}}
    else:
      commandquery = {}

    if 'pwd' in requestobject and \
            requestobject['pwd'] != "":
      pwdquery = {"pwd": {"$regex":".*%s.*"%(requestobject['pwd'])}}
    else:
      pwdquery = {}



    and_queries = []
    or_queries = [{"failing":"initial value"}]

    # source is always required

    if 'commandrequired' in requestobject:
      and_queries.append(commandquery)
    else:
      or_queries.append(commandquery)

    if 'pwdrequired' in requestobject:
      and_queries.append(pwdquery)
    else:
      or_queries.append(pwdquery)


    if len(and_queries) == 0:
      and_queries = [{"failing":"initial value"}]

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



            # {"$and": and_queries}
            # ,
            # { "$or": or_queries }
          ]
      }

    # print(entire_query_object)

    resultslist = run_the_query(entire_query_object)

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




def run_the_query(entire_query_object):

  # CONNECT TO MONGODB
  collection = mongoconnector.connect_and_return_collection()


  resultslist = []
  betterresults = collection.find(
    entire_query_object
  ).sort('timestamp',-1) \
    .limit(10)

  for result in betterresults:
    #  KLUDGE VALIDATE THIS DATA CLEAN THE DAMN DATA
    if 'timestamp' not in result:
      result['timestamp'] = 0
    resultslist.append(result)

    # FOR TESTING
    # print(result)

  return resultslist


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
