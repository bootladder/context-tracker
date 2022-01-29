#!/usr/bin/python3

# This DAEMON will poll the SQLite database
# checking for new rows.
# The new rows will be sent to collectord-data-receiver message queue
#
# and possibly to central collector

# The SQLite data is parsed to JSON here

# The last ID of rows retrived is stored,
# which is how new rows are detected.
# this last ID shall be stored somewhere and updated every once in a while.

import sqlite3
import glob
import json
from shutil import copyfile
import sys
import time
import collectord_messagequeue

socket = collectord_messagequeue.start_client()

searchquery = ""


# path_to_ash_db = "/home/*/.ash/history.db"
path_to_ash_db = "/ash/history.db"
shadow_db_location = "/tmp/ashshadow.sqlite"

# Get the path to the user's ASH database
globresult = glob.glob(path_to_ash_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)
dbfilename = globresult[0]

# Connect to the ASH database
conn = sqlite3.connect(dbfilename)

# Track the last id, so only the latest
# new rows are sent up to data receiver
latest_row_id = 0





def process_new_ash_row_and_send_to_data_receiver(row):
  collection_object = dict()
  collection_object['source'] = "ash_collector_daemon.py"
  collection_object['version'] = "0.0.1"

  collection_object['cwd']         = row[6]
  collection_object['starttime']    = row[8]
  collection_object['command']     = row[13]

  # send to msgqueue
  jsondump = json.dumps(collection_object, indent=2)
  print(jsondump)

## TODO TIMEOUT!!! IT HANGS
  collectord_messagequeue.send_message(socket, jsondump)


print("ASH COLLECTOR DAEMON")

while True:

  print("sleep")
  sys.stdout.flush()
  time.sleep(5.0)

  # Get the Rows
  cursor = conn.execute("SELECT * from commands where id > %d ORDER BY id desc limit 10" % latest_row_id)


  outputrows = []
  local_max_id = 0
  number_of_rows = 0
  for row in cursor:
    # track number of rows in the query
    number_of_rows = number_of_rows + 1

    process_new_ash_row_and_send_to_data_receiver(row)

    # track highest id
    thisrowid = row[0]
    if thisrowid > local_max_id:
      local_max_id = thisrowid

    print("got row id ", row[0])


  # this is how we check for new rows coming in
  if number_of_rows == 0:
    print("no new rows")
    continue
  
  # we got some outputrows and a new max id


  # update max id
  latest_row_id = local_max_id
  print("new max id is ", latest_row_id)
  # write the maxid to a file sometimes



conn.close()
