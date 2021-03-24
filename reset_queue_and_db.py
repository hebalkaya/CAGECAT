from redis import Redis
from rq import Queue
import os

# empty queue
q = Queue(connection=Redis())
q.empty()
print("rq Queue was emptied")

# remove database
os.remove("multicblaster/status.db")
print("SQL database removed succesfully")
