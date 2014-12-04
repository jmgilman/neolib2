FROM ubuntu:14.04
MAINTAINER Joshua Gilman <joshuagilman@gmail.com>

# Update the repositories
RUN apt-get update

# This is necessary to download pip
RUN apt-get install -y wget

# Get the latest version of pip
RUN wget 'https://bootstrap.pypa.io/get-pip.py'
RUN python3 get-pip.py

# Install lxml dependencies
RUN apt-get install -y libxml2-dev libxslt-dev zlib1g-dev python3-dev

# Install the latest version of neolib2
RUN pip3 install neolib2
