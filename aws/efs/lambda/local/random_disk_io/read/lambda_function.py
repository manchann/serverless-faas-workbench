from time import time
import subprocess
import os
import random
import boto3
import decimal

opt = '/opt/'


def lambda_handler(event, context):
    try:
        file_size = int(event['fs'])
        byte_size = int(float(event['bs']) * 1024)

        file_write_path = opt + 'read_file'
        r_file_size = file_size * 1024 * 1024
        total_file_bytes = r_file_size - byte_size

        random_set = [i for i in range(int(total_file_bytes / byte_size))]

        start = time()
        with open(file_write_path, 'rb', 0) as f:
            for _ in range(int(total_file_bytes / byte_size)):
                f.seek(random.randrange(total_file_bytes))
                f.read(byte_size)
        disk_read_latency = time() - start
        disk_read_bandwidth = file_size / disk_read_latency

        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'local',
                'second_type': 'random',
                'third_type': 'read',
                'disk_read_bandwidth': decimal.Decimal(str(disk_read_bandwidth)),
                'disk_read_latency': decimal.Decimal(disk_read_latency),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return {
            'disk_read_bandwidth': disk_read_bandwidth,
            'disk_read_latency': disk_read_latency
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
                'third_type': 'read',
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
                'third_type': 'read',
                'error': str(ex),
                'fs': event['fs'] + 'MB',
                'bs': event['bs'] + 'KB',
                'test': event['test']
            }
        )
        return event['fs'] + 'MB ' + event['bs'] + 'KB\n'
