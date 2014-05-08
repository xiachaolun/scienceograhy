from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_author_list, redis_server
from redis import Redis
from rq import Queue

from crawler_author import crawlAndSaveAuthorInfo

from data_process.data_provider import getAllAuthorId

import random

def getAuthorInfo():

    ci = MongoDBInterface()
    ci.setCollection(main_author_list)

    ids = getAllAuthorId()

    random.shuffle(ids)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for id in ids:
        # if it is already in the db
        if ci.getOneDocument(condition={'_id': id}) is not None:
            print '%d is already there' % id
            continue
        print id
        crawlAndSaveAuthorInfo(id)

    ci.disconnect()

def getAuthorInfoWithRQ():

    ci = MongoDBInterface()
    ci.setCollection(main_author_list)

    ids = getAllAuthorId()

    random.shuffle(ids)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for id in ids:
        # if it is already in the db
        if ci.getOneDocument(condition={'_id': id}) is not None:
            print '%d is already there' % id
            continue
        paras = (id)
        q.enqueue_call(func=crawlAndSaveAuthorInfo,args=(paras,),timeout=3600)

    ci.disconnect()

if __name__ == '__main__':
    #getAuthorInfo()
    getAuthorInfoWithRQ()