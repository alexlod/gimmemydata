
from crontab import CronTab
import os, sys

class Cron:
    def __init__(self):
        self.user = os.getlogin()
        self.cron = CronTab(user=self.user)
        self.app_comment = "Created by GimmeMyData"
    
    def list_scheduled_jobs(self):
        cron = CronTab(user=os.getlogin())
        print("Current scheduled jobs:")
        gimmemydata_jobs = [job for job in cron if job.comment == self.app_comment] 
        for job in gimmemydata_jobs:
            print(job)

    def clear_scheduled_jobs(self):
        cron = CronTab(user=os.getlogin())
        jobs_to_remove = [job for job in cron if job.comment == self.app_comment] 
        for job in jobs_to_remove:
            cron.remove(job)
        cron.write()
        print("Cleared all GimmeMyData cron jobs for current user.")

    def schedule_job(self, service, interval):
        cron = CronTab(user=os.getlogin())
        job_command = f"python3 {os.path.abspath(sys.modules[service + '_main'].__file__)}"
        job = cron.new(command=job_command)
        job.set_comment(self.app_comment)  # setting comment so we can identify jobs created by this app
        job.setall(f"*/{interval} * * * *")  # Run every 'interval' minutes
        cron.write()