#!/usr/bin/python


import sqlite3
import json
import glob
import sys
from shutil import copyfile
import time

import collectord_messagequeue

socket = collectord_messagequeue.start_client()

path_to_firefox_history_db = "/home/*/.mozilla/firefox/*default*/places.sqlite"

globresult = glob.glob(path_to_firefox_history_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)

#print("database is at " , globresult[0])
dbfilename = globresult[0]



latest_row_id = 0

# want to look at schema? for testing only
if False:
  cursor = conn.execute("SELECT sql from sqlite_master")
  for row in cursor:
    for poop in row:
      print(poop)
    print('wat')



while True:
  print("sleep")
  time.sleep(5.0)
  #print("copy the database because firefox locks it")
  shadow_db_location = "/tmp/firefoxshadow.sqlite"
  copyfile(dbfilename, shadow_db_location)
  conn = sqlite3.connect(shadow_db_location)


  # Get the Rows
  cursor = conn.execute("SELECT * from moz_places where id > %d ORDER BY id desc limit 10" % latest_row_id)

  collection_object = dict()
  collection_object['source'] = "firefox_collector_daemon.py"
  collection_object['version'] = "0.0.1"

  outputrows = []
  local_max_id = 0
  number_of_rows = 0
  for row in cursor:
    # track number of rows in the query
    number_of_rows = number_of_rows + 1
    thisoutputrow = dict()
    thisoutputrow['last_visit_date']         = row[8]
    thisoutputrow['url']     = row[1]
    thisoutputrow['description']     = row[12]
    thisoutputrow['title']     = row[2]
    outputrows.append(thisoutputrow)

    # track highest id
    thisrowid = row[0]
    if thisrowid > local_max_id:
      local_max_id = thisrowid

    print("got row id ", row[0])

  # this is how we check for new rows coming in
  if number_of_rows == 0:
    print("no new rows")
    continue
  #
  # prepare object for sending
  collection_object['rows'] = outputrows
  #
  # update max id
  latest_row_id = local_max_id
  print("new max id is ", latest_row_id)
  # write the maxid to a file sometimes

  jsondump = json.dumps(collection_object, indent=2)
  print(jsondump)
  collectord_messagequeue.send_message(socket, jsondump)

  conn.close() # close every lop
