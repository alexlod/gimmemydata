import os
from datasources.spotify import main as spotify_main
from datasources.strava import main as strava_main
from datasources.oura import main as oura_main
from datasources.github import main as github_main
from manage.cron import Cron

def main():
    # Initialize cron
    cron = Cron()
    crontab = cron.cron

    jobs = [
        {
            'name': 'spotify',
            'command': f"python3 {os.path.abspath(spotify_main.__file__)}",
            'schedule': '0 0 * * *',
        },
        {
            'name': 'strava',
            'command': f"python3 {os.path.abspath(strava_main.__file__)}",
            'schedule': '0 6 * * *',
        },
        {
            'name': 'oura',
            'command': f"python3 {os.path.abspath(oura_main.__file__)}",
            'schedule': '0 12 * * *',
        },
        {
            'name': 'github',
            'command': f"python3 {os.path.abspath(github_main.__file__)}",
            'schedule': '0 18 * * *',
        },
    ]

    # Clear all existing cron jobs created by GimmeMyData
    jobs_to_remove = [job for job in crontab if job.comment == "Created by GimmeMyData"] 
    for job in jobs_to_remove:
        crontab.remove(job)
    crontab.write()
    print("Cleared all existing GimmeMyData cron jobs for current user.")

    # Deploy all specified cron jobs
    for job_data in jobs:
        job = list(crontab.find_comment(job_data['name']))
        if job:
            job[0].setall(job_data['schedule'])
            job[0].set_command(job_data['command'])
            job[0].set_comment(cron.app_comment)
        else:
            job = crontab.new(command=job_data['command'], comment=cron.app_comment)
            job.setall(job_data['schedule'])

    # Write the new cron jobs
    crontab.write()

    # Print the list of cron jobs
    print("Cron jobs deployed:")
    for job in crontab:
        print(job)

if __name__ == "__main__":
    main()