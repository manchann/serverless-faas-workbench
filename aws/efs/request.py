import subprocess

# loop_count = input("Enter the count")

bs = input('Enter the bs: ')
count = input('Enter the count: ')


def requester(bs, count):
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/efs-test/?bs=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, count),
        shell=True)
    subprocess.check_call(
        "\curl 'https://oma3z82y67.execute-api.ap-northeast-2.amazonaws.com/version1/tmp-test/?bs=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, count),
        shell=True)


threads = []
requester(bs, count)

# while(loop_count):
#     t = Thread(target=requester, args=(bs, count))
#     t.start()
#     threads.append(t)
#     loop_count -=1

# for t in threads:
#     t.join()
