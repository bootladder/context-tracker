#!/usr/bin/python

# this shall be a one-shot command to request a JSON of shell history
# the JSON will contain an array of history entries

# Parameters may be such as
# - number of entries
# - search string
# - date range
# - from cwd

# By default it will be the last 100 (10 for now, testing) shell commands

import sqlite3
import glob
import json
from shutil import copyfile

path_to_ash_db = "/home/*/.ash/history.db"
shadow_db_location = "/tmp/ashshadow.sqlite"

globresult = glob.glob(path_to_ash_db)
if len(globresult) != 1:
  print("wtf too many globs")
  sys.exit(1)


dbfilename = globresult[0]
conn = sqlite3.connect(dbfilename)

# want to look at schema? for testing only
if False:
  cursor = conn.execute("SELECT sql from sqlite_master where name='commands'")
  for row in cursor:
    for poop in row:
      print(poop)
    print('wat')


# Get the Rows
cursor = conn.execute("SELECT * from commands ORDER BY id desc limit 10")
outputrows = []
for row in cursor:
  thisoutputrow = dict()
  thisoutputrow['cwd']         = row[6]
  thisoutputrow['starttime']    = row[8]
  thisoutputrow['command']     = row[13]
  outputrows.append(thisoutputrow)

conn.close()


print(json.dumps(outputrows, indent=2))
#for outputrow in outputrows:
#  print(outputrow)
