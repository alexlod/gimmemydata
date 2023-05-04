
import boto3
from manage.config import Config

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
    
    def get_latest_filename(self, prefix):
        """
        Get the most recent filename from S3 based on the time-aligned directory structure.
        Returns filename as string (excluding extension) or None if no files are found.
        """
        try:
            s3_objects = []
            paginator = self.s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
                if 'Contents' in page:
                    s3_objects += page['Contents']

            if not s3_objects:
                latest_filename = None
            else:
                latest_object = s3_objects[-1]
                latest_filename = latest_object['Key'].split('/')[-1].split('.')[0]

        except KeyError:
            latest_filename = None
            print('No previous activities found in S3')

        return latest_filename