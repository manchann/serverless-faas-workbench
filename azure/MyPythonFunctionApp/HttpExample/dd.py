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
        b = int(req.route_params.get('bs')) * 1024

        bs = 'bs=' + str(b)
        count = 'count=' + req.route_params.get('count')
        out_fd = open(mnt_test + 'io_write_logs', 'w')
        dd = subprocess.Popen(['dd', 'if=/ap/read_file', 'of=/ap/out', bs, count], stderr=out_fd)
        dd.communicate()
        # subprocess.check_output(['ls', '-alh', mnt_test])

        with open(mnt_test + 'io_write_logs') as logs:
            result = str(logs.readlines()[2]).replace('\n', '')
        return result + "\n"
    except Exception as ex:
        return str(ex)
    

