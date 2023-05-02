#!/usr/bin/env python3

from manage.config import Config
import argparse
import logging
import sys
import argparse
import os
# from crontab import CronTab
from datasources.spotify import spotify as spotify_main
from datasources.strava import strava as strava_main

def enableDebugMode():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.debug("Debug mode enabled.")

# def list_cron_jobs():
#     cron = CronTab(user=os.getlogin())
#     print("Current crontab jobs:")
#     for job in cron:
#         print(job)

def run_script(service):
    print(f"Running {service} script...")
    try:
        if service == 'spotify':
            spotify_main.run_task()
            print("Script finished successfully.")
        elif service == 'strava':
            strava_main.run_task()
        else:
            print(f"Service '{service}' not recognized.")
            return
    except Exception as e:
        print(f"Script failed with error: {e}")

def cli():
    parser = argparse.ArgumentParser(description='CLI to manage data sources.')
    exclusive_group = parser.add_mutually_exclusive_group(required=False)
    exclusive_group.add_argument('--configure', action='store_true', help="Configure the CLI and create or update config yaml file.")
    # parser.add_argument('--debug', action="store_true", help="Enable debug mode.")
    subparsers = parser.add_subparsers(dest='command')

    # list command
    list_parser = subparsers.add_parser('list', help='List current crontab jobs.')

    # run command
    run_parser = subparsers.add_parser('run', help='Manually run a data source script.')
    run_parser.add_argument('service', choices=['spotify', 'strava'], help='Service to run (spotify or strava).')

    args = parser.parse_args()

    # if args.get('debug'):
    #     enableDebugMode()

    # if args.get('configure'):
    #     Config().configure()
    #     sys.exit(1)

    if args.command == 'list':
        print("Current crontab jobs:")
        # list_cron_jobs()
    elif args.command == 'run':
        run_script(args.service)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
