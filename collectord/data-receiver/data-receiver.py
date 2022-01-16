#!/usr/bin/python
#
# Data Receiver
# Read from socket, assume it is JSON,
# Make the data available for 2 consumers:  Local Web App and Central Collector
#
# Validate the data has a common vector format
# Data Receiver itself has access/maintenance of new dimensions added.

# For Local Web App,
#    store the JSON into a DATABASE
#
# For Central Collector, HTTP request the payloads up.

# 2022-01-13 adding central mongo store

#
import time
import json
import jsonlines
import zmq
import glob
import sqlite3
import sys


socket = 0  #zmq socket

common_vector_version = '0.0.1'

# connect to local db
path_to_commonvector_db = "/home/*/.context-tracker/commonvector.db"
globresult = glob.glob(path_to_commonvector_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)
dbfilename = globresult[0]
conn = sqlite3.connect(dbfilename)
print("connected to local db")

# connect to central db
from pymongo import MongoClient
centraldbclient = MongoClient("bootladder.com:9017")
db = centraldbclient['steve_context_tracker']
collection = db["common_vectors"]
print("connected to central db")

def c2c_ash_collector_0_0_1(collection_object):
  print("watffff")
  commonvector = dict()
  commonvector['version'] = common_vector_version
  commonvector['source'] = collection_object['source']
  commonvector['sourceversion'] = collection_object['version']
  commonvector['command'] = collection_object['command']
  commonvector['pwd'] = collection_object['cwd']

  # timestamp is not in this version
  if collection_object.has_key('starttime')
      print("using starttime from source")
      commonvector['timestamp'] = collection_object['starttime']
  commonvector['timestamp'] = int(time.time())
  return commonvector

def c2c_firefox_collector_0_0_1(collection_object):
    print("c2c firefox 0 0 1")
    commonvector = dict()
    try:
        commonvector['version'] = common_vector_version
        commonvector['source'] = collection_object['source']
        commonvector['sourceversion'] = collection_object['version']
        commonvector['url'] = collection_object['url']

        # timestamp is last_visit_date
        # commonvector['timestamp'] = int(time.time())
        commonvector['timestamp'] = collection_object['last_visit_date']

    except Exception as e:
        print(e)
        print("unable to parse incoming vector")

    print("c2c OK")
    return commonvector

# Table of conversions
conversion_funcs = dict()
conversion_funcs['ash_collector_daemon.py'] = dict()
conversion_funcs['ash_collector_daemon.py']['0.0.1'] = c2c_ash_collector_0_0_1
conversion_funcs['firefox_collector_daemon.py'] = dict()
conversion_funcs['firefox_collector_daemon.py']['0.0.1'] = c2c_firefox_collector_0_0_1


def convert_to_common_vector(collection_object):
  print("derp")
  # validate object
  data_source = collection_object['source']
  data_version = collection_object['version']
  print("herp", data_source, data_version)

  # make sure there is a handler defined TODO
  vector = dict()
  try:
      conversion_func = conversion_funcs[data_source][data_version]
      vector = conversion_func(collection_object)
  except Exception as e:
      print("no conversion function defined for incoming data")
      print("this is the collection_object")
      print(collection_object)

  return vector


def insert_common_vector_into_local_storage(vector):
    print("insert_common_vector_into_local_storage")
    try:
        print("clearly sqlite local storage is flawed because")
        print("excessive maintenance of common vector schema")
        # rowlist = [vector['version'], vector['pwd'], vector['command']]
        # cursor = conn.execute("INSERT INTO commonvector values (?,?,?)", rowlist)
        # conn.commit()
    except Exception as e:
        print(e)
        print("fail local storage")

def insert_common_vector_into_central_storage(vector):
    print("insert_common_vector_into_central_storage")
    try:
        collection.insert_one(vector)
        print("done")
    except Exception as e:
        print(e)
        print("fail central storage)")



def main():
  setup_zmq_socket()

  while True:
      #  Wait for any collectors to send data
      message = socket.recv()
      print("\n\nData Collector: Received msg.")

      try:
        collection_object = json.loads(message)
        commonvector = convert_to_common_vector(collection_object)

        print("Common Vector ready for storage: ")
        print(commonvector)
        insert_common_vector_into_local_storage(commonvector)
        insert_common_vector_into_central_storage(commonvector)

        #  Send reply back to client
        socket.send(b"OK")

      except Exception as e:
        print(e)
        print("error")
        socket.send(b"Error at data receiver")


def setup_zmq_socket():
  global socket
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")


if __name__ == "__main__":
  main()
