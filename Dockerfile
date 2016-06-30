FROM ubuntu:xenial
MAINTAINER Reece Stevens
RUN apt-get update
RUN apt-get install -y lxc python3 python3-pip python3-pandas make
COPY . /source/
WORKDIR /source
ENV PYTHONPATH=$PYTHONPATH:/source
ENV LANG C.UTF-8
CMD pip3 install --upgrade pip && make install && make all 
