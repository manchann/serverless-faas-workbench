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

# testing count changes
test_set1 = [
    {'bs': '10M', 'count': '1', 'test': 'test1'},
    {'bs': '10M', 'count': '5', 'test': 'test1'},
    {'bs': '10M', 'count': '10', 'test': 'test1'},
    {'bs': '10M', 'count': '20', 'test': 'test1'},
    {'bs': '10M', 'count': '40', 'test': 'test1'},
    {'bs': '10M', 'count': '80', 'test': 'test1'},
    {'bs': '10M', 'count': '160', 'test': 'test1'},
    {'bs': '10M', 'count': '320', 'test': 'test1'},
    {'bs': '10M', 'count': '640', 'test': 'test1'},
]
# testing bs changes
test_set2 = [
    {'bs': '64', 'count': '10', 'test': 'test2'},
    {'bs': '64', 'count': '10', 'test': 'test2'},
    {'bs': '128', 'count': '10', 'test': 'test2'},
    {'bs': '256', 'count': '10', 'test': 'test2'},
    {'bs': '512', 'count': '10', 'test': 'test2'},
    {'bs': '1024', 'count': '10', 'test': 'test2'},
    {'bs': '2M', 'count': '10', 'test': 'test2'},
    {'bs': '4M', 'count': '10', 'test': 'test2'},
    {'bs': '8M', 'count': '10', 'test': 'test2'},
    {'bs': '16M', 'count': '10', 'test': 'test2'},
    {'bs': '32M', 'count': '10', 'test': 'test2'},
    {'bs': '64M', 'count': '10', 'test': 'test2'},
    {'bs': '128M', 'count': '10', 'test': 'test2'},
    {'bs': '256M', 'count': '10', 'test': 'test2'},
    {'bs': '512M', 'count': '10', 'test': 'test2'},
    {'bs': '1024M', 'count': '10', 'test': 'test2'},
]
# testing cold start using efs
test_set3 = [
    {'bs': '64', 'count': '10', 'test': 'test3'},
    {'bs': '64', 'count': '10', 'test': 'test3'},

]
# for obj in test_set1:
#     requester(obj['bs'], obj['count'], obj['test'])
#
# for obj in test_set2:
# #     requester(obj['bs'], obj['count'], obj['test'])

for obj in test_set3:
    requester(obj['bs'], obj['count'], obj['test'])
