import psutil

def maintain():
    cmdline = 'run_worker.py'

    cnt = 0
    for proc in psutil.process_iter():
        if proc.username() == 'cx28':
            for part in proc.cmdline():
                if cmdline in part:
                    cnt += 1
    if cnt == 1:
        print 'good'
        return

    print 'need to kill'

    for proc in psutil.process_iter():
        if proc.username() == 'cx28':
            for part in proc.cmdline():
                if cmdline in part:
                    if cnt > 1:
                        cnt -= 1
                        try:
                            proc.kill()
                        except Exception, e:
                            print e

if __name__ == '__main__':
    maintain()