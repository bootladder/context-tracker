#!/bin/bash

WATCHDIR="/opt/projects/"
FORMAT=$(echo -e "%T,%w%f,%e")
"$@"
while inotifywait -qre close_write -e modify -e attrib -e move -e create -e delete --timefmt "%s" --format "$FORMAT" $WATCHDIR | tee -a /tmp/inotify-collector-testlog.txt
do
    "$@"
done

