
from datasources.spotify.client import SpotifyClient
import json
from datetime import datetime
import gzip
from utils.render import DBClient
from utils.aws import S3Client


# Set up S3 client and bucket
s3 = S3Client()

# Instantiate Spotify API Client
spotify = SpotifyClient()

def get_last_event_ts(prefix) -> datetime:
    # Get the most recent timestamp from S3.   Return a datetime.datetime object
    lf = s3.get_latest_filename(prefix)
    
    if lf == None:
        latest_timestamp_dt = datetime.strptime('2010-04-15', '%Y-%m-%d')
    else:
        latest_timestamp_dt = datetime.strptime(lf, '%Y%m%d%H%M%S')
    
    print('Latest timestamp in S3: ', latest_timestamp_dt.strftime('%Y-%m-%d %H:%M:%S'))

    return latest_timestamp_dt

def write_events_to_s3(events, prefix):

    # Write data to S3
    if len(events) > 0:
        for event in events:
            played_at = datetime.strptime(event['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            filename = played_at.strftime('%Y%m%d%H%M%S') + '.json.gz'
            dir_path = played_at.strftime(f'{prefix}/%Y/%m/%d/%H/')
            s3_key = dir_path + filename
            
            event_json = json.dumps(event).encode('utf-8')
            
            # Compress the file content using gzip
            file_content = gzip.compress(event_json)
            
            s3.write_to_s3(file_content, s3_key)
            print('Wrote data to S3:', s3_key)
    else:
        print('No new events to write to S3.')

def run_task():
    script_name = 'spotify-get_recently_played'
    task_ts = datetime.now()
    formatted_ts = datetime.strptime(task_ts, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

    # Set up DB Connection for logging
    db_client = DBClient()

    try: 
        # Get the most recent timestamp from S3
        latest_timestamp: datetime = get_last_event_ts("spotify/recently_played")

        # Retrieve listening history from Spotify API
        history = spotify.get_recently_played(latest_timestamp)

        # Write data to S3
        write_events_to_s3(history, 'spotify/recently_played')

        # If the script ran successfully, insert a log entry with a successful status
        db_client.insert_task_log(script_name, formatted_ts, 'success')
    
    except Exception as e:
        # If there was an error during the script execution, insert a log entry with a failed status
        print(f"Error during script execution: {e}")
        db_client.insert_task_log(script_name, formatted_ts, 'failed')

if __name__ == '__main__':
    run_task()


## TODO - switch this to use the before and after logic to avoid having to retrieve all records every time
