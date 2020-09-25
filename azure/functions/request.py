import subprocess
import time
from threading import Thread


def requester(bs, count):
    subprocess.check_call(
        "\curl 'https://jgfuncrandom.azurewebsites.net/api/HttpExample/bs=%22'{}'%22/count=%22'{}'%22?code=XiKx1zPlLSsS2cimGbKIfzjGPOygEV5xbxtIoFGFvoF55M0ldaNkdQ=='".format(
            bs, count),
        shell=True)


# fs(MB) if fs = 1 -> 1MB
test_set1 = [
    {'bs': '1', 'fs': '10', 'test': 'test1'},
    {'bs': '50', 'fs': '10', 'test': 'test1'},
    {'bs': '512', 'fs': '10', 'test': 'test1'},
    {'bs': '1024', 'fs': '10', 'test': 'test1'},
    {'bs': '2048', 'fs': '10', 'test': 'test1'},
]
# testing bs changes
test_set2 = [
    {'bs': '50', 'fs': '200', 'test': 'test4'},
    {'bs': '256', 'fs': '200', 'test': 'test4'},
    {'bs': '1024', 'fs': '200', 'test': 'test4'},
    {'bs': '2048', 'fs': '200', 'test': 'test4'},
]
# testing cold start using efs
test_set3 = [
    {'bs': '50', 'fs': '200', 'test': 'test3'},
    {'bs': '256', 'fs': '200', 'test': 'test4'},
    {'bs': '50', 'fs': '200', 'test': 'test3'},
    {'bs': '256', 'fs': '200', 'test': 'test4'},
    {'bs': '50', 'fs': '200', 'test': 'test3'},
]

# efs scalablity testset

efs_strong1 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]
efs_strong10 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]
efs_strong20 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]
efs_strong50 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]
efs_strong100 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]
efs_strong200 = [
    {'bs': '256', 'fs': '1', 'test': 'efs_strong1', 'scale': 1},
]

# threads_1 = []
# for obj in test_set1:
#     t = Thread(target=requester, args=(obj['bs'], obj['fs'], obj['test']))
#     t.start()
#     threads_1.append(t)
# for t in threads_1:
#     t.join()

# threads_2 = []
# for obj in test_set2:
#     t = Thread(target=requester, args=(obj['bs'], obj['fs'], obj['test']))
#     t.start()
#     threads_2.append(t)
# for t in threads_2:
#     t.join()

azure_test_set = [
    {

    }
]

threads_3 = []
for obj in test_set3:
    t = Thread(target=requester, args=(obj['bs'], obj['fs'], obj['test']))
    t.start()
    threads_3.append(t)
for t in threads_3:
    t.join()

# for obj in test_set1:
#     requester(obj['bs'], obj['fs'], obj['test'])
#
# for obj in test_set2:
#     requester(obj['bs'], obj['fs'], obj['test'])

# for obj in test_set3:
#     requester(obj['bs'], obj['fs'], obj['test'])
