"""Stores models of entities for SQL database interacted by with SQLAlchemy

Author: Matthias van den Belt
"""
from datetime import datetime
from multicblaster import db

## SQLAlchemy database classes
class Job(db.Model):
    """Model for creating a job entry

        Inherits from db.Model

    """
    id = db.Column(db.String(15), primary_key=True)
    job_type = db.Column(db.String(10), nullable=False)
    main_search_job = db.Column(db.String(15))
    child_jobs = db.Column(db.String())
    depending_on = db.Column(db.String(10))
    # parent_search_job = db.Column(db.String(15)) # TODO: maybe in future
    redis_id = db.Column(db.String(80))
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)

    status = db.Column(db.Text, nullable=False)

    def __repr__(self):
        print("Main search:", self.main_search_job)
        print("Children:", self.child_jobs)
        print("Depending:", self.depending_on)
        return f"ID: {self.id}; Type: {self.job_type}; Status: {self.status}; Posted: {self.post_time}; Started: {self.start_time}; Finished: {self.finish_time}"

class Statistic(db.Model):
    """Model for creating a entry for job statistics

    Inherits from db.Model

    """
    # Implemented as counters instead of querying the full db, which could
    # take a long time when the db becomes large

    name = db.Column(db.String(20), primary_key=True)
    count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"{self.name.capitalize()}: {self.count} jobs"
