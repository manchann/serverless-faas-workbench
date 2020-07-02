import boto3
from PIL import Image, ImageFilter
import time
import json
import decimal
from threading import Thread

bucket_name = 'pre-image-group'
return_bucket_name = 'aug-ec2'

TMP = "/tmp/"


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
    return [path]


def contour(image, file_name):
    path = TMP + "contour-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.CONTOUR)
    img.save(path)
    return [path]


def flip_lr(image, file_name):
    path = TMP + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)
    return [path]


def flip_tb(image, file_name):
    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(path)
    return [path]


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    image = image.convert('RGB')
    img = image.convert('L')
    img.save(path)
    return [path]


def resized(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((128, 128))
    image.save(path)
    return [path]


def rotate90(image, file_name):
    path = TMP + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    img.save(path)
    return [path]


def rotate180(image, file_name):
    path = TMP + "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    img.save(path)
    return [path]


def rotate270(image, file_name):
    path = TMP + "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    img.save(path)
    return [path]


def sharpen(image, file_name):
    path = TMP + "sharpen-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.SHARPEN)
    img.save(path)
    return [path]


def augmentation(file_name, image_path):
    return_file = []
    image = Image.open(image_path)
    return_file += blur(image, file_name)
    return_file += contour(image, file_name)
    return_file += flip_lr(image, file_name)
    return_file += flip_tb(image, file_name)
    return_file += gray_scale(image, file_name)
    return_file += resized(image, file_name)
    return_file += rotate90(image, file_name)
    return_file += rotate180(image, file_name)
    return_file += rotate270(image, file_name)
    return_file += sharpen(image, file_name)
    print(return_file)
    return return_file


s3_time = 0
aug_time = 0


def handler(bucket_name, object_path):
    tmp = '/tmp/' + object_path
    s3 = boto3.client('s3')
    s3_start = time.time()
    s3.download_file(bucket_name, object_path, tmp)
    aug_start = time.time()
    return_path = augmentation(object_path, tmp)
    aug_end = time.time()
    s3_time = aug_start - s3_start
    aug_time = aug_end - aug_start

    print(s3_time, aug_time)


start = time.time()
bucket = boto3.resource('s3').Bucket(bucket_name)
image_count = 0

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table('ec2-s3-aug')
threads = []
for bucket_object in bucket.objects.all():
    event = {
        'bucket_name': bucket_name,
        'object_path': bucket_object.key,
    }
    t = Thread(target=handler, args=(event['bucket_name'], event['object_path']))
    t.start()
    threads.append(t)
    image_count += 1
for t in threads:
    t.join()
end = time.time()

print('total duration:', end - start)
# response = table.put_item(
#         Item={
#             'id': time.time(),
#             'type': 't2.micro',
#             's3_time': decimal.Decimal(s3_time),
#             'aug_time': decimal.Decimal(aug_time),
#         }
#     )
table = dynamodb.Table('ec2')
table.put_item(
    Item={
        'instance':'t2.micro',
        'type': 'func-only-sequence',
        'image_count': decimal.Decimal(image_count),
        'duration': decimal.Decimal(end - start)
    }
)
