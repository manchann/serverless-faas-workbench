import boto3
from PIL import Image, ImageFilter
import time
import json
import decimal
from threading import Thread
from io import BytesIO
import numpy as np

bucket_name = 'lambda-performance'
return_bucket_name = 'lambda-performance-result'

TMP = "/tmp/"

return_path = []


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def blur(image, file_name):
    path = "blur-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.BLUR)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def contour(image, file_name):
    path = "contour-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.CONTOUR)
    # img.save(path)

    return_path.append((img, path))
    return [path]


def flip_lr(image, file_name):
    path = "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def flip_tb(image, file_name):
    path = "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def gray_scale(image, file_name):
    path = "gray-scale-" + file_name
    image = image.convert('RGB')
    img = image.convert('L')
    # img.save(path)
    return_path.append((img, path))
    return [path]


def resized(image, file_name):
    path = "resized-" + file_name
    img = image.resize((32, 32))
    # image.save(path)
    return_path.append((img, path))
    return [path]


def rotate90(image, file_name):
    path = "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    # img.save(path)

    return_path.append((img, path))
    return [path]


def rotate180(image, file_name):
    path = "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    # img.save(path)

    return_path.append((img, path))
    return [path]


def rotate270(image, file_name):
    path = "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def sharpen(image, file_name):
    path = "sharpen-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.SHARPEN)
    # img.save(path)
    return_path.append((img, path))
    return [path]


region_name = 'ap-northeast-2'


def read_image_from_s3(bucket, key):
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return im


def write_image_to_s3(img, key):
    s3 = boto3.resource('s3', region_name)
    bucket = s3.Bucket(return_bucket_name)
    object = bucket.Object(key)
    file_stream = BytesIO()
    img.save(file_stream, format='png')
    object.put(Body=file_stream.getvalue())


functions = [
    # blur,
    # contour,
    flip_lr,
    flip_tb,
    gray_scale,
    # resized,
    rotate90,
    rotate180,
    # rotate270,
    # sharpen
]


def augmentation(file_name, image):
    return_file = []
    for f in functions:
        t = Thread(target=f, args=(image, file_name))
        t.start()
        return_file.append(t)

    for t in return_file:
        t.join()
    return return_file


def remove_image(key):
    client = boto3.client('s3')
    client.delete_object(Bucket=return_bucket_name, Key=key)



def lambda_handler(event, context):
    object_path = event['object']

    s3 = boto3.client('s3')

    download_start = time.time()
    image = read_image_from_s3(bucket_name, object_path)
    download_time = time.time() - download_start
    augmentation_start = time.time()
    augmentation(object_path, image)
    augmentation_time = time.time() - augmentation_start
    upload_start = time.time()
    u_t = []
    for r in return_path:
        t = Thread(target=write_image_to_s3, args=(r[0], r[1]))
        t.start()
        u_t.append(t)

    for t in u_t:
        t.join()
    upload_time = time.time() - upload_start

    r_t = []

    for r in return_path:
        remove_image(r[1])
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('aug')

    table.put_item(
        Item={
            'id': decimal.Decimal(time.time()),
            'type': 's3',
            'second_type': 'aug',
            'name': event['object'],
            'download_time': decimal.Decimal(download_time),
            'augmentation_time': decimal.Decimal(augmentation_time),
            'upload_time': decimal.Decimal(upload_time),
            'test': event['test'],
        }
    )

    return (
        'type: s3',
        'download_time: ', download_time,
        'upload_time: ', upload_time
    )
