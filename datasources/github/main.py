
"""
NOTES ON GITHUB EVENTS:
- Only events created within the past 90 days will be included in timelines. Events older than 90 days will not
     be included (even if the total number of events in the timeline is less than 300).
"""

import datetime
import json
from utils.render import DBClient
from utils.aws import S3Client
from datasources.github.client import GithubClient
from github.GithubException import RateLimitExceededException
import gzip

# Set up S3 client and bucket
s3 = S3Client()

# Set up DB Connection for logging
db_client = DBClient()

# Instantiate Github API client
gh = GithubClient()

def get_last_event_ts(prefix):
    # Get the most recent timestamp from S3.   Return a datetime.datetime object
    lf = s3.get_latest_filename(prefix)
    
    if lf == None:
        latest_timestamp_dt = datetime.datetime.strptime('2010-04-15', '%Y-%m-%d')
    else:
        latest_timestamp_dt = datetime.datetime.strptime(lf, '%Y%m%d%H%M%S')
    
    print('Latest timestamp in S3: ', latest_timestamp_dt.strftime('%Y-%m-%d %H:%M:%S'))

    return latest_timestamp_dt

def write_event_to_s3(events, prefix):

    # Write data to S3
    if len(events) > 0:
        for event in events:
            played_at = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            filename = played_at.strftime('%Y%m%d%H%M%S') + '.json.gz'
            dir_path = played_at.strftime(f'{prefix}/%Y/%m/%d/%H/')
            s3_key = dir_path + filename
            
            event_json = json.dumps(event).encode('utf-8')
            
            # Compress the file content using gzip
            file_content = gzip.compress(event_json)
            
            s3.write_to_s3(file_content, s3_key)
            print('Wrote data to S3:', s3_key)

def run_task():
    
    script_name = f'github-user_events'
    task_ts = datetime.datetime.now()
    formatted_ts = task_ts.strftime("%Y-%m-%dT%H:%M:%S")
    
    try:
        # Get the last event timestamp
        last_event_ts = get_last_event_ts("github/events")
        start_date = last_event_ts
        end_date = datetime.datetime.now()

        # Fetch events within the date range
        try:
            print('Fetching events from Github API for user...')
            events = gh.fetch_events_paginated(start_date, end_date)
        except RateLimitExceededException:
            print("Rate limit exceeded. Please try again later.")

        print(f'Found {len(events)} events from Github API')

        # Store the fetched events in S3 or update the last event timestamp as needed
        write_event_to_s3(events, "github/events")
    
    except Exception as e:
        # Log the error in the database
        db_client.insert_task_log(script_name, formatted_ts, 'Failed')
        raise e

    # Log the success in the database
    db_client.insert_task_log(script_name, formatted_ts, "Success")
    
    db_client.close()

    

if __name__ == "__main__":
    run_task()

