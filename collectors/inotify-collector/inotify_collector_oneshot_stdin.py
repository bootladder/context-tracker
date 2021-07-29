#!/usr/bin/python3


import json
import sys
import time
import collectord_messagequeue

def process_line_and_send_to_queue(line):
  values = line.split(',')
  collection_object = dict()
  collection_object['source'] = "inotify_collector"
  collection_object['version'] = "0.0.1"

  collection_object['data'] = dict()
  collection_object['data']['timestamp'] = values[0]
  collection_object['data']['filename'] = values[1]
  collection_object['data']['operation'] = values[2]

  jsondump = json.dumps(collection_object, indent=2)
  print(jsondump)

  collectord_messagequeue.send_message(socket, jsondump)


# start with obvious ones, swap, locks
def i_should_filter(line):
  values = line.split(',')
  if values[1].endswith('.swp') \
  or values[1].endswith('.lock') \
  or values[1].endswith('.d') \
  or values[1].endswith('.o') \
  or ('/.mozilla/firefox' in values[1] and '.default-release' in values[1]):
    print("\nFiltered Filename: " + values[1])
    return True

  return False


socket = collectord_messagequeue.start_client()

# This is csv. read lines
for line in sys.stdin:
  if i_should_filter(line):
    continue
  process_line_and_send_to_queue(line)


