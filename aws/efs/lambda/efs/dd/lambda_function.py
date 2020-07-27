import subprocess
import time
import boto3
import decimal

tmp = '/tmp/'
mnt_test = '/mnt/efs/'

"""
dd - convert and copy a file
man : http://man7.org/linux/man-pages/man1/dd.1.html
Options 
 - bs=BYTES
    read and write up to BYTES bytes at a time (default: 512);
    overrides ibs and obs
 - if=FILE
    read from FILE instead of stdin
 - of=FILE
    write to FILE instead of stdout
 - count=N
    copy only N input blocks
"""


def lambda_handler(event, context):
    try:
        start = time.time()
        b = int(event['bs']) * 1024

        bs = 'bs=' + str(b)
        count = 'count=' + event['count']
        out_fd = open(mnt_test + 'io_write_logs', 'w')
        dd = subprocess.Popen(['dd', 'if=/dev/zero', 'of=/mnt/efs/out', bs, count], stderr=out_fd)
        dd.communicate()
        # subprocess.check_output(['ls', '-alh', mnt_test])

        with open(mnt_test + 'io_write_logs') as logs:
            result = str(logs.readlines()[2]).replace('\n', '')
            end = time.time()
            print(event['bs'], " ", event['count'])
            dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
            table = dynamodb.Table('EFS')
            response = table.put_item(
                Item={
                    'id': decimal.Decimal(time.time()),
                    'type': 'efs',
                    'second_type': 'dd',
                    'result': result,
                    'latency': decimal.Decimal(end - start),
                    'count': event['count'],
                    'bs': event['bs'] + 'KB',
                    'test': event['test']
                }
            )
            return result + ' efs ' + event['bs'] + event['count'] + event['test'] + " "
    except Exception as ex:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('EFS')
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time.time()),
                'type': 'efs',
                'second_type': 'dd',
                'result': str(ex),
                'count': event['count'],
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return str(ex)
