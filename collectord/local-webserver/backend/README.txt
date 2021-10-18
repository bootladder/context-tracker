collectord is 2 things

1. Message queue and database for locally installed collector daemons
     to send data to.  The received data can be passed to a central collector,
     and/or handled locally.

1. Webapp and frontend for viewing data collected by collectord
     and possibly also from central collector



postrgres database will be stored somewhere, /var/collectord or /var/lib/collectord
/var/lib/collectord/data.postgres

collectord will expose an API for client collectors to submit data.
Collectors may be in python, go, C, etc.
But really what it is, is just JSON payloads.
So the only important thing is clients can identify the message queue.

bah, actually local tcp socket is the only thing, because Windows wont have unix sockets.
So the port number has to be somewhere, damn.
at this point why not just do HTTP, bah.  The client libs are alot easier in http
but with HTTP you have urls, with socket it's just the socket and then the payloads.
ok, socket, picka  number.  The collector daemons wil also need this number.  bah.



The collector daemons have to run in the background but also detect only new events.
Their only purpose now is to detect new events.  Probably by polling, with SQLites,
or maybe callbacked ala. inotify.


postgres has to be installed already.
probably want to bundle it in with a systemd service
start collectord, start postgres, or make sure postgres is started.
now freaking postgres needs a port too, wtf.  how the hell is that any faster

fuck it, fuck postgres, just put the json files in /var/lib/collectord/abc-collector.json
pass the buck up to central server




