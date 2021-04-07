def submit_job():
    new_jobs = [] # [(function: func, j_id: str, options: dict, file_path:str , depending_j_id: str, job_type:str), ...]

    for new_job in new_jobs:
        ut.save_settings(request.form, job_id)
        job = q.enqueue(new_job[0], args=(new_job[1],),
                        kwargs={"options": new_job[2],
                                "file_path": new_job[3]},
                        depends_on=new_job[4], result_ttl=86400)
        # if depends_on=None, it does not depend on anything: no error




        # job = q.enqueue(f, args=(job_id,),kwargs={
        #     "options": request.form,
        #     "file_path": file_path,
        #     "prev_page": "/" + request.referrer.split("/")[-1]
        # }, result_ttl=86400)

