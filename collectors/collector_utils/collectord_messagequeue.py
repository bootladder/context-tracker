#!/usr/bin/python3

import zmq

# return the socket
def start_client():
  context = zmq.Context()
  print("Connecting to collectord queue")
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")
  return socket


def send_message(socket, msg):
  socket.send_string(msg)
  message = socket.recv()
  print("receivved from socket : ", message)
