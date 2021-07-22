#!/usr/bin/python

# note  /var/lib/collectord has to be acceisible

import time
import json
import zmq


def main():
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")

  while True:
      #  Wait for next request from client
      message = socket.recv()
      print("Received msg.")

      try:
        # check for valid json
        collection_object = json.loads(message)

        # look for magic fields
        source = collection_object['source']
        print("SOURCE!!! ", source)

        # find the appropriate .json file
        filename = source2filename(source)
        print("filename is " + filename)

        # append the entire message to the file
        print(message)
        with open(filename, 'a+') as f:
          f.write(message)

        #  Do some 'work'
        time.sleep(1)

        #  Send reply back to client
        socket.send(b"OK")

      except Exception as e:
        print(e)
        print("Pbad")
        socket.send(b"BAD")


def source2filename(source):
  # check for bad characters
  return "/var/lib/collectord/" + source.replace('_','').replace('.','') + ".json"


if __name__ == "__main__":
  main()
