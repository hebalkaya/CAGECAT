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
#logging.basicConfig(filename="logs.log", level=logging.INFO)

from multicblaster import routes
import multicblaster.models as m

db.create_all()

# line below indicates the Statistic table is empty
if m.Statistic.query.filter_by(name="finished").first() is None:
    stats = [m.Statistic(name="finished"),
             m.Statistic(name="failed")]
    # Maybe some additional statistics

    for s in stats:
        db.session.add(s)

    db.session.commit()
