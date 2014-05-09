import sys
import os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from rq import Queue, Worker, Connection
from redis import Redis

from utility.config import redis_server
import psutil

def checkStatus():
    cmdline = 'run_worker.py'
    cnt = 0
    for proc in psutil.process_iter():
        if proc.username() == 'cx28':
            for part in proc.cmdline():
                if cmdline in part:
                    cnt += 1
    assert cnt >= 1
    return cnt == 1

def startWorker():
    redis_conn = Redis(redis_server)
    with Connection(connection=redis_conn):
        q = Queue()
        Worker(q).work()

if __name__ == '__main__':
    if checkStatus():
        print "there is no worker, start a new one"
        startWorker()
    else:
        print 'already has a worker'