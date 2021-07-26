FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt-get install -y supervisor redis zip hmmer nginx systemd nano htop cron ncdu
RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker uWSGI

RUN git clone https://github.com/gamcil/cblaster.git && cd cblaster/ && pip install .


# TODO: could: create  dirs inside container instead of copying
COPY repo/ /repo/
COPY present_databases.txt /present_databases.txt

RUN mkdir /backups
RUN mkdir /process_logs
RUN mkdir /pfam_db
RUN mkdir -p /root/.config/cblaster

#RUN cblaster config --email "matthias.vandenbelt@wur.nl"
RUN mv /repo/docker/cagecat /etc/nginx/sites-available/cagecat
RUN mv /repo/docker/config.ini /root/.config/cblaster/config.ini

# We don't have to copy uwsgi_params, as in cagecat the /repo/docker/uwsgi_params file is referenced to

RUN ln -s /etc/nginx/sites-available/cagecat /etc/nginx/sites-enabled

CMD ["/usr/bin/supervisord", "-c", "/repo/docker/supervisord.conf"]