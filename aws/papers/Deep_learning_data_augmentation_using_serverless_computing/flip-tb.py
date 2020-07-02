import boto3
from PIL import Image, ImageFilter
import json
import time
import decimal

return_bucket_name = 'aug-module'

TMP = "/tmp/"


def flip_tb(image, file_name):
    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(path)

    return path


def augmentation(file_name, image_path):
    image = Image.open(image_path)
    ret = flip_tb(image, file_name)
    return ret


def handler(event, context):
    start = time.time()
    records = json.loads(event['Records'][0]['Sns']['Message'])
    bucket_name = records['bucket_name']
    object_path = records['object_path']
    tmp = '/tmp/' + object_path
    s3_start = time.time()
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, object_path, tmp)
    s3_end = time.time()
    s3_time = s3_end - s3_start
    aug_start = time.time()
    ret = augmentation(object_path, tmp)
    aug_end = time.time()
    aug_time = aug_end - aug_start

    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('lambda')
    end = time.time()
    response = table.put_item(
        Item={
            'id': decimal.Decimal(time.time()),
            'type': 'flip-tb',
            'details': {
                'start_time': decimal.Decimal(start),
                'end_time': decimal.Decimal(end),
                's3_time': decimal.Decimal(s3_time),
                'aug_time': decimal.Decimal(aug_time),
            }
        }
    )
    print('s3_time: ', s3_time)
    print('aug_time: ', aug_time)
    print('flip-tb')
    return 'flip-tb'
