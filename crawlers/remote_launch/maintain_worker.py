import psutil

def maintain():
    cmdline = 'run_worker.py'

    procs = []
    for proc in psutil.process_iter():
        if proc.username() == 'cx28':
            for part in proc.cmdline():
                if cmdline in part:
                    procs.append(proc)
    if len(procs) <= 1:
        print 'good'
        return

    print 'need to kill'

    for i in xrange(len(procs) - 1):
        try:
            proc[i].kill()
        except Exception, e:
            print e

if __name__ == '__main__':
    maintain()