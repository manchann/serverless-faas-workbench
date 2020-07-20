import boto3
from PIL import Image, ImageFilter
import time
import json
import decimal
from threading import Thread
import os

TMP = "/tmp/"
mnt_test = '/mnt/test/'

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
    path = TMP + "blur-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.BLUR)
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def contour(image, file_name):
    path = TMP + "contour-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.CONTOUR)
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def flip_lr(image, file_name):
    path = TMP + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def flip_tb(image, file_name):
    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    image = image.convert('RGB')
    img = image.convert('L')
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def resized(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((128, 128))
    image.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def rotate90(image, file_name):
    path = TMP + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    img.save(path)
    return_path.append(path.split('/')[2])

    return [path]


def rotate180(image, file_name):
    path = TMP + "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    img.save(path)
    return_path.append(path.split('/')[2])

    return [path]


def rotate270(image, file_name):
    path = TMP + "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


def sharpen(image, file_name):
    path = TMP + "sharpen-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.SHARPEN)
    img.save(path)
    return_path.append(path.split('/')[2])
    return [path]


functions = [
    blur,
    contour,
    flip_lr,
    flip_tb,
    gray_scale,
    resized,
    rotate90,
    rotate180,
    rotate270,
    sharpen
]


def augmentation(file_name, image_path):
    return_file = []
    for f in functions:
        image = Image.open(image_path)
        t = Thread(target=f, args=(image, file_name))
        t.start()
        return_file.append(t)

    for t in return_file:
        t.join()
    return return_file


def lambda_handler(event, context):
    start = time.time()
    print(event)
    p = mnt_test + '/0'
    file_list = os.listdir(p)
    tmp = '/mnt/test/0/' + file_list[0]
    download_start = time.time()

    download_time = time.time() - download_start

    augmentation(file_list[0], tmp)

    upload_start = time.time()
    for p in return_path:
        text = open(p, 'w')
    upload_time = time.time() - upload_start

    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('EFS')
    end = time.time()

    response = table.put_item(
        Item={
            'id': decimal.Decimal(time.time()),
            'type': 'efs',
            'start_time': decimal.Decimal(start),
            'end_time': decimal.Decimal(end),
            'download_time': decimal.Decimal(download_time),
            'upload_time': decimal.Decimal(upload_time),
        }
    )
    print('download_time: ', download_time)
    print('upload_time: ', upload_time)
