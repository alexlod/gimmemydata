
import boto3
from manage.config import Config
import datetime

class S3Client():

    def __init__(self):
        self.bucket_name = Config().get_param('S3_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def write_to_s3(self, file_content, s3_key):
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=s3_key,
            Body=file_content
        )
    
    def get_last_activity_id(self, prefix: str):
        
        print('Getting last activity ID saved to S3...')
        
        # Get most recent activity ID from S3
        latest_activity_id = None
        try:
            s3_objects = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, MaxKeys=1)['Contents']
            latest_object = s3_objects[0]
            latest_activity_id = latest_object['Key'].split('/')[-1].split('.')[0]
            print(f'Found latest activity ID {latest_activity_id} in S3')
        except KeyError:
            # If there are no objects in the S3 bucket, set latest_timestamp to a very old timestamp to retrieve all records
            latest_activity_id = None
            print('No previous activities found in S3')
        
        return latest_activity_id
    
    def get_latest_mtime_date_from_s3(self, prefix):
        latest_date = None

        for obj in self.s3_client.get_objects(self.bucket_name, prefix):
            date_str = obj.key.split('/')[-1].split('.')[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if latest_date is None or date_obj > latest_date:
                latest_date = date_obj

        return latest_date