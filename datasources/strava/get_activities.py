
import logging
from stravalib.client import Client
import json
import time
import requests
import datetime
import os
import psycopg2
from gimmemydata.config import Config
from gimmemydata.utils.render import DBClient
from gimmemydata.utils.aws import S3Client


POLL_INTERVAL = 3600
S3_BUCKET_NAME = Config().get_param('S3_BUCKET_NAME')
STRAVA_CLIENT_ID = Config().get_param('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = Config().get_param('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = Config().get_param('STRAVA_REFRESH_TOKEN')


# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# logging.debug("Debug mode enabled.")

# Set up DB Connection for Auth
conn = DBClient().connection
cur = conn.cursor()

# Set up S3 client and bucket
s3 = S3Client()

def update_db(access_token, refresh_token, expiration_timestamp):
    # Update DB with new access token
    print('Updating DB with new access token...')
    cur.execute("INSERT INTO strava_auth (access_token, refresh_token, expiration_timestamp) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET access_token = %s, refresh_token = %s, expiration_timestamp = %s;", (access_token, refresh_token, expiration_timestamp, access_token, refresh_token, expiration_timestamp))
    conn.commit()
    print('DB updated')

def get_permission():
    client = Client()
    authorize_url = client.authorization_url(client_id=STRAVA_CLIENT_ID, redirect_uri='http://localhost:8282/authorized')
    print('Go to the following URL and authorize the application:')
    print(authorize_url)
    
    # Extract the code from your webapp response
    code = input('Paste the code here and press Enter: ')
    token_response = client.exchange_code_for_token(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET, code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']
    update_db(access_token, refresh_token, expires_at)

def init_client():

    # Initialize Strava API client and authenticate with access token
    print('Initializing Strava API client...')
    client = Client()
    client.access_token = None
    expiration_timestamp = None
    cur.execute("SELECT access_token, expiration_timestamp FROM strava_auth ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    if row is not None:
        access_token, expiration_timestamp = row
    if access_token is not None and expiration_timestamp is not None and expiration_timestamp > time.time():
        client.access_token = access_token
        
        print(f'Using existing access token expiring at {expiration_timestamp}')
    else:
        print('No valid access token found, refreshing...')

        token_response = client.refresh_access_token(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET, refresh_token=STRAVA_REFRESH_TOKEN)
        access_token = token_response['access_token']
        expiration_timestamp = token_response['expires_at']
        client.access_token = access_token
        print(f'Got new access token expiring at {datetime.datetime.fromtimestamp(expiration_timestamp)}')
        update_db(access_token, token_response['refresh_token'], expiration_timestamp)

    return client

def get_last_activity_id():
    print('Getting last activity ID saved to S3...')
    # Get most recent activity ID from S3
    latest_activity_id = None
    try:
        s3_objects = s3.s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix='strava/activities/', MaxKeys=1)['Contents']
        latest_object = s3_objects[0]
        latest_activity_id = latest_object['Key'].split('/')[-1].split('.')[0]
        print(f'Found latest activity ID {latest_activity_id} in S3')
    except KeyError:
        # If there are no objects in the S3 bucket, set latest_timestamp to a very old timestamp to retrieve all records
        latest_activity_id = None
        print('No previous activities found in S3')
    
    return latest_activity_id


def get_last_activity_datetime():
    print('Getting datetime of the last activity saved to S3...')
    # Get the datetime of the most recent activity from S3
    latest_activity_datetime = None
    try:
        s3_objects = s3.s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix='strava/activities/')['Contents']
        
        # Sort S3 objects by key (filename) in descending order
        sorted_s3_objects = sorted(s3_objects, key=lambda x: x['Key'], reverse=True)
        
        # Get the most recent object
        latest_object = sorted_s3_objects[0]
        
        # Download the JSON file
        s3.s3_client.download_file(S3_BUCKET_NAME, latest_object['Key'], '/tmp/latest_activity.json')
        
        # Load the JSON data
        with open('/tmp/latest_activity.json', 'r') as f:
            latest_activity_data = json.load(f)
        
        # Get the start_date from the JSON data
        latest_activity_datetime = latest_activity_data['start_date']
        print(f'Found latest activity datetime {latest_activity_datetime} in S3')
    except KeyError:
        # If there are no objects in the S3 bucket, set latest_activity_datetime to None
        latest_activity_datetime = None
        print('No previous activities found in S3')
    
    return latest_activity_datetime

def save_activities():

    client = init_client()

    # Get the latest activity ID from S3
    latest_activity_datetime = get_last_activity_datetime()

    # Get new activities from Strava API
    new_activities = []
    if latest_activity_datetime is not None:
        activities = client.get_activities(after=latest_activity_datetime)
    else:
        activities = client.get_activities()

    for activity in activities:
        new_activities.append(activity)
    
    print(f'new activities: {new_activities}')
    print(f'Found {len(new_activities)} new activities')

    # Save each new activity to S3
    for activity in new_activities:

        print(activity.to_dict())
        # activity_ts = datetime.datetime.strptime(activity.start_date_local, '%Y-%m-%dT%H:%M:%SZ')
        activity_ts = activity.start_date_local
        activity_id = activity.id
        s3_key = f'strava/activities/{activity_ts.strftime("%Y/%m/%d")}/{activity_id}.json'

        # s3_key = f'strava/activities/{activity_ts.year:04}/{activity_ts.month:02}/{activity_ts.day:02}/{activity_id}.json'

        # Write to S3
        body = json.dumps(activity.to_dict())
        s3.write_to_s3(body, s3_key)
        print(f'Uploaded activity {activity.id} to S3 at: {s3_key}')

# get_permission()
# save_activities()

while True: 
    try:
        save_activities()
    except Exception as e:
        print(f'Error: {e}')
    print('Sleeping...')
    time.sleep(int(POLL_INTERVAL))