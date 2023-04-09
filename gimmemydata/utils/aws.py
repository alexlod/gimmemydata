
import boto3
from gimmemydata.config import Config

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