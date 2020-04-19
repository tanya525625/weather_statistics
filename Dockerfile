FROM python:3
RUN mkdir src/
COPY python-requirments.txt src/
WORKDIR /src/
RUN pip3 install -r python-requirments.txt
ADD . /src/
