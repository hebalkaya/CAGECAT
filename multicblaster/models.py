from datetime import datetime
from multicblaster import db

## SQLAlchemy database classes #TODO: move it to another file
class Job(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    redis_id = db.Column(db.String(80))
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.DateTime)
    finished_time = db.Column(db.DateTime)

    status = db.Column(db.Text, nullable=False)
