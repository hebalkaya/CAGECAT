from multicblaster import db
from multicblaster.models import Job, Statistic
from sys import argv


if __name__ == "__main__":
    try:
        if argv[1] == "failed":
            for j in Job.query.filter_by(status="failed").all():
                print(j)
                path = f"multicblaster/jobs/{j.id}/logs/{j.id}_cblaster.log"

                with open(path) as inf:
                    print(inf.readlines())
    except:

        for j in Job.query.all():
            print(j)

        print(Statistic.query.all())