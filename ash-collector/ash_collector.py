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
import json

conn = sqlite3.connect('/home/steve/.ash/history.db')

# want to look at schema? for testing only
if False:
  cursor = conn.execute("SELECT sql from sqlite_master where name='commands'")
  for row in cursor:
    for poop in row:
      print(poop)
    print('wat')


# Get the Rows
cursor = conn.execute("SELECT * from commands ORDER BY id desc limit 4")
outputrows = []
for row in cursor:
  thisoutputrow = dict()
  thisoutputrow['cwd']         = row[6]
  thisoutputrow['startime']    = row[8]
  thisoutputrow['command']     = row[13]
  outputrows.append(thisoutputrow)

conn.close()


print(json.dumps(outputrows, indent=2))
#for outputrow in outputrows:
#  print(outputrow)
