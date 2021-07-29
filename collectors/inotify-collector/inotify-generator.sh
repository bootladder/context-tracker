#!/bin/bash

# Events come out stdout
# Tee to a file for debugging
# Then to 1shot collector py

WATCHDIR="/home/steve/"
FORMAT=$(echo -e "%T,%w%f,%e")
"$@"
while inotifywait -qre close_write -e modify -e attrib -e move -e create -e delete --timefmt "%s" --format "$FORMAT" $WATCHDIR | tee -a /tmp/inotify-collector-testlog.txt | ./inotify_collector_oneshot_stdin.py
do
    "$@"
done

