
import datetime
import json
from manage.config import Config
from utils.render import DBClient
from utils.aws import S3Client
from datasources.github.auth import GithubAuth
from github import Github
from github.GithubException import RateLimitExceededException


S3_BUCKET_NAME = Config().get_param('S3_BUCKET_NAME')

# Set up S3 client and bucket
s3 = S3Client()

# Set up DB Connection for logging
db_client = DBClient()

# Instantiate Github API client
gh = GithubAuth().client

def get_last_event_ts(prefix):
    # Get the most recent timestamp from S3.   Return a datetime.datetime object
    lf = s3.get_latest_filename(prefix)
    
    if lf == None:
        latest_timestamp_dt = datetime.datetime.strptime('2010-04-15', '%Y-%m-%d')
    else:
        latest_timestamp_dt = datetime.datetime.strptime(lf, '%Y%m%d')
    
    print('Latest timestamp in S3: ', latest_timestamp_dt.strftime('%Y-%m-%d %H:%M:%S'))

    return latest_timestamp_dt


def run_task():
    
    # Get the authenticated user
    user = gh.get_user()

    # Get the last event timestamp
    last_event_ts = get_last_event_ts("github/events")
    start_date = last_event_ts
    end_date = datetime.datetime.now()

    # Fetch events within the date range
    events = []
    try:
        for event in user.get_events():
            event_created_at = event.created_at.replace(tzinfo=None)
            if start_date <= event_created_at <= end_date:
                events.append(event)
            elif event_created_at < start_date:
                break
    except RateLimitExceededException:
        print("Rate limit exceeded. Please try again later.")

    # Print the fetched events
    for event in events:
        print(event)

    # Store the fetched events in S3 or update the last event timestamp as needed
    # coming soon...

    return events

if __name__ == "__main__":
    print('bloop')
    # run_task()

