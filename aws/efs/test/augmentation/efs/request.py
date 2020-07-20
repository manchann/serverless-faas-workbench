import subprocess
import time


def requester(bs, count, test):
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/efs-test/?bs=%22'{}'%22&count=%22'{}'%22&test=%22'{}'%22#'".format(
            bs, count, test),
        shell=True)
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/tmp-test/?bs=%22'{}'%22&count=%22'{}'%22&test=%22'{}'%22#'".format(
            bs, count, test),
        shell=True)


test_set3 = [
    {'bs': '64', 'count': '10', 'test': 'test3'},
    {'bs': '64', 'count': '10', 'test': 'test3'},

]

for obj in test_set3:
    requester(obj['bs'], obj['count'], obj['test'])
