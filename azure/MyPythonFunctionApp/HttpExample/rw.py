import logging

import azure.functions as func

from time import time
import subprocess
import os
import random

tmp = '/tmp/'
mnt_test = '/ap/'

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:

        file_size = 200
        byte_size = int(req.route_params.get('bs')) * 1024
        file_write_path = mnt_test + str(time())

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
                os.fsync(f.fileno())
        disk_write_latency = time() - start
        disk_write_bandwidth = file_size / disk_write_latency

        return "rw latency: " + str(disk_write_latency)+ " bandwidth: " + str(disk_write_bandwidth)+ " \n"
    except Exception as ex:
        return str(ex)
    

