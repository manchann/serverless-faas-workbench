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
        file_write_path = mnt_test + 'read_file'

        r_file_size = file_size * 1024 * 1024 

        start = time()
        with open(file_write_path, 'rb', 0) as f:
            for _ in range(int(r_file_size / byte_size)):
                f.read(byte_size)
        disk_read_latency = time() - start
        disk_read_bandwidth = file_size / disk_read_latency

        return "sr latency: " + str(disk_read_latency)+ " bandwidth: " + str(disk_read_bandwidth) + " \n"
    except Exception as ex:
        return str(ex)
    

