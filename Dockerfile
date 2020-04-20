FROM python:3
RUN mkdir src/
COPY requirments.txt src/
WORKDIR /src/
RUN pip3 install -r requirments.txt
ADD . /src/
