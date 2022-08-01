"""Initializes CAGECAT web service (started by uwsgi)

Initialization module of the CAGECAT web service. This module executes any
preparational steps before starting CAGECAT. This file is ran from
<server_prefix>/run.py

Author: Matthias van den Belt
"""

# import statements
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import redis
import rq

from config_files.config import init_config

r = redis.Redis()
q = rq.Queue(connection=r, default_timeout=28800) # 8h for 1 job

app = Flask("cagecat")
app.config.update(init_config)

db = SQLAlchemy(app)

from cagecat.routes import routes
from cagecat.tools.tools_routes import tools
from cagecat.result.result_routes import result

app.register_blueprint(tools, url_prefix="/tools")
app.register_blueprint(result, url_prefix="/results")

db.create_all()
