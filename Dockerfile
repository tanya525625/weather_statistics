FROM python:3
RUN mkdir src/
COPY python-requirments.txt src/
WORKDIR /src/
RUN pip3 install -r python-requirments.txt
ADD . /src/

FROM alpine:3.2
ADD repositories /etc/apk/repositories
RUN apk add --update python python-dev gfortran py-pip build-base py-numpy@community