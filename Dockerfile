FROM ubuntu:18.04

WORKDIR /P4-Lucat-API
ADD . /P4-Lucat-API

RUN apt-get update --assume-yes
RUN apt-get install --assume-yes software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update --assume-yes
RUN apt-get install --assume-yes python3.8 python3-pip
RUN python3.8 -m pip install --upgrade pip

# If you want to use Python 3.8 as your default Python version, you can create a symbolic link like this
RUN ln -s /usr/bin/python3.8 /usr/bin/python

RUN pip3 install flask sparqlwrapper
RUN pip3 install -r /P4-Lucat-API/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME ENDPOINT

# Run app.py when the container launches
CMD ./service.sh
