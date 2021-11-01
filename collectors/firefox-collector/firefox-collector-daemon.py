#!/usr/bin/python

import sqlite3
import json
import glob
import sys
from shutil import copyfile
import time

def get_exact_path_to_firefox_sqlite():
  path_to_firefox_history_db = "/home/*/.mozilla/firefox/*default*/places.sqlite"

  globresult = glob.glob(path_to_firefox_history_db)
  if len(globresult) != 1:
    print("wtf too many globs")
    sys.exit(1)

  print("database is at " , globresult[0])
  dbfilename = globresult[0]
  return dbfilename



# Setup collectord messagequeue to send JSON to
import collectord_messagequeue
try:
  socket = collectord_messagequeue.start_client()
  print("Socket good to go")
except e:
  print("fail catch")

dbfilename = get_exact_path_to_firefox_sqlite()


# Setup the Collection Object
#
# Predefined keyvalues here, will be modified in place by received SQLite events,
# and then serialized each time to JSON for sending to the collectord message queue
collection_object = dict()
collection_object['source'] = "firefox_collector_daemon.py"
collection_object['version'] = "0.0.1"



##################################################################
#
# SQLite Polling Loop
#
#

latest_row_id = 0

while True:
  print("sleep")
  time.sleep(2.0)

  #copy the database because firefox locks it
  shadow_db_location = "/tmp/firefoxshadow.sqlite"
  copyfile(dbfilename, shadow_db_location)

  # Connect to shadow db
  conn = sqlite3.connect(shadow_db_location)

  # Get the Rows
  cursor = conn.execute("SELECT * from moz_places where id > %d ORDER BY id desc limit 10" % latest_row_id)


  # Collect all new rows in SQLite DB
  outputrows = []
  local_max_id = 0
  number_of_rows = 0
  for row in cursor:
    # track number of rows in the query
    number_of_rows = number_of_rows + 1
    thisoutputrow = dict()
    thisoutputrow['last_visit_date']         = row[8]
    thisoutputrow['url']                     = row[1]
    thisoutputrow['description']             = row[12]
    thisoutputrow['title']                   = row[2]
    outputrows.append(thisoutputrow)

    # track highest id
    thisrowid = row[0]
    if thisrowid > local_max_id:
      local_max_id = thisrowid

    print("got row id ", row[0])

  # If no new rows, stop here
  if number_of_rows == 0:
    print("no new rows")
    continue


  # Prepare Collection Object for sending N new rows to collector message queue
  collection_object['rows'] = outputrows

  # Update max id (prepping for next query at top of loop)
  latest_row_id = local_max_id
  print("new max id is ", latest_row_id)

  # Write the maxid to a file sometimes (TODO)

  # Serialize collection object to JSON
  jsondump = json.dumps(collection_object, ensure_ascii=False)
  print(jsondump[1:])

  # Send JSON to Message Queue
  print("SENDING TO MESSAGE QUEUE")
  collectord_messagequeue.send_message(socket, jsondump)

  # close every lop
  conn.close()
