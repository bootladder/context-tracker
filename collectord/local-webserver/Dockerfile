# FROM golang:1.17

# This container runs the local webapp
# it is a golang binary, which is already built and supplied here to build this image.
# the backend will call out to shell commands
# these shell scripts need to be in the container
# the shell scripts will call out to central mongo
# so a full environment needs to be setup.


from python:3
run mkdir /opt/installs

RUN useradd -ms /bin/bash localwebserver

run chown -R localwebserver:localwebserver /opt/installs


USER localwebserver
run echo whoami
run whoami
run echo what the hell
#run sudo echo what htehll sudo
WORKDIR /home/localwebserver


# do pip stuff so that the backend can call out to python
# and the python can do stuff.
RUN pip install --upgrade pip
run pip install --no-cache-dir zmq glob2 pysqlite3 pymongo


# Copy everything in the source build directory, into the image,
# at the workdir, /home/localwebserver


# NO, VOLUMING MAPING IT IN
# COPY . .




# this is already built
CMD ["./backend/collectord-local-webapp"]
# CMD ["/bin/bash"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
