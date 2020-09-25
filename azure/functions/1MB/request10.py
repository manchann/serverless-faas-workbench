import subprocess
import time
from threading import Thread


def requester(bs, count):
    subprocess.check_call(
        "\curl 'https://jgfuncrandom.azurewebsites.net/api/HttpExample/{}/{}?code=XiKx1zPlLSsS2cimGbKIfzjGPOygEV5xbxtIoFGFvoF55M0ldaNkdQ=='".format(
            bs, count),
        shell=True)



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
    {'bs': '1024', 'fs': '200', 'test': 'efs_strong1', 'scale': 1, 'count': 200},
]
efs_strong10 = [
    {'bs': '1024', 'fs': '200', 'test': 'efs_strong10', 'scale': 10, 'count': 200},
]
efs_strong20 = [
    {'bs': '1024', 'fs': '200', 'test': 'efs_strong20', 'scale': 20, 'count': 200},
]
efs_strong50 = [
    {'bs': '1024', 'fs': '200', 'test': 'efs_strong50', 'scale': 50, 'count': 200},
]
efs_strong100 = [
    {'bs': '1024', 'fs': '200', 'test': 'efs_strong100', 'scale': 100, 'count': 200},
]
efs_strong200 = [
    {'bs': '1024', 'fs': '200', 'test': 'efs_strong200', 'scale': 200, 'count': 200},
]

threads_1 = []
for obj in efs_strong10:
    for i in range(obj['scale']):
        t = Thread(target=requester, args=(obj['bs'], obj['count']))
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
