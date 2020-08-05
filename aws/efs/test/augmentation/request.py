import boto3
import json
from threading import Thread
import os
import subprocess

bucket_name = 'lambda-performance'
result_bucket_name = 'lambda-performance-result'
bucket = boto3.resource('s3').Bucket(bucket_name)
result_bucket = boto3.resource('s3').Bucket(result_bucket_name)


def make_topic(bucket_name, object_path_key):
    message = {
        'bucket_name': bucket_name,
        'object_path': object_path_key
    }
    subprocess.check_call(
        "\curl 'https://yfidnyb622.execute-api.ap-northeast-2.amazonaws.com/test/s3-aug-test/?object=%22'{}'%22#'".format(
            object_path_key),
        shell=True)
    subprocess.check_call(
        "\curl 'https://yfidnyb622.execute-api.ap-northeast-2.amazonaws.com/test/efs-test-2/?object=%22'{}'%22#'".format(
            object_path_key),
        shell=True)


ret_arr = []
num = 0

result_bucket.objects.all().delete()

threads = []
for bucket_object in bucket.objects.all():
    t = Thread(target=make_topic, args=(bucket_name, bucket_object.key))
    t.start()
    threads.append(t)
    num += 1
for t in threads:
    t.join()
print('이미지 개수:', num)
