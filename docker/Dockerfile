FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt-get install -y supervisor redis zip hmmer nginx systemd nano htop cron
RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker uWSGI

RUN git clone https://github.com/gamcil/cblaster.git && cd cblaster/ && pip install .

#COPY supervisord.conf /etc/supervisord.conf DONE
# TODO: create the dirs inside the container instead of copying
COPY pfam_db/ /pfam_db/
COPY repo/ /repo/
COPY process_logs/ /process_logs/
COPY present_databases.txt /present_databases.txt

#COPY uwsgi_params /repo/uwsgi_params DONE
#COPY multicblaster /etc/nginx/sites-available/multicblaster DONE
#COPY multicblaster.ini /repo/multicblaster.ini DONE
#COPY config.ini /.config/cblaster/config.ini

RUN mkdir -p /.config/cblaster

#RUN cblaster config --email "matthias.vandenbelt@wur.nl"
RUN mv /repo/docker/multicblaster /etc/nginx/sites-available/multicblaster
RUN mv /repo/docker/config.ini /.config/cblaster/config.ini
RUN mv /repo/aux_files/crontab /etc/crontab

RUN ln -s /etc/nginx/sites-available/multicblaster /etc/nginx/sites-enabled
RUN cron

CMD ["/usr/bin/supervisord", "-c", "/repo/docker/supervisord.conf"]