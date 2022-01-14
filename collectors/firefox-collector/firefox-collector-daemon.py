#!/usr/bin/python

# Firefox stores history in a SQLite database.

# SHADOW
# It's always open so you can't open it in sqlite.
# first you have to copy it.  this is called the shadow.
# querying is done on the shadow, but it is always up to date.

# NEW ROW DETECTION
# when this daemon starts, new rows will be inserted into the db.
# to detect these new rows, this daemon will poll every few seconds. eg. 5.
# within a few seconds there can be multiple rows appended, ie.
# multiple browser history events.
# so within a polling interval there may be multiple new rows.
# the polling loop will query the database for any rows more recent
# than the last one received.
# to do this, the last received ID is tracked.


import sqlite3
import json
import glob
import sys
from shutil import copyfile
import time

def main():
  print("Hello World!")


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
    print("firefox-collector-daemon.py top loop sleep")
    time.sleep(2.0)

    #copy the database because firefox locks it
    shadow_db_location = "/tmp/firefoxshadow.sqlite"
    copyfile(dbfilename, shadow_db_location)

    # Connect to shadow db
    conn = sqlite3.connect(shadow_db_location)

    # Get the Rows
    # Last 10 recent rows of firefox history
    # AFTER the last one received previously
    cursor = conn.execute("SELECT * from moz_places where id > %d ORDER BY id desc limit 10" % latest_row_id)


    # Collect all new rows in SQLite DB
    outputrows = []
    local_max_id = 0
    number_of_rows = 0
    for row in cursor:
      # track number of rows in the query, sometimes there is 0
      number_of_rows = number_of_rows + 1

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

      # track highest id of these new rows
      thisrowid = row[0]
      if thisrowid > local_max_id:
        local_max_id = thisrowid

      print("NEW Firefox ROW, ID: ", row[0])

    # If no new rows, stop here
    if number_of_rows == 0:
      print("NO NEW Firefox rows")
      continue



    # Update max id (prepping for next query at top of loop)
    latest_row_id = local_max_id
    print("new max id is ", latest_row_id)

    # Write the maxid to a file sometimes (TODO)


    # close every lop
    conn.close()




def get_exact_path_to_firefox_sqlite():
  path_to_firefox_history_db = "/home/*/.mozilla/firefox/*default*/places.sqlite"

  globresult = glob.glob(path_to_firefox_history_db)
  if len(globresult) != 1:
    print("wtf too many globs")
    sys.exit(1)

  print("database is at " , globresult[0])
  dbfilename = globresult[0]
  return dbfilename



if __name__ == "__main__":
  main()
