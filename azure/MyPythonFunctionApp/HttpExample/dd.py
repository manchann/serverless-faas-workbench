import logging

import azure.functions as func
from opencensus.ext.azure.log_exporter import AzureLogHandler
import time
import subprocess
import os
import random

tmp = '/tmp/'
mnt_test = '/ap/'


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # logger = logging.getLogger(__name__)
        # logger.addHandler(AzureLogHandler(
        #     connection_string='InstrumentationKey=468aaf92-e505-456a-8869-2ba7616741dc')
        # )

        start = time.time()
        b = int(req.route_params.get('bs')) * 1024

        bs = 'bs=' + str(b)
        count = 'count=' + req.route_params.get('count')
        out_fd = open(mnt_test + 'io_write_logs', 'w')
        dd = subprocess.Popen(['dd', 'if=/dev/zero', 'of=/ap/out', bs, count], stderr=out_fd)
        dd.communicate()
        end = time.time()
        # subprocess.check_output(['ls', '-alh', mnt_test])

        with open(mnt_test + 'io_write_logs') as logs:
            result = str(logs.readlines()[2]).replace('\n', '')
        now = time.localtime()
        res = {
            'current': str(now.tm_hour) + str(now.tm_min),
            'result': result,
            'start': str(start),
            'end': str(end),
            'scale': req.route_params.get('scale')
        }
        logging.info(res)
        return result + " scale: " + str(res['scale']) + "\n"
    except Exception as ex:
        return str(ex) + "\n"
