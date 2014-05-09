from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from redis import Redis
from rq import Queue

import random

from crawler_venue_info import crawlAndSaveVenueInfo

def getVenueInfo():

    ci = MongoDBInterface()
    ci.setCollection(all_venue_with_info)

    ids = []
    for doc in ci.getAllDocuments(fields_to_select=['_id', 'publication_count_time_series']):
        if 'publication_count_time_series' not in doc.keys():
            ids.append(doc['_id'])

    random.shuffle(ids)

    for venue_id in ids:
        crawlAndSaveVenueInfo(venue_id)

    ci.disconnect()

def getVenueInfoWithRQ():

    ci = MongoDBInterface()
    ci.setCollection(all_venue_with_info)

    ids = []
    for doc in ci.getAllDocuments(fields_to_select=['_id', 'publication_count_time_series']):
        if 'publication_count_time_series' not in doc.keys():
            ids.append(doc['_id'])

    random.shuffle(ids)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for venue_id in ids:
        q.enqueue_call(func=crawlAndSaveVenueInfo, args=(venue_id,), timeout=time_out)

    ci.disconnect()

if __name__ == '__main__':
    getVenueInfoWithRQ()