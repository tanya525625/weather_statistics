FROM ubuntu:18.04
RUN mkdir src/
COPY requirements.txt src/
WORKDIR /src/
RUN apt-get update
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-psycopg2
RUN pip3 install -r requirements.txt
ADD . /src/
