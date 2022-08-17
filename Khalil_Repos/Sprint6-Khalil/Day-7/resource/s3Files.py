
import boto3
import sys


s3 = boto3.client('s3')         # Set boto3 client

# s3.download_file('sprintonekhalil', 'file.py', '/tmp/websites.py')       #must be 'tmp' beacuse it is a root folder
# sys.path.insert(1, '/tmp')                  # to enter in path 'tmp'

S3_BUCKET_NAME = 'khalil-sprint6'


def lambda_handler(event,context):              
    object_key = "file2.txt"  # replace object key
    file_content = s3.get_object(Bucket=S3_BUCKET_NAME, Key=object_key)["Body"].read()
    print(file_content)

