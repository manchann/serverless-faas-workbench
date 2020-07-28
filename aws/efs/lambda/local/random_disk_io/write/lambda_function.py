from time import time
import subprocess
import os
import random
import boto3
import decimal


def lambda_handler(event, context):
    try:
        file_size = int(event['fs'])
        byte_size = int(float(event['bs']) * 1024)
        file_write_path = '/tmp/' + str(time())

        block = os.urandom(byte_size)
        r_file_size = file_size * 1024 * 1024
        total_file_bytes = r_file_size - byte_size

        random_set = [i for i in range(int(total_file_bytes / byte_size))]
        start = time()
        with open(file_write_path, 'wb', 0) as f:
            for _ in range(int(total_file_bytes / byte_size)):
                ran_num = random.choice(random_set)
                random_set.remove(ran_num)
                f.seek(ran_num * byte_size)
                f.write(block)
                f.flush()
                os.fsync(f.fileno())  # change
        disk_write_latency = time() - start
        disk_write_bandwidth = file_size / disk_write_latency
        rm = subprocess.Popen(['rm', '-rf', file_write_path])
        rm.communicate()

        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'local',
                'second_type': 'random',
                'third_type': 'write',
                'disk_write_bandwidth': decimal.Decimal(str(disk_write_bandwidth)),
                'disk_write_latency': decimal.Decimal(disk_write_latency),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return {
            'disk_write_bandwidth': disk_write_bandwidth,
            'disk_write_latency': disk_write_latency,
        }
    except OSError as os_e:
        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'local',
                'second_type': 'random',
                'third_type': 'write',
                'error': str(os_e),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return event['fs'] + 'MB ' + event['bs'] + 'KB\n'

    except Exception as ex:
        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'local',
                'second_type': 'random',
                'third_type': 'write',
                'error': str(ex),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return event['fs'] + 'MB ' + event['bs'] + 'KB\n'
