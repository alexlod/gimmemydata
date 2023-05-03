import os
from crontab import CronTab
from datasources.spotify import spotify as spotify_main
from datasources.strava import strava as strava_main
from datasources.oura import oura as oura_main
from manage.config import Config

def main():
    # Initialize cron
    cron = CronTab(user=os.getlogin())

    # Schedule Spotify job
    job_spotify = cron.new(command=f"python3 {os.path.abspath(spotify_main.__file__)}")
    job_spotify.setall('0 0 * * *')  # Run daily at 00:00

    # Schedule Strava job
    job_strava = cron.new(command=f"python3 {os.path.abspath(strava_main.__file__)}")
    job_strava.setall('0 6 * * *')  # Run daily at 06:00

    # Schedule Oura job
    job_oura = cron.new(command=f"python3 {os.path.abspath(oura_main.__file__)}")
    job_oura.setall('0 12 * * *')  # Run daily at 12:00

    # Write the new cron jobs
    cron.write()

    # Print the list of cron jobs
    print("Cron jobs deployed:")
    for job in cron:
        print(job)

if __name__ == "__main__":
    main()