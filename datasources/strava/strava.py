
import json
import datetime
from manage.config import Config
from utils.render import DBClient
from utils.aws import S3Client
from datasources.strava.auth import StravaAuth
from botocore.exceptions import ClientError
import io

POLL_INTERVAL = 3600
S3_BUCKET_NAME = Config().get_param('S3_BUCKET_NAME')

# Set up DB Connection for Auth
conn = DBClient().connection
cur = conn.cursor()

# Set up S3 client and bucket
s3 = S3Client()


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
        s3_objects = s3.s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix='strava/activities/', MaxKeys=1)['Contents']
        latest_object = s3_objects[0]
        # Download the JSON file into memory
        s3_object = s3.s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=latest_object['Key'])
        s3_data = s3_object['Body'].read()

        # Load the JSON data
        latest_activity_data = json.loads(s3_data.decode('utf-8'))

        # Get the start_date from the JSON data
        latest_activity_datetime = latest_activity_data['start_date']
        print(f'Found latest activity datetime {latest_activity_datetime} in S3')
    except ClientError as e:
        print(f"Error downloading S3 object: {e}")
        latest_activity_datetime = None
    except KeyError:
        # If there are no objects in the S3 bucket, set latest_activity_datetime to None
        latest_activity_datetime = None
        print('No previous activities found in S3')
    
    return latest_activity_datetime


def run_task():
    script_name = 'strava-get_activities'
    task_ts = datetime.datetime.now()
    formatted_ts = datetime.strptime(task_ts, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

    strava_client = StravaAuth().init_client()

    # Set up DB Connection for logging
    db_client = DBClient()

    try: 
        
        # Get the latest activity ID from S3
        latest_activity_datetime = get_last_activity_datetime()

        # Get new activities from Strava API
        new_activities = []
        if latest_activity_datetime is not None:
            activities = strava_client.get_activities(after=latest_activity_datetime)
        else:
            activities = strava_client.get_activities()

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

            # Write to S3
            body = json.dumps(activity.to_dict())
            s3.write_to_s3(body, s3_key)
            print(f'Uploaded activity {activity.id} to S3 at: {s3_key}')

        # If the script ran successfully, insert a log entry with a successful status
        db_client.insert_task_log(script_name, formatted_ts, 'success')
    
    except Exception as e:
        # If there was an error during the script execution, insert a log entry with a failed status
        print(f"Error during script execution: {e}")
        db_client.insert_task_log(script_name, formatted_ts, 'failed')

if __name__ == '__main__':
    run_task()