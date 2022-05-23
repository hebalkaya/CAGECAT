FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt update

RUN apt-get install -y supervisor redis zip hmmer nginx systemd nano htop cron ncdu ncbi-entrez-direct diamond-aligner
RUN apt install -y default-jdk

# Install Python packages
RUN pip3 install jinja2==3.0.1 rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker uWSGI wtforms

### Using Bioconda for antiSmash dependencies installation
# intall Bioconda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN echo "\n yes" | sh Miniconda3-latest-Linux-x86_64.sh -p /miniconda3

# add Bioconda channels to download packages from
RUN /miniconda3/condabin/conda config --add channels defaults
RUN /miniconda3/condabin/conda config --add channels bioconda
RUN /miniconda3/condabin/conda config --add channels conda-forge

# install Bioconda packages
RUN /miniconda3/condabin/conda install hmmer2 hmmer diamond fasttree prodigal blast glimmerhmm
#RUN /miniconda3/condabin/conda install muscle=3.8.31 meme=4.11.2
##

### Installing antiSmash itself
RUN wget https://dl.secondarymetabolites.org/releases/6.0.0/antismash-6.0.0.tar.gz
RUN tar -zxf antismash-6.0.0.tar.gz
RUN pip install ./antismash-6.0.0
RUN download-antismash-databases

RUN /miniconda3/condabin/conda init
RUN antismash --check-prereqs

# Manually clone the CAGECAT repository
# RUN git clone https://github.com/gamcil/cblaster.git && cd cblaster/ && pip install .

COPY repo/ /repo/

RUN mkdir /backups
RUN mkdir -p /process_logs/maintenance
RUN mkdir /pfam_db
RUN mkdir -p /root/.config/cblaster

RUN mv /repo/config_files/cagecat /etc/nginx/sites-available/cagecat
RUN mv /repo/config_files/config.ini /root/.config/cblaster/config.ini

# We don't have to copy uwsgi_params, as in cagecat the /repo/config_files/uwsgi_params file is referenced to

RUN ln -s /etc/nginx/sites-available/cagecat /etc/nginx/sites-enabled

RUN chmod +x /repo/maintenance/maint_backup.sh
RUN chmod +x /repo/hmm_database_creation/construct_hmm_databases.sh
RUN chmod +x /repo/maintenance/maint_remove_old_jobs.py
RUN chmod +x /repo/hmm_database_creation/create_databases.py

RUN mv /repo/config_files/crontab /etc/crontab

CMD ["/usr/bin/supervisord", "-c", "/repo/config_files/supervisord.conf"]
