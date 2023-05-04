
import datetime
import json
from manage.config import Config
from datasources.oura.client import OuraClientV2
from utils.render import DBClient
from utils.aws import S3Client


OURA_PERSONAL_ACCESS_TOKEN = Config().get_param('OURA_PERSONAL_ACCESS_TOKEN')
S3_BUCKET_NAME = Config().get_param('S3_BUCKET_NAME')

# Set up S3 client and bucket
s3 = S3Client()

# Set up DB Connection for logging
db_client = DBClient()

# Instantiate Oura API client
oura_client = OuraClientV2(personal_access_token=OURA_PERSONAL_ACCESS_TOKEN)

def get_last_event_ts(prefix):
    # Get the most recent timestamp from S3
    try:
        s3_objects = []
        paginator = s3.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=prefix):
            if 'Contents' in page:
                s3_objects += page['Contents']

        if not s3_objects:
            latest_timestamp = '20210901'
        else:
            latest_object = s3_objects[-1]
            latest_timestamp = latest_object['Key'].split('/')[-1].split('.')[0]

    except KeyError:
        # If there are no objects in the S3 bucket, set latest_timestamp to a very old timestamp to retrieve all records
        latest_timestamp = '20210901'
    
    latest_timestamp_dt = datetime.datetime.strptime(latest_timestamp, '%Y%m%d')
    print('Latest timestamp in S3: ', latest_timestamp_dt.strftime('%Y-%m-%d %H:%M:%S'))

    # Remove microseconds from the latest timestamp to avoid precision errors
    # latest_timestamp = latest_timestamp[:-6]
    return latest_timestamp_dt

def get_heartrate():
    print("Getting Heartrate data...")
    script_name = 'oura-get_heartrate'
    task_ts = datetime.datetime.now()
    formatted_ts = task_ts.strftime("%Y-%m-%dT%H:%M:%S")

    try:
        latest_date_in_s3 = get_last_event_ts('oura/heartrate')
        print(f'Latest date in S3: {latest_date_in_s3}')
              
        if latest_date_in_s3 is None:
            start_date = datetime.datetime.strptime('2021-09-01', '%Y-%m-%d')
            print("No previous data found in S3, defaulting to 2020-01-01.")
            return
        
        start_date = datetime.datetime.combine(latest_date_in_s3, datetime.datetime.min.time()) - datetime.timedelta(days=1)
        print(f'Start date: {start_date}')
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)

        date = start_date
    
        while date <= end_date:
            date_plus_one = date + datetime.timedelta(days=1)
            print(f'New api call where start_date={date.strftime("%Y-%m-%d")} and end_date={date_plus_one.strftime("%Y-%m-%d")} and api: heartrate')
            data = oura_client.heartrate(start_date=date.strftime('%Y-%m-%d'), end_date=date_plus_one.strftime('%Y-%m-%d'))
            
            if data['data'] == []:
                print('No data found for date:', date.strftime('%Y-%m-%d'))
                date += datetime.timedelta(days=1)
                continue
            else:
                filename = date.strftime('%Y%m%d') + '.json'
                dir_path = date.strftime('oura/heartrate/%Y/%m/%d')
                s3_key = f'{dir_path}/{filename}'
                
                file_content = json.dumps(data).encode('utf-8')
                s3.write_to_s3(file_content, s3_key)
                print('Wrote data to S3:', s3_key)
        
            date += datetime.timedelta(days=1)

    except Exception as e:
        # Log the error in the database
        db_client.insert_task_log(script_name, formatted_ts, 'failed')
        raise e

    # Log the success in the database
    db_client.insert_task_log(script_name, formatted_ts, 'success')

def fetch_and_store_data(start_date, end_date, api_endpoint):
    print(f'Fetching data for {api_endpoint} from {start_date} to {end_date}')
    data = oura_client.get_data_for_range(start_date=start_date, end_date=end_date, endpoint=api_endpoint)
    print("made it here.")
    if data == []:
        print('No data found for specified date range')
        return
    else:
        for record in data:
            record_day = record['day']
            filename = record_day.replace('-','') + '.json'
            day_datetime = datetime.datetime.strptime(record_day, '%Y-%m-%d')
            dir_path = day_datetime.strftime(f'oura/{api_endpoint}/%Y/%m/%d')
            s3_key = f'{dir_path}/{filename}'
            # print(json.dumps(record))
            s3.write_to_s3(json.dumps(record), s3_key)
            print(f'Wrote {s3_key} to S3 for date: {record["day"]}')
            
def get_report(endpoint):
    script_name = f'oura-get_{endpoint}'
    task_ts = datetime.datetime.now()
    formatted_ts = task_ts.strftime("%Y-%m-%dT%H:%M:%S")

    try:
        
        latest_date_in_s3 = get_last_event_ts(f'oura/{endpoint}')

        if latest_date_in_s3 is None:
            start_date = datetime.datetime.strptime('2021-09-01', '%Y-%m-%d')
            print("No previous data found in S3, defaulting to 2020-01-01.")
            return

        start_date = datetime.datetime.combine(latest_date_in_s3, datetime.datetime.min.time()) - datetime.timedelta(days=1)
        # start_date =datetime.datetime.strptime('2023-04-15', '%Y-%m-%d')
        print(f'Start date: {start_date}')
        end_date = datetime.datetime.now() - datetime.timedelta(days=1)

        fetch_and_store_data(start_date, end_date, endpoint)

    except Exception as e:
        # Log the error in the database
        db_client.insert_task_log(script_name, formatted_ts, 'Failed')
        raise e

    # Log the success in the database
    db_client.insert_task_log(script_name, formatted_ts, "Success")


def run_task():
    
    get_report('daily_activity')
    get_report('daily_readiness')
    get_report('daily_sleep')
    get_report('sleep')
    get_heartrate()

if __name__ == "__main__":
    run_task()