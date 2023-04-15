#!/usr/bin/python

# Local System Collector Daemon

# Collects the following:

# Memory and CPU usage of running processes

# Track events:
#  - Process created




import sqlite3
import json
import glob
import sys
from shutil import copyfile
import time

def main():
  print("Hello World!")
  sys.stdout.flush()


  # Setup collectord messagequeue to send JSON to
  import collectord_messagequeue
  try:
    socket = collectord_messagequeue.start_client()
    print("Socket good to go")
  except e:
    print("fail catch")

  sys.stdout.flush()

  # Setup the Collection Object
  #
  # Predefined keyvalues here, will be modified in place by received SQLite events,
  # and then serialized each time to JSON for sending to the collectord message queue
  collection_object = dict()
  collection_object['source'] = "firefox_collector_daemon.py"
  collection_object['version'] = "0.0.1"



  ##################################################################
  #
  # Local System Polling Loop
  #

  while True:
    print("localsystem-collector.py top loop sleep")
    sys.stdout.flush()
    time.sleep(10.0)




    collection_object['last_visit_date']         = row[8]
    collection_object['url']                     = row[1]
    collection_object['description']             = row[12]
    collection_object['title']                   = row[2]

    # Serialize collection object to JSON
    jsondump = json.dumps(collection_object, ensure_ascii=False)
    print(jsondump[1:])

    # Send JSON to Message Queue
    print("SENDING TO MESSAGE QUEUE")
    collectord_messagequeue.send_message(socket, jsondump)


    # close every lop
    conn.close()



if __name__ == "__main__":
  main()
