import subprocess
import time
from threading import Thread


def requester(bs, fs, test):
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/efs-test/?bs=%22'{}'%22&fs=%22'{}'%22&test=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, fs, test, '0'),
        shell=True)
    # subprocess.check_call(
    #     "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/tmp-test/?bs=%22'{}'%22&fs=%22'{}'%22&test=%22'{}'%22&count=%22'{}'%22#'".format(
    #         bs, fs, test, '0'),
    #     shell=True)


# fs(MB) if fs = 1 -> 1MB
test_set1 = [
    {'bs': '1024', 'fs': '100', 'test': 'test1'},
    {'bs': '1024', 'fs': '100', 'test': 'test2'},
    {'bs': '1024', 'fs': '100', 'test': 'test3'},
    {'bs': '1024', 'fs': '100', 'test': 'test4'},
    {'bs': '1024', 'fs': '100', 'test': 'test5'},
    {'bs': '1024', 'fs': '100', 'test': 'test6'},
]
# testing bs changes
test_set2 = [
    {'bs': '256', 'fs': '100', 'test': 'test1'},
    {'bs': '256', 'fs': '100', 'test': 'test2'},
    {'bs': '256', 'fs': '100', 'test': 'test3'},
    {'bs': '256', 'fs': '100', 'test': 'test4'},
    {'bs': '256', 'fs': '100', 'test': 'test5'},
    {'bs': '256', 'fs': '100', 'test': 'test6'},
]
# testing cold start using efs
test_set3 = [
    {'bs': '512', 'fs': '1', 'test': 'test3'},
    {'bs': '512', 'fs': '1', 'test': 'test3'},
    {'bs': '1024', 'fs': '5', 'test': 'test3'},
    {'bs': '1024', 'fs': '5', 'test': 'test3'},
]

# efs scalablity testset

efs_strong1 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]
efs_strong10 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong10', 'scale': 10},
]
efs_strong20 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong20', 'scale': 20},
]
efs_strong50 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong50', 'scale': 50},
]
efs_strong100 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong100', 'scale': 100},
]
efs_strong200 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong200', 'scale': 200},
]

threads_1 = []
for obj in efs_strong100:
    for i in range(obj['scale']):
        t = Thread(target=requester, args=(obj['bs'], obj['fs'], obj['test']))
        t.start()
        threads_1.append(t)
    for t in threads_1:
        t.join()

# threads_2 = []
# for obj in test_set1:
#     t = Thread(target=requester, args=(obj['bs'], obj['fs'], obj['test']))
#     t.start()
#     threads_2.append(t)
# for t in threads_2:
#     t.join()

# for obj in test_set1:
#     requester(obj['bs'], obj['fs'], obj['test'])
#
# for obj in test_set2:
#     requester(obj['bs'], obj['fs'], obj['test'])

# for obj in test_set3:
#     requester(obj['bs'], obj['fs'], obj['test'])
