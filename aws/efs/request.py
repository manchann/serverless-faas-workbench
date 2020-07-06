import subprocess
import time


def requester(bs, count):
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/efs-test/?bs=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, count),
        shell=True)
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/tmp-test/?bs=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, count),
        shell=True)


test_set = [
    {'bs': '1', 'count': '1'}
]

for obj in test_set:
    requester(obj['bs'], obj['count'])
