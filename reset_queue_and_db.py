from redis import Redis
from rq import Queue
from rq.registry import StartedJobRegistry, FinishedJobRegistry, FailedJobRegistry, DeferredJobRegistry, ScheduledJobRegistry
import os

DB_PATH = "multicblaster/status.db"
REGISTRIES = [StartedJobRegistry, FinishedJobRegistry, FailedJobRegistry, DeferredJobRegistry, ScheduledJobRegistry]

print("\n" + "========== WARNING ==========")
print("Continuing will empty the current queue, delete the database, and reset all registries.")
result = None

while result not in ("y", "n", "yes", "no"):
    result = input("Continue? (y/n)")
    if result in ("y", "yes"):
        # empty queue
        q = Queue(connection=Redis())
        q.empty()
        print("The rq Queue has been emptied")

        # remove database
        if not os.path.exists(DB_PATH):
            print(f"No database found at: {DB_PATH}")
        else:
            os.remove("multicblaster/status.db")
            print("Database removed succesfully")

        # clean registries
        for registry in REGISTRIES:
            reg = registry(queue=q)
            for job_id in reg.get_job_ids():
                print(f"Deleted job {job_id} from the {reg}")
                reg.remove(job_id, delete_job=True)

    elif result in ("n", "no"):
        print("Nothing has been emptied or removed. Exiting..")



