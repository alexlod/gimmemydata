
from datasources.spotify.auth import SpotifyAuth
from manage.config import Config
import time
import json
import datetime
import requests
from utils.render import DBClient
from utils.aws import S3Client


S3_BUCKET_NAME = Config().get_param('S3_BUCKET_NAME')
# POLL_INTERVAL = 3600

# Set up S3 client and bucket
s3 = S3Client()

def get_last_event_ts():
    # Get the most recent timestamp from S3
    try:
        s3_objects = []
        paginator = s3.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix='spotify/recently-played/'):
            if 'Contents' in page:
                s3_objects += page['Contents']
                
        latest_object = s3_objects[-1]
        latest_timestamp = latest_object['Key'].split('/')[-1].split('.')[0]
        print(latest_timestamp)

    except KeyError:
        # If there are no objects in the S3 bucket, set latest_timestamp to a very old timestamp to retrieve all records
        latest_timestamp = '20000101000000'
    
    latest_timestamp_dt = datetime.datetime.strptime(latest_timestamp, '%Y%m%d%H%M%S')
    print('Latest timestamp in S3: ', latest_timestamp_dt.strftime('%Y-%m-%d %H:%M:%S'))

    # Remove microseconds from the latest timestamp to avoid precision errors
    # latest_timestamp = latest_timestamp[:-6]
    return latest_timestamp_dt

def get_spotify_history():

    # Create SpotifyAuth instance
    spotify_auth = SpotifyAuth()
    access_token = spotify_auth.get_valid_access_token()

    # Build Spotify API request URL
    spotify_api_url = 'https://api.spotify.com/v1/me/player/recently-played'

    # Make Spotify API request with access token
    retries = 3
    for i in range(retries):
        response = requests.get(
            spotify_api_url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        if response.status_code == 200:
            response_json = response.json()
            return response_json['items']

        elif response.status_code == 500:
            print(f'Server error, retrying in {i+1} seconds...')
            time.sleep(i+1)
        else:
            raise Exception(f'Request failed with status code {response.status_code}: {response.text}')
    raise Exception('Maximum retries exceeded, request failed.')


def run_task():
    script_name = 'spotify-get_recently_played'
    task_ts = datetime.datetime.now()
    formatted_ts = datetime.strptime(task_ts, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

    # Set up DB Connection for logging
    db_client = DBClient()

    try: 
        # Get the most recent timestamp from S3
        latest_timestamp = get_last_event_ts()

        # Retrieve listening history from Spotify API
        history = get_spotify_history()

        # Filter out tracks that have already been saved to S3
        filtered_history = [track for track in history if datetime.datetime.strptime(track['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ') > latest_timestamp]
        for track in filtered_history:
            print(track['played_at'], track['track']['name'])

        # Write data to S3
        if len(filtered_history) > 0:
            for track in filtered_history:
                played_at = datetime.datetime.strptime(track['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                filename = played_at.strftime('%Y%m%d%H%M%S') + '.json'
                dir_path = played_at.strftime('spotify/recently-played/%Y/%m/%d/%H/')
                s3_key = dir_path + filename
                
                file_content = json.dumps(track).encode('utf-8')
                s3.write_to_s3(file_content, s3_key)
                print('Wrote data to S3:', s3_key)

        # If the script ran successfully, insert a log entry with a successful status
        db_client.insert_task_log(script_name, formatted_ts, 'success')
    
    except Exception as e:
        # If there was an error during the script execution, insert a log entry with a failed status
        print(f"Error during script execution: {e}")
        db_client.insert_task_log(script_name, formatted_ts, 'failed')

if __name__ == '__main__':
    run_task()


## TODO - switch this to use the before and after logic to avoid having to retrieve all records every time
