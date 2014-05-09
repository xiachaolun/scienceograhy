import psutil


cmdline = '/grad/users/cx28/scienceograhy/'

cnt = 0
for proc in psutil.process_iter():
    if proc.username() == 'cx28':
        for part in cmdline in proc.cmdline():
            if cmdline in part:
                cnt += 1
print cnt