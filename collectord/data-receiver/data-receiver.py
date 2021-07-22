#!/usr/bin/python
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received msg.")

    # check for valid json

    # look for magic fields

    # find the appropriate .json file

    # append the entire message to the file

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"OK")
