import logging

import azure.functions as func

import time
import subprocess
import os
import random

tmp = '/tmp/'
mnt_test = '/ap/'


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    try:
        start = time.time()
        print(start)
        time.sleep(1)
        end = time.time()
        print(end)
        return str(start) + " " + str(end) + '\n'
    except Exception as ex:
        return str(ex) + "\n"
