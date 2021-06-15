FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt-get install -y supervisor redis zip hmmer
RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker

RUN git clone https://github.com/gamcil/cblaster.git && cd cblaster/ && pip install .

COPY supervisord.conf /etc/supervisord.conf
COPY repo/ /repo/
COPY process_logs/ /process_logs/
COPY present_databases.txt /present_databases.txt

RUN cblaster config --email "matthias.vandenbelt@wur.nl"

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]