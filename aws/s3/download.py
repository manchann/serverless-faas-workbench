import boto3

bucket_name = ''
file_name = ''
local_file_path = '/'

s3 = boto3.client('s3')
s3.download_file(bucket_name, file_name, local_file_path)
