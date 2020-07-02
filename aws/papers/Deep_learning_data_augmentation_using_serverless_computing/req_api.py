import boto3
import json
from threading import Thread
import os
import subprocess

bucket_name = 'pre-image-group'

bucket = boto3.resource('s3').Bucket(bucket_name)


def make_topic(bucket_name, object_path_key):
    message = {
        'bucket_name': bucket_name,
        'object_path': object_path_key
    }
    subprocess.check_call(
        "\curl 'https://2bs4iii4rd.execute-api.ap-northeast-2.amazonaws.com/lambda-test/total/?bucket=%22'{}'%22&object=%22'{}'%22#'".format(
            bucket_name, object_path_key),
        shell=True)


ret_arr = []
num = 0
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table('lambda')

scan = table.scan()
with table.batch_writer() as batch:
    for each in scan['Items']:
        batch.delete_item(Key={
            'id': each['id'],
            'type': each['type']
        })
threads = []
for bucket_object in bucket.objects.all():
    t = Thread(target=make_topic, args=(bucket_name, bucket_object.key))
    t.start()
    threads.append(t)
    num += 1
for t in threads:
    t.join()
print('이미지 개수:', num)
