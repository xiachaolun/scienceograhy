import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import *

import random

from crawler_context import crawlCitingContext

from redis import Redis
from rq import Queue

def getCitingContext():

    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)

    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_context)

    docs = [doc for doc in mi.getAllDocuments()]
    mi.disconnect()

    random.shuffle(docs)

    for doc in docs:
        # if it is already in the db
        if ci.getOneDocument(condition={'_id': doc['_id']}) is not None:
            print '%d is already there' % doc['_id']
            continue
        crawlCitingContext(doc)

    ci.disconnect()

def getCitingContextWithRQ():

    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)

    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_context)

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
        q.enqueue_call(func=crawlCitingContext,args=(paras,),timeout=time_out)

    ci.disconnect()

if __name__ == '__main__':
    #getCitingContext()
    getCitingContextWithRQ()