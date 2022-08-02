# Manually clone the correct repository and add

#/repo/config_files/config.ini
#/repo/config_files/sensitive.py

# to the folder

FROM ubuntu:latest
FROM python:3

RUN apt-get update
RUN apt update

RUN apt-get install -y supervisor redis zip hmmer nginx systemd nano htop cron ncdu ncbi-entrez-direct diamond-aligner zip
RUN apt install -y default-jdk

RUN pip3 install rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker wtforms pytz uwsgi genomicsqlite

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

# Install Python packages
RUN /miniconda3/bin/pip3 install jinja2==3.0.1 rq Flask more_itertools Flask_SQLAlchemy redis Werkzeug clinker wtforms pytz genomicsqlite
RUN /miniconda3/condabin/conda init

RUN pip3 install jinja2==3.0.1

### Installing antiSmash itself
RUN wget https://dl.secondarymetabolites.org/releases/6.0.0/antismash-6.0.0.tar.gz
RUN tar -zxf antismash-6.0.0.tar.gz
RUN pip install ./antismash-6.0.0
RUN download-antismash-databases
RUN antismash --check-prereqs

RUN git clone https://github.com/MatthiasvdBelt/cblaster.git && cd cblaster/ && pip install .

COPY repo/ /repo/

RUN mkdir /backups /pfam_db /hmm_databases /sanitization /hmm_profiles /repo/cagecat/jobs
RUN mkdir -p /process_logs/maintenance
RUN mkdir -p /root/.config/cblaster


RUN mv /repo/config_files/cagecat /etc/nginx/sites-available/cagecat

# We don't have to copy uwsgi_params, as in cagecat the /repo/config_files/uwsgi_params file is referenced to

RUN ln -s /etc/nginx/sites-available/cagecat /etc/nginx/sites-enabled

RUN chmod +x /repo/maintenance/maint_backup.sh /repo/hmm_database_creation/construct_hmm_databases.sh /repo/maintenance/maint_remove_old_jobs.py /repo/hmm_database_creation/create_databases.py

CMD ["/usr/bin/supervisord", "-c", "/repo/config_files/supervisord.conf"]
