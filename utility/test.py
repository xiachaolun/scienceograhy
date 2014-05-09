import psutil

cmdline = '/grad/users/cx28/scienceograhy/crawlers/run_worker.py'

cnt = 0
for proc in psutil.process_iter():
    if proc.username() == 'cx28' and cmdline in proc.cmdline():
            cnt += 1
print cnt