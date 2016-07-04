FROM python:3.5
ENV LANG C.UTF-8
RUN apt-get update && apt-get install -y make
RUN mkdir /source
WORKDIR /source
COPY requirements.txt /source/
RUN pip install -r requirements.txt
COPY . /source/
ENV PYTHONPATH=$PYTHONPATH:/source
CMD make
