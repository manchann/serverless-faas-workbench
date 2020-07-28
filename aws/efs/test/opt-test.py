from time import time
import subprocess
import os
import boto3
import decimal
import random


def lambda_handler(event, context):
    with open('/opt/python/test', 'rb', 0) as f:
        f.read()
    return True
