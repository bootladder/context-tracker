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

#
import time
import json
import jsonlines
import zmq

socket = 0  #zmq socket

common_vector_version = '0.0.1'

def c2c_ash_collector_0_0_1(collection_object):
  commonvector = dict()
  commonvector['version'] = common_vector_version
  commonvector['command'] = collection_object['command']
  commonvector['pwd'] = collection_object['cwd']
  return commonvector



# Table of conversions
conversion_funcs = dict()
conversion_funcs['ash_collector_daemon.py'] = dict()
conversion_funcs['ash_collector_daemon.py']['0.0.1'] = c2c_ash_collector_0_0_1


def convert_to_common_vector(collection_object):
  # validate object
  data_source = collection_object['source']
  data_version = collection_object['version']

  conversion_func = conversion_funcs[data_source][data_version]
  vector = conversion_func(collection_object)
  return vector


def insert_common_vector_into_local_storage(vector):

  return True

def main():
  setup_zmq_socket()

  while True:
      #  Wait for any collectors to send data
      message = socket.recv()
      print("\n\nData Collector: Received msg.")

      try:
        collection_object = json.loads(message)
        commonvector = convert_to_common_vector(collection_object)

        insert_common_vector_into_local_storage(commonvector)

        #  Send reply back to client
        socket.send(b"OK")

      except Exception as e:
        print(e)
        socket.send(b"Error at data receiver")


def setup_zmq_socket():
  global socket
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")


if __name__ == "__main__":
  main()
