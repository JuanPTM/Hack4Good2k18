FROM mariadb
MAINTAINER Juan Pedro Torres "jutorresm@gmail.com"
ENV MYSQL_ROOT_PASSWORD hack4f00d
ENV MYSQL_DATABASE=MSZ
ADD trigger.py /trigger.py
ADD maria.sql /docker-entrypoint-initdb.d
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install paho-mqtt 
