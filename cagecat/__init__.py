"""Initializes CAGECAT web service (started by uwsgi)

Initialization module of the CAGECAT web service. This module executes any
preparational steps before starting CAGECAT. This file is ran from
<server_prefix>/run.py

Author: Matthias van den Belt
"""

# import statements
import base64
import hashlib

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy

import redis
import rq
import re


from config_files.config import init_config

r = redis.Redis()
q = rq.Queue(connection=r, default_timeout=28800) # 8h for 1 job

app = Flask("cagecat")
app.config.update(init_config)

db = SQLAlchemy(app)

from cagecat.routes import routes
from cagecat.tools.tools_routes import tools
from cagecat.result.result_routes import result

from cagecat.db_utils import Statistic

app.register_blueprint(tools, url_prefix="/tools")
app.register_blueprint(result, url_prefix="/results")

db.create_all()

# for custom instances
if Statistic.query.filter_by(name="finished").first() is None:
    stats = [Statistic(name="finished"),
             Statistic(name="failed")]
    # Maybe some additional statistics

    for s in stats:
        db.session.add(s)

    db.session.commit()

# add_header Content-Security-Policy "script-src 'self' *.googleapis.com cdnjs.cloudflare.com cdn.jsdelivr.net; frame-src 'self'";
# csp_headers = {
#     'frame-src': [
#         'self'
#     ],
#     'script-src': [
#         "'sha256-VTAmOhFJf7NXPaOoDtmGnzgeTy5irawqE7Gps5UfNaU='",
#         "'sha256-5NUfqwE5Ru7GwQSUKLQJ+U61xroMjwjJdR/FrbGlXgc='",
#         0,
#         # body.onload will be added here. index 2 will be set over and over for every response
#         'self',
#         '*.googleapis.com',
#         'cdnjs.cloudflare.com',
#         'cdn.jsdelivr.net',
#     ]
# }

csp_headers =   "frame-src 'self'; " \
                "frame-ancestors 'self'; " \
                "style-src 'self' cdnjs.cloudflare.com; " \
                "script-src " \
                "'unsafe-hashes' " \
                "'sha256-VTAmOhFJf7NXPaOoDtmGnzgeTy5irawqE7Gps5UfNaU=' " \
                "'sha256-5NUfqwE5Ru7GwQSUKLQJ+U61xroMjwjJdR/FrbGlXgc=' " \
                "'sha256-{0}' " \
                "'self' " \
                "ajax.googleapis.com " \
                "cdnjs.cloufdare.com " \
                "cdn.jsdelivr.net"

# js_pattern = r'<body .+onload="(.+)">'
js_pattern = re.compile(r'<script type="application\/javascript">(function wrapped\(\).+)<\/script>')

def hash_digest_js_code(resp):
    """Returns sha256 digest of response JS code to set CSP header

    :param resp:
    :return:
    """
    resp: Response

    print(resp.get_data(True))

    matches = re.findall(pattern=js_pattern, string=resp.get_data(as_text=True))
    if len(matches) == 0:
        to_encode = ''
    elif len(matches) == 1:
        to_encode = matches[0]
    else:
        raise Exception('Invalid match length')

    print('ENCODING:', to_encode)
    return base64.b64encode(hashlib.sha256(to_encode.encode()).digest()).decode('UTF-8')

@app.after_request
def add_security_headers(resp):
    headers = csp_headers.format(hash_digest_js_code(resp))
    resp.headers['Content-Security-Policy'] = headers

    return resp
