
from manage.config import Config
import logging
import sys
import argparse
import os
from crontab import CronTab
from datasources.spotify import spotify as spotify_main
from datasources.strava import strava as strava_main
from datasources.oura import oura as oura_main

SUPPORTED_DATASOURCES = ['spotify', 'strava', 'oura', 'github']

def enableDebugMode():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.debug("Debug mode enabled.")

def list_scheduled_jobs():
    cron = CronTab(user=os.getlogin())
    print("Current scheduled jobs:")
    for job in cron:
        print(job)

def schedule_job(service, interval):
    cron = CronTab(user=os.getlogin())
    job_command = f"python3 {os.path.abspath(sys.modules[service + '_main'].__file__)}"
    job = cron.new(command=job_command)
    job.setall(f"*/{interval} * * * *")  # Run every 'interval' minutes
    cron.write()

def run_script(service):
    print(f"Running {service} script...")
    try:
        if service == 'spotify':
            spotify_main.run_task()
            print("Script finished successfully.")
        elif service == 'strava':
            strava_main.run_task()
            print("Script finished successfully.")
        elif service == 'oura':
            oura_main.run_task()
            print("Script finished successfully.")
        else:
            print(f"Service '{service}' not recognized.")
            return
    except Exception as e:
        print(f"Script failed with error: {e}")

def cli():
    parser = argparse.ArgumentParser(description='CLI to manage data sources.')
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    exclusive_group.add_argument('--configure', action='store_true', help="Configure the CLI and create or update config yaml file.")
    parser.add_argument('--debug', action="store_true", help="Enable debug mode.")
    subparsers = parser.add_subparsers(dest='command')

    # list command
    list_parser = subparsers.add_parser('list', help='List current crontab jobs.')

    # run command
    run_parser = subparsers.add_parser('run', help='Manually run a data source script.')
    run_parser.add_argument('service', choices=SUPPORTED_DATASOURCES, help='Service to run (spotify or strava).')

    # schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a data source script to run at a given interval (in minutes).')
    schedule_parser.add_argument('service', choices=SUPPORTED_DATASOURCES, help='Service to schedule (spotify, oura, github or strava).')
    schedule_parser.add_argument('interval', type=int, help='Interval (in minutes) at which the script should run.')

    args = parser.parse_args()

    if args.__dict__.get('debug'):
        enableDebugMode()

    if args.__dict__.get('configure'):
        Config().configure()
        sys.exit(1)

    if args.command == 'list':
        list_scheduled_jobs()
    elif args.command == 'run':
        run_script(args.service)
    elif args.command == 'schedule':
        schedule_job(args.service, args.interval)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
