#!/usr/bin/python3

import zmq

def start_client(host, port):
    context = zmq.Context()
    print("Oh yeah!")
    print("Connecting to collectord queue")
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")
    print(f"Connected to {host}:{port}")
    return socket


def send_message(socket, msg):
    socket.send_string(msg)
    message = socket.recv()
    print("received from socket :", message)
