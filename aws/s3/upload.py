import boto3

bucket_name = ''
object_path = ''
file_path = '/'

s3 = boto3.client('s3')
response = s3.upload_file(file_path, bucket_name, object_path)
