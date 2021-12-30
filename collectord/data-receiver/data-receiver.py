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

def main():
  setup_zmq_socket()

  while True:
      #  Wait for next request from client
      message = socket.recv()
      # .decode('utf8')  decode or not?
      print("\n\nData Collector: Received msg.")

      try:
        collection_object = json.loads(message)

        # validate object

        # insert into database

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


def setup_zmq_socket():
  global socket
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")


if __name__ == "__main__":
  main()
