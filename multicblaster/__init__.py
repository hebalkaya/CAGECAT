"""Initializes multicblaster web service

Main module of the multicblaster web service

Ran services:
    - Redis-server
    - Flask
    - SQLAlchemy

# TODO: extensive description

Author: Matthias van den Belt
"""

# import statements
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os
import redis
import rq

# TODO: Find out how pre-submission uploading works

r = redis.Redis()
q = rq.Queue(connection=r, default_timeout=28800) # 8h for 1 job

app = Flask("multicblaster")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///status.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)



UPLOAD_FOLDER = os.path.join("multicblaster/static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


from multicblaster import routes
import multicblaster.models as m
from multicblaster.job_types.job_views import job_views

app.config["DOWNLOAD_FOLDER"] = "jobs" # multicblaster not required in front of jobs
app.register_blueprint(job_views, url_prefix="/downstream")

db.create_all()

# line below indicates the Statistic table is empty
if m.Statistic.query.filter_by(name="finished").first() is None:
    stats = [m.Statistic(name="finished"),
             m.Statistic(name="failed")]
    # Maybe some additional statistics

    for s in stats:
        db.session.add(s)

    db.session.commit()
