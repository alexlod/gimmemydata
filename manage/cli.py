
from manage.config import Config
import logging
import sys
import argparse
from datasources.spotify import main as spotify_main
from datasources.strava import main as strava_main
from datasources.oura import main as oura_main
from datasources.github import main as github_main
from manage.cron import Cron

SUPPORTED_DATASOURCES = ['spotify', 'strava', 'oura', 'github']

# Import your deploy script
from manage.deploy import main as deploy_main

def enableDebugMode():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.debug("Debug mode enabled.")

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
        elif service == 'github':
            github_main.run_task()
            print("Github script finished successfully.")
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
    list_parser = subparsers.add_parser('list', help='List currently deployed GimmeMyData cron jobs for current user.')

    # clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all scheduled GimmeMyData cron jobs.')
    
    # deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy all jobs defined in manage.deploy.')

    # run command
    run_parser = subparsers.add_parser('run', help='Manually run a data source script.')
    run_parser.add_argument('service', choices=SUPPORTED_DATASOURCES, help='Service to run.')

    # schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a data source script to run at a given interval (in minutes).')
    schedule_parser.add_argument('service', choices=SUPPORTED_DATASOURCES, help='Service to schedule (spotify, oura, github or strava).')
    schedule_parser.add_argument('interval', type=int, help='Interval (in minutes) at which the script should run.')

    args = parser.parse_args()
    cron = Cron()

    if args.__dict__.get('debug'):
        enableDebugMode()

    if args.__dict__.get('configure'):
        Config().configure()
        sys.exit(1)

    if args.command == 'list':
        cron.list_scheduled_jobs()
    elif args.command == 'clear':
        cron.clear_scheduled_jobs()
    elif args.command == 'deploy':
        deploy_main()
    elif args.command == 'run':
        run_script(args.service)
    elif args.command == 'schedule':
        cron.schedule_job(args.service, args.interval)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
