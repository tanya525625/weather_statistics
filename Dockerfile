FROM ubuntu:18.04
RUN mkdir src/
COPY requirements.txt src/
WORKDIR /src/
RUN apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
ADD . /src/
