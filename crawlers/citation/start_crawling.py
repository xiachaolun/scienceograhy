import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import *

import random

from crawler import *

from redis import Redis
from rq import Queue


def crawlPaperCitation():
    # this method crawl citation in non-redis distributed way
    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_citation)

    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)

    docs = [doc for doc in mi.getAllDocuments()]
    mi.disconnect()

    random.shuffle(docs)

    for doc in docs:
        if ci.getOneDocument(condition={'_id': doc['_id']}) is not None:
            continue
        res = crawlCitationPaper(doc['_id'])
        doc['citing_papers'] = res
        #pprint(res)
        ci.saveDocument(doc)
        randomSleep()

    ci.disconnect()

def crawlPaperCitationWithRQ():
    # this method crawl citation in redis distributed way
    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_citation)

    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)

    docs = [doc for doc in mi.getAllDocuments()]
    mi.disconnect()

    random.shuffle(docs)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for doc in docs:
        if ci.getOneDocument(condition={'_id': doc['_id']}) is not None:
            continue

        paras = (doc)
        q.enqueue_call(func=crawlCitationPaperWithRQ,args=(paras,),timeout=3600)

    ci.disconnect()

if __name__ == '__main__':
    #crawlCitationPaperWithRQ({'_id':155})
    crawlPaperCitationWithRQ()
    #crawlPaperCitation()