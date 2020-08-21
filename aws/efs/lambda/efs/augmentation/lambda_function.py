import boto3
from PIL import Image, ImageFilter
import time
import json
import decimal
from threading import Thread
from io import BytesIO
import subprocess

# import numpy as np

region_name = 'ap-northeast-2'
TMP = "/tmp/"
mnt_test = '/mnt/efs/'

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
    path = mnt_test + "blur-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.BLUR)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def contour(image, file_name):
    path = mnt_test + "contour-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.CONTOUR)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def flip_lr(image, file_name):
    path = mnt_test + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def flip_tb(image, file_name):
    path = mnt_test + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def gray_scale(image, file_name):
    path = mnt_test + "gray-scale-" + file_name
    image = image.convert('RGB')
    img = image.convert('L')
    # img.save(path)
    return_path.append((img, path))
    return [path]


def resized(image, file_name):
    path = mnt_test + "resized-" + file_name
    img = image.resize((32, 32))
    # image.save(path)
    return_path.append((img, path))
    return [path]


def rotate90(image, file_name):
    path = mnt_test + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    # img.save(path)
    return_path.append((img, path))

    return [path]


def rotate180(image, file_name):
    path = mnt_test + "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    # img.save(path)
    return_path.append((img, path))

    return [path]


def rotate270(image, file_name):
    path = mnt_test + "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    # img.save(path)
    return_path.append((img, path))
    return [path]


def sharpen(image, file_name):
    path = mnt_test + "sharpen-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.SHARPEN)
    # img.save(path)
    return_path.append((img, path))
    return [path]


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


def augmentation(file_name, img):
    return_file = []
    for f in functions:
        t = Thread(target=f, args=(img, file_name))
        t.start()
        return_file.append(t)

    for t in return_file:
        t.join()
    return return_file


def write_image_to_efs(img, key):
    img.save(key)


def remove_image(key):
    rm = subprocess.Popen(['rm', '-rf', key])
    rm.communicate()


def lambda_handler(event, context):
    object_path = event['object']

    p = mnt_test + 'aug/'

    data_path = p + object_path
    s3 = boto3.client('s3')

    download_start = time.time()
    image = Image.open(data_path)
    download_time = time.time() - download_start
    augmentation_start = time.time()
    augmentation(object_path, image)
    augmentation_time = time.time() - augmentation_start

    u_t = []

    for r in return_path:
        upload_start = time.time()
        write_image_to_efs(r[0], r[1])
        upload_time = time.time() - upload_start
        u_t.append(upload_time)


    r_t = []

    for r in return_path:
        remove_image(r[1])

    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('aug')

    table.put_item(
        Item={
            'id': decimal.Decimal(time.time()),
            'type': 'efs',
            'second_type': 'aug',
            'name': event['object'],
            'download_time': decimal.Decimal(download_time),
            'upload_time1': decimal.Decimal(u_t[0]),
            'upload_time2': decimal.Decimal(u_t[1]),
            'upload_time3': decimal.Decimal(u_t[2]),
            'upload_time4': decimal.Decimal(u_t[3]),
            'upload_time5': decimal.Decimal(u_t[4]),
            'augmentation_time': decimal.Decimal(augmentation_time),
            'test': event['test'],
        }
    )

    return (
        'type: efs',
        'download_time: ', download_time,
        'upload_time1: ', u_t[0],
        'upload_time2: ', u_t[1],
        'upload_time3: ', u_t[2],
        'upload_time4: ', u_t[3],
        'upload_time5: ', u_t[4],
    )
