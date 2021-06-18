FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt-get install -y supervisor redis zip hmmer nginx systemd nano htop
RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker uWSGI

RUN git clone https://github.com/gamcil/cblaster.git && cd cblaster/ && pip install .

COPY supervisord.conf /etc/supervisord.conf
COPY pfam_db/ /pfam_db/
COPY repo/ /repo/
COPY process_logs/ /process_logs/
COPY present_databases.txt /present_databases.txt

COPY multicblaster /etc/nginx/sites-available/multicblaster
COPY multicblaster.ini /repo/multicblaster.ini
COPY config.ini /.config/cblaster/config.ini

#RUN cblaster config --email "matthias.vandenbelt@wur.nl"
RUN ln -s /etc/nginx/sites-available/multicblaster /etc/nginx/sites-enabled

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]