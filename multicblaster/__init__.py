"""Initializes multicblaster web service (started by uwsgi

Main module of the multicblaster web service

# TODO: extensive description

Author: Matthias van den Belt
"""

# import statements
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os
import redis
import rq
import config


r = redis.Redis()
q = rq.Queue(connection=r, default_timeout=28800) # 8h for 1 job

app = Flask("multicblaster")
app.config.update(config.CONF)

db = SQLAlchemy(app)

from multicblaster import routes
import multicblaster.models as m
from multicblaster.downstream.downstream_routes import downstream
from multicblaster.result.result_routes import result

app.register_blueprint(downstream, url_prefix="/downstream")
app.register_blueprint(result, url_prefix="/results")

db.create_all()

# line below indicates the Statistic table is empty
if m.Statistic.query.filter_by(name="finished").first() is None:
    stats = [m.Statistic(name="finished"),
             m.Statistic(name="failed")]
    # Maybe some additional statistics

    for s in stats:
        db.session.add(s)

    db.session.commit()
