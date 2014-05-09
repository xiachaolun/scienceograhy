from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import all_venue_with_info, redis_server
from redis import Redis
from rq import Queue

from crawler_venue_list import crawlAndSaveVenueList

def getVenueList():

    ci = MongoDBInterface()
    ci.setCollection(all_venue_with_info)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for domain in xrange(1, 50):
        for venue_type in [3, 4]:
            crawlAndSaveVenueList(venue_type, domain)

    ci.disconnect()

def getVenueListWithRQ():

    ci = MongoDBInterface()
    ci.setCollection(all_venue_with_info)

    redis_conn = Redis(redis_server)
    q = Queue(connection=redis_conn)

    for domain in xrange(1, 50):
        for venue_type in [3, 4]:
            paras = (venue_type, domain)
            q.enqueue_call(func=crawlAndSaveVenueList,args=(paras,),timeout=3600)

    ci.disconnect()

if __name__ == '__main__':
    #getVenueList()
    getVenueListWithRQ()