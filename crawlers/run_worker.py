import sys
import os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from rq import Queue, Worker, Connection
from redis import Redis

from utility.config import redis_server
from citing_context.crawler import *

if __name__ == '__main__':
    redis_conn = Redis(redis_server)
    with Connection(connection=redis_conn):
        q = Queue()
        Worker(q).work()