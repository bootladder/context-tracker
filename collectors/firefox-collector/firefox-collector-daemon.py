#!/usr/bin/python

# This shall be a one-shot command to request a JSON of Firefox History
# the JSON will contain:
# 

# Parameters may be such as

import sqlite3
import json
import glob
import sys
from shutil import copyfile

path_to_firefox_history_db = "/home/*/.mozilla/firefox/*default*/places.sqlite"
shadow_db_location = "/tmp/firefoxshadow.sqlite"

globresult = glob.glob(path_to_firefox_history_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)

#print("database is at " , globresult[0])
dbfilename = globresult[0]

#print("copy the database because firefox locks it")

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
cursor = conn.execute("SELECT * from moz_places ORDER BY id desc limit 10")
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
