FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt-get install -y supervisor redis
RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug cblaster clinker

COPY repo/ /repo/
COPY supervisord.conf /etc/supervisord.conf
COPY process_logs/ /process_logs/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]