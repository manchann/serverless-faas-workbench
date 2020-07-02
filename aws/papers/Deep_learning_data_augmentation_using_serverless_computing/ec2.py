import boto3
from PIL import Image, ImageFilter

bucket_name = 'pre-aug-document'
return_bucket_name = 'aug-document'

TMP = "/tmp/"


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
    img = image.filter(ImageFilter.BLUR)
    img.save(path)
    path_list.append(path)

    path = TMP + "contour-" + file_name
    img = image.filter(ImageFilter.CONTOUR)
    img.save(path)
    path_list.append(path)

    path = TMP + "sharpen-" + file_name
    img = image.filter(ImageFilter.SHARPEN)
    img.save(path)
    path_list.append(path)

    return path_list


def gray_scale(image, file_name):
    path = TMP + "gray-scale-" + file_name
    img = image.convert('L')
    img.save(path)
    return [path]


def resize(image, file_name):
    path = TMP + "resized-" + file_name
    image.thumbnail((100, 100))
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
    s3.download_file(bucket_name, object_path, tmp)
    return_path = augmentation(object_path, tmp)
    for upload in return_path:
        print(upload)
        s3.upload_file(upload, return_bucket_name, upload.split('/')[2])


bucket = boto3.resource('s3').Bucket(bucket_name)
for bucket_object in bucket.objects.all():
    print(bucket_object)
    event = {
        'bucket_name': bucket_name,
        'object_path': bucket_object.key,
    }
    handler(event)