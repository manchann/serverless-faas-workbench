import subprocess
import time
tmp = '/tmp/'
mnt_test = '/mnt/test/'

"""
dd - convert and copy a file
man : http://man7.org/linux/man-pages/man1/dd.1.html
Options 
 - bs=BYTES
    read and write up to BYTES bytes at a time (default: 512);
    overrides ibs and obs
 - if=FILE
    read from FILE instead of stdin
 - of=FILE
    write to FILE instead of stdout
 - count=N
    copy only N input blocks
"""


def lambda_handler(event, context):
    start = time.time()
    bs = 'bs='+event['bs']
    count = 'count='+event['count']

    out_fd = open(mnt_test + 'io_write_logs', 'w')
    dd = subprocess.Popen(['dd', 'if=/dev/zero', 'of=/mnt/test/out', bs, count], stderr=out_fd)
    dd.communicate()
    
    subprocess.check_output(['ls', '-alh', tmp])

    with open(mnt_test + 'io_write_logs') as logs:
        result = str(logs.readlines()[2]).replace('\n', '')
        end = time.time()
        print('test_time',end - start)
        return result