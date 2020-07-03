import subprocess


# loop_count = input("Enter the count")

bs, count = input('Enter the bs & count')

def requester(bs, count):
    subprocess.check_call("\curl 'https://2bs4iii4rd.execute-api.ap-northeast-2.amazonaws.com/lambda-test/total/?bs=%22'{}'%22&count=%22'{}'%22#'".format(
            bs, count),
        shell=True)

threads = []
requester(bs,count)

# while(loop_count):
#     t = Thread(target=requester, args=(bs, count))
#     t.start()
#     threads.append(t)
#     loop_count -=1
    
# for t in threads:
#     t.join()
