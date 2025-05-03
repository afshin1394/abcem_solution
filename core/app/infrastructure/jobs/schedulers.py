# infra/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED

class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = []

    def start(self):
        """Start the APScheduler."""
        self.scheduler.add_listener(self._listener, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
        self.scheduler.start()

    def stop(self):
        """Shut down the APScheduler."""
        self.scheduler.shutdown()

    def add_cron_job(self, func, cron_expr: str, job_id: str = None):
        """
        Add a cron job with a given function and cron expression.
        :param func: Callable function (e.g., job.execute).
        :param cron_expr: Cron expression (e.g., "0 */1 * * *").
        :param job_id: Optional job ID for reference.
        """
        trigger = CronTrigger.from_crontab(cron_expr)
        job = self.scheduler.add_job(func, trigger, id=job_id or func.__name__)
        self.jobs.append(job)
        print(f"Added job: {job}")

    def list_jobs(self):
        """List all scheduled jobs."""
        return [{"id": job.id, "next_run_time": str(job.next_run_time)} for job in self.scheduler.get_jobs()]

    @staticmethod
    def _listener(event):
        """Handle job errors or missed executions."""
        if event.exception:
            print(f"Job {event.job_id} failed: {event.exception}")
        elif event.code == EVENT_JOB_MISSED:
            print(f"Job {event.job_id} missed its run time.")
