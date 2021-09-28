FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    mysql-server

RUN pip3 install \
    mysql-connector-python \
    Flask \
    autopep8

RUN service mysql start && \
    mysql --execute="CREATE USER 'sql_task'@'localhost' IDENTIFIED BY 'sql_task';" && \
    mysql --execute="CREATE DATABASE sql_task;" && \
    mysql --execute="GRANT ALL PRIVILEGES ON sql_task.* TO 'sql_task'@'localhost';" && \
    mysql --execute="CREATE USER 'api_task'@'localhost' IDENTIFIED BY 'api_task';" && \
    mysql --execute="CREATE DATABASE api_task;" && \
    mysql --execute="GRANT ALL PRIVILEGES ON api_task.* TO 'api_task'@'localhost';"