#!/usr/bin/python
#
# Data Receiver
# Read from socket, assume it is JSON,
# Make the data available for 2 consumers:  Local Web App and Central Collector
#
# For Local Web App,
#    store the JSON into a file, based on the "source" field in the JSON
#    Convert incoming JSON to jsonlines to allow line separation
#    These data files can be further parsed by the local webserver.
#
# For Central Collector, HTTP request the payloads up.

# note  /var/lib/collectord has to be accessible, these are where the local files are appended.
#
JSON_FILE_STORAGE_DIR = "/var/lib/collectord/"
from pathlib import Path
Path(JSON_FILE_STORAGE_DIR).mkdir(parents=True, exist_ok=True)

import time
import json
import jsonlines
import zmq

socket = 0  #zmq socket

def main():
  setup_zmq_socket()

  while True:
      #  Wait for next request from client
      message = socket.recv()
      # .decode('utf8')  decode or not?
      print("\n\nData Collector: Received msg.")

      try:
        c1 = jsonlines.Reader(message)
        collection_object = json.loads(message)

        filename = obj2filename(collection_object, '.msgpack')
        print("filename is " + filename)

        # append the entire message to the file
        print(message)
        with open(filename, 'a+') as f:
          f.write(str(message, encoding='utf-8'))

        #  Do some 'work'
        #time.sleep(1)

        #  Send reply back to client
        socket.send(b"OK")

      except Exception as e:
        print(e)
        print("Pbad")
        socket.send(b"BAD")


def obj2filename(obj, suffix):
  # look for magic fields
  source  = obj['source']
  version = obj['version']

  # check for bad characters
  return JSON_FILE_STORAGE_DIR + source.replace('_','').replace('.','') + ".json"

def setup_zmq_socket():
  global socket
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")


if __name__ == "__main__":
  main()
