import boto3
from PIL import Image, ImageFilter
import time
import json
import decimal

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


def flip(image, file_name):
    path_list = []
    path = TMP + "flip-left-right-" + file_name
    img = image.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)
    path_list.append(path)

    path = TMP + "flip-top-bottom-" + file_name
    img = image.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(path)
    path_list.append(path)

    return path_list


def rotate(image, file_name):
    path_list = []
    path = TMP + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    img.save(path)
    path_list.append(path)

    path = TMP + "rotate-180-" + file_name
    img = image.transpose(Image.ROTATE_180)
    img.save(path)
    path_list.append(path)

    path = TMP + "rotate-270-" + file_name
    img = image.transpose(Image.ROTATE_270)
    img.save(path)
    path_list.append(path)

    return path_list


def filter(image, file_name):
    path_list = []
    path = TMP + "blur-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.BLUR)
    img.save(path)
    path_list.append(path)

    path = TMP + "contour-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.CONTOUR)
    img.save(path)
    path_list.append(path)

    path = TMP + "sharpen-" + file_name
    image = image.convert('RGB')
    img = image.filter(ImageFilter.SHARPEN)
    img.save(path)
    path_list.append(path)

    return path_list


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    image = image.convert('RGB')
    img = image.convert('L')
    img.save(path)
    return [path]


def resize(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((128, 128))
    image.save(path)
    return [path]


def augmentation(file_name, image_path):
    return_file = []
    image = Image.open(image_path)
    return_file += flip(image, file_name)
    return_file += rotate(image, file_name)
    return_file += filter(image, file_name)
    return_file += gray_scale(image, file_name)
    return_file += resize(image, file_name)
    print(return_file)
    return return_file


def handler(event):
    bucket_name = event['bucket_name']
    object_path = event['object_path']
    tmp = '/tmp/' + object_path
    s3 = boto3.client('s3')
    s3_start = time.time()
    s3.download_file(bucket_name, object_path, tmp)
    aug_start = time.time()
    return_path = augmentation(object_path, tmp)
    aug_end = time.time()
    return aug_start - s3_start, aug_end - aug_start


start = time.time()
bucket = boto3.resource('s3').Bucket(bucket_name)
image_count = 0

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
table = dynamodb.Table('ec2-s3-aug')
for bucket_object in bucket.objects.all():
    event = {
        'bucket_name': bucket_name,
        'object_path': bucket_object.key,
    }
    s3_time, aug_time = handler(event)
    #
    # response = table.put_item(
    #     Item={
    #         'id': decimal.Decimal(time.time()),
    #         'type': 't2.micro',
    #         's3_time': decimal.Decimal(s3_time),
    #         'aug_time': decimal.Decimal(aug_time),
    #     }
    # )
    image_count += 1
end = time.time()

print('total duration: ', end - start)

table = dynamodb.Table('ec2')
table.put_item(
    Item={
        'instance': 't2.micro',
        'type': 'sequence',
        'image_count': decimal.Decimal(image_count),
        'duration': decimal.Decimal(end - start)
    }
)
