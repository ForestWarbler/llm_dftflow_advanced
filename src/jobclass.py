class Job:
    def __init__(self):
        self._job_id = None
        self._job_scale = None
        self._job_root_dir = None

    def get_job_id(self):
        return self._job_id

    def get_job_scale(self):
        return self._job_scale

    def get_job_root_dir(self):
        return self._job_root_dir

    def set_job_id(self, job_id):
        self._job_id = job_id

    def set_job_scale(self, job_scale):
        self._job_scale = job_scale

    def set_job_root_dir(self, job_root_dir):
        self._job_root_dir = job_root_dir