import os
from crontab import CronTab
from datasources import spotify, strava
from manage.config import Config

def main():
    # Initialize cron
    cron = CronTab(user=os.getlogin())

    # Schedule Spotify job
    job_spotify = cron.new(command=f"python3 {os.path.abspath(spotify.__file__)}")
    job_spotify.setall('0 0 * * *')  # Run daily at 00:00

    # Schedule Strava job
    # job_strava = cron.new(command=f"python3 {os.path.abspath(strava.__file__)}")
    # job_strava.setall('0 6 * * *')  # Run daily at 06:00


    # Write the new cron jobs
    cron.write()

if __name__ == "__main__":
    main()