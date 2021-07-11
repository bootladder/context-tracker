#!/usr/bin/python

# this shall be a one-shot command to request a JSON of 
# inotify event history
# the JSON will contain an array of
# inotify events

# Parameters may be such as

# By default it will be 
#

import json

path_to_inotify_log = "/tmp/inotify-collector-testlog.txt"

# Tail the last 10 lines of the file
lines = []

with open(path_to_inotify_log, 'r') as f:
    lines = f.readlines()[-10:]

outputrows = []
for line in lines:
  thisoutputrow = dict()
  # each line is a CSV.  split it
  splitted = line.split(',')
  thisoutputrow['timestamp']         = splitted[0]
  thisoutputrow['filename']    = splitted[1]
  thisoutputrow['event']     = splitted[2]
  outputrows.append(thisoutputrow)



print(json.dumps(outputrows, indent=2))
#for outputrow in outputrows:
#  print(outputrow)

