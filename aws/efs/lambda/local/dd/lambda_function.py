import subprocess
import time
import boto3
import decimal

tmp = '/tmp/'
mnt_test = '/mnt/test/'

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
        b = str(int(event) * 1024)
        bs = 'bs=' + b
        count = 'count=' + event['count']

        out_fd = open(tmp + 'io_write_logs', 'w')
        dd = subprocess.Popen(['dd', 'if=/dev/zero', 'of=/tmp/out', bs, count], stderr=out_fd)
        dd.communicate()

        subprocess.check_output(['ls', '-alh', tmp])

        with open(tmp + 'io_write_logs') as logs:
            result = str(logs.readlines()[2]).replace('\n', '')
            end = time.time()
            print('test', end - start)
            dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
            table = dynamodb.Table('EFS')
            response = table.put_item(
                Item={
                    'id': decimal.Decimal(time.time()),
                    'type': 'local',
                    'second_type': 'dd',
                    'result': result,
                    'latency': decimal.Decimal(end - start),
                    'count': event['count'],
                    'bs': event['bs'] + 'KB',
                    'test': event['test']
                }
            )
            return result + ' tmp ' + event['bs'] + event['count'] + event['test'] + " "
    except:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('EFS')
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time.time()),
                'type': 'local',
                'second_type': 'dd',
                'result': 'error',
                'count': event['count'],
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return 'list index out of range' + ' tmp error' + event['bs'] + event['count'] + event['test'] + " "
