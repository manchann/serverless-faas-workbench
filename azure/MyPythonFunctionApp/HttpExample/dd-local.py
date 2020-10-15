import logging
import json
import azure.functions as func
import asyncio
from opencensus.ext.azure.log_exporter import AzureLogHandler
import time
import subprocess
import os
import random
import tempfile

tmp = '/tmp/'
mnt_test = '/tmp/'

readfile = 'readfile'
out_path = '/out/'


async def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # logger = logging.getLogger(__name__)
        # logger.addHandler(AzureLogHandler(
        #     connection_string='InstrumentationKey=468aaf92-e505-456a-8869-2ba7616741dc')
        # )
        local_path = tempfile.gettempdir()
        start = time.time()
        b = int(req.route_params.get('bs')) * 1024

        bs = 'bs=' + str(b)
        count = 'count=' + req.route_params.get('count')
        out_fd = open(mnt_test + 'io_write_logs', 'w')
        dd = subprocess.Popen(
            ['dd', 'if=/dev/zero', 'of=/tmp/out'+str(time.time()), bs, count],
            stderr=out_fd)
        dd.communicate()
        end = time.time()
        # subprocess.check_output(['ls', '-alh', mnt_test])

        with open(mnt_test + 'io_write_logs') as logs:
            result = str(logs.readlines()[2]).replace('\n', '')
            latency = result.split(',')[2]
        res = {
            'test': str(req.route_params.get('test')),
            'result': result,
            'start': str(start),
            'end': str(end),
            'scale': req.route_params.get('scale')
        }
        # res = json.dumps(res)
        logging.info(json.dumps(res))
        return result + " scale: " + str(res['scale']) + " latency:"+ latency + "\n"
    except Exception as ex:
        return str(ex) + "\n"
