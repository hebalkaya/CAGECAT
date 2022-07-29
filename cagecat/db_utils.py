import typing as t

from werkzeug.utils import secure_filename

from cagecat.db_models import Job, Statistic


def fetch_job_from_db(job_id: str) -> t.Optional[Job]:
    """Checks if a job with a specific job ID exists in the database

    Input:
        - job_id: ID of a job to search for

    Output:
        - Job instance if present in the database OR
        - None if no job with the given ID was found in the database
    """
    job_id = secure_filename(job_id)
    return Job.query.filter_by(id=job_id).first()


def fetch_statistic_from_db(name: str):
    return Statistic.query.filter_by(name=name).first()
