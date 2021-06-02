FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt-get install -y supervisor redis zip hmmer
RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker

RUN git clone https://github.com/gamcil/cblaster.git && cd cblaster/ && pip install .

COPY supervisord.conf /etc/supervisord.conf
COPY repo/ /repo/
COPY process_logs/ /process_logs/
COPY storage/ /storage

RUN cblaster config --email "server@server.com"

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]