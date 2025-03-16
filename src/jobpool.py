from src.jobclass import Job

class JobPool:
    def __init__(self):
        self._jobs = []

    def get_num_jobs(self):
        return len(self._jobs)

    def get_jobs(self):
        return self._jobs

    def add_job(self, job: Job):
        self._jobs.append(job)

    def flush(self):
        self._jobs.clear()