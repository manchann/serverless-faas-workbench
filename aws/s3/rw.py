from PIL import Image
from io import BytesIO
import numpy as np
import boto3

region_name = 'ap-northeast-2'

def read_image_from_s3(bucket, key, region_name):

    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return np.array(im)


def write_image_to_s3(img_array, bucket, key, region_name):

    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im = Image.fromarray(img_array)
    im.save(file_stream, format='jpeg')
    object.put(Body=file_stream.getvalue())
