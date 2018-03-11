FROM ubuntu:latest
MAINTAINER Juan Pedro Torres "juanp.95.torres@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libmysqlclient-dev
COPY . /api
WORKDIR /api
RUN pip install -r requirements.txt
CMD ["python","api.py"]
