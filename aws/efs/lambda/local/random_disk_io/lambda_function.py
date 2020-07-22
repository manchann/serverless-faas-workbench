from time import time
import subprocess
import os
import random
import boto3
import decimal


def lambda_handler(event, context):
    try:
        file_size = int(event['fs'])
        byte_size = int(event['bs'])
        file_write_path = '/tmp/file'

        block = os.urandom(byte_size)
        r_file_size = file_size * 1024 * 1024
        total_file_bytes = r_file_size - byte_size

        start = time()
        with open(file_write_path, 'wb') as f:
            for _ in range(int(total_file_bytes / byte_size)):
                f.seek(random.randrange(total_file_bytes))
                f.write(block)
            f.flush()
            os.fsync(f.fileno())
        disk_write_latency = time() - start
        disk_write_bandwidth = file_size / disk_write_latency

        output = subprocess.check_output(['ls', '-alh', '/tmp/'])
        print(output)

        start = time()
        with open(file_write_path, 'rb') as f:
            for _ in range(int(total_file_bytes / byte_size)):
                f.seek(random.randrange(total_file_bytes))
                f.read(byte_size)
        disk_read_latency = time() - start
        disk_read_bandwidth = file_size / disk_read_latency
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
                'disk_write_bandwidth': decimal.Decimal(str(disk_write_bandwidth)),
                'disk_write_latency': decimal.Decimal(disk_write_latency),
                'disk_read_bandwidth': decimal.Decimal(str(disk_read_bandwidth)),
                'disk_read_latency': decimal.Decimal(disk_read_latency),
                'fs': str(r_file_size),
                'bs': event['bs'],
                'test': event['test']
            }
        )
        return {
            'disk_write_bandwidth': disk_write_bandwidth,
            'disk_write_latency': disk_write_latency,
            'disk_read_bandwidth': disk_read_bandwidth,
            'disk_read_latency': disk_read_latency
        }
    except OSError as os_e:
        file_size = int(event['fs'])
        byte_size = int(event['bs'])
        r_file_size = file_size * 1024 * 1024
        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'local',
                'error': 'OS Error',
                'fs': str(r_file_size),
                'bs': event['bs'],
                'test': event['test']
            }
        )
    except Exception as ex:
        file_size = int(event['fs'])
        byte_size = int(event['bs'])
        r_file_size = file_size * 1024 * 1024

        table_name = 'EFS'
        region_name = 'ap-northeast-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        response = table.put_item(
            Item={
                'id': decimal.Decimal(time()),
                'type': 'local',
                'error': str(ex),
                'fs': str(r_file_size),
                'bs': event['bs'],
                'test': event['test']
            }
        )
