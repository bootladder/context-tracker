#!/usr/bin/python

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

searchquery = ""


path_to_ash_db = "/home/*/.ash/history.db"
shadow_db_location = "/tmp/ashshadow.sqlite"

globresult = glob.glob(path_to_ash_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)


dbfilename = globresult[0]
conn = sqlite3.connect(dbfilename)

latest_row_id = 0

while True:

  print("sleep")
  time.sleep(5.0)

  # Get the Rows
  cursor = conn.execute("SELECT * from commands where id > %d ORDER BY id desc limit 10" % latest_row_id)

  outputrows = []
  local_max_id = 0
  number_of_rows = 0
  for row in cursor:
    # track number of rows in the query
    number_of_rows = number_of_rows + 1

    # save the row in a dict
    thisoutputrow = dict()
    thisoutputrow['cwd']         = row[6]
    thisoutputrow['starttime']    = row[8]
    thisoutputrow['command']     = row[13]
    outputrows.append(thisoutputrow)

    # track highest id
    thisrowid = row[0]
    if thisrowid > local_max_id:
      local_max_id = thisrowid

    print("got row id ", row[0])


  # this is how we check for new rows coming in
  # wait for new rows with higher ids
  if number_of_rows == 0:
    print("no new rows")
    continue
  
  # we got some outputrows and a new max id
  latest_row_id = local_max_id
  print("new max id is ", latest_row_id)
  # write the maxid to a file sometimes

  # send to msgqueue
  print(json.dumps(outputrows, indent=2))

conn.close()
