#!/usr/bin/python

# Test and PoC for Firefox Collection
#
# This shall be a one-shot command to request a JSON of Firefox History
# Demonstrates usage of sqlite

import sqlite3
import json
import glob
import sys
from shutil import copyfile

# First copy the DB to prevent locking.  Connection here will be to the shadow DB
path_to_firefox_history_db = "/home/*/.mozilla/firefox/*default*/places.sqlite"
shadow_db_location = "/tmp/firefoxshadow.sqlite"

globresult = glob.glob(path_to_firefox_history_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)

dbfilename = globresult[0]
copyfile(dbfilename, shadow_db_location)

conn = sqlite3.connect(shadow_db_location)

# want to look at schema? for testing only
if False:
  cursor = conn.execute("SELECT sql from sqlite_master")
  for row in cursor:
    for poop in row:
      print(poop)
    print('wat')


# Get the Rows
num_rows_to_query = 2
cursor = conn.execute("SELECT * from moz_places ORDER BY id desc limit %s" % num_rows_to_query)
outputrows = []
for row in cursor:
  thisoutputrow = dict()
  thisoutputrow['last_visit_date']         = row[8]
  thisoutputrow['url']     = row[1]
  thisoutputrow['description']     = row[12]
  thisoutputrow['title']     = row[2]
  outputrows.append(thisoutputrow)

conn.close()


print(json.dumps(outputrows, indent=2))
#for outputrow in outputrows:
#  print(outputrow)
