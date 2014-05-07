from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_paper_with_abstract, main_paper_list, other_paper_with_abstract, redis_server
from redis import Redis
from rq import Queue

from abstract_crawler import crawlMainPaperAbstract, crawlOtherPaperAbstract

from data_process.data_provider import getOtherPaperId

import random

def getMainPaperAbstract():

    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)

    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_abstract)

    docs = [doc for doc in mi.getAllDocuments()]
    mi.disconnect()

    random.shuffle(docs)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for doc in docs:

        # if it is already in the db
        if ci.getOneDocument(condition={'_id': doc['_id']}) is not None:
            print '%d is already there' % doc['_id']
            continue

        crawlMainPaperAbstract(doc)

    ci.disconnect()

def getMainPaperAbstractWithRQ():

    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)

    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_abstract)

    docs = [doc for doc in mi.getAllDocuments()]
    mi.disconnect()

    random.shuffle(docs)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for doc in docs:

        # if it is already in the db
        if ci.getOneDocument(condition={'_id': doc['_id']}) is not None:
            print '%d is already there' % doc['_id']
            continue

        paras = (doc)
        q.enqueue_call(func=crawlMainPaperAbstract,args=(paras,),timeout=3600)

    ci.disconnect()

def getOtherPaperAbstractWithRQ():

    ci = MongoDBInterface()
    ci.setCollection(other_paper_with_abstract)

    ids = getOtherPaperId()

    random.shuffle(ids)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for id in ids:

        doc = {}
        doc['_id'] = id
        # if it is already in the db
        if ci.getOneDocument(condition={'_id': doc['_id']}) is not None:
            print '%d is already there' % doc['_id']
            continue

        paras = (doc)
        q.enqueue_call(func=crawlOtherPaperAbstract,args=(paras,),timeout=3600)

    ci.disconnect()



if __name__ == '__main__':
    getMainPaperAbstractWithRQ()
    getOtherPaperAbstractWithRQ()