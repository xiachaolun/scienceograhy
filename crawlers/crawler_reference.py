from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import randomSleep


def crawlReferenceGivenUrl(url):
    hmtl = pq(url)

    #print hmtl
    ids = []
    for item in hmtl('li').filter('.paper-item').items():
        href = item('a').filter(lambda i: '_Title' in str(pq(this).attr('id'))).attr('href')
        citing_paper_id = int(href.split('/')[1])
        ids.append(citing_paper_id)

    return ids

def crawlReferenceGivenPaperId(id):
    id = int(id)
    fail = 0
    start = 1
    res = []
    while fail < 3:
        end = start + 9
        url = 'http://academic.research.microsoft.com/' \
              'Detail?entitytype=1&searchtype=2&id=%d&start=%d&end=%d' % (id, start, end)
        print url
        tmp_res = crawlReferenceGivenUrl(url)
        if len(tmp_res) == 0:
            fail += 1
            #print 'no more citing sentences'
        else:
            res += tmp_res
            # reset
            fail = 0

        start += 10
        randomSleep()

        # for debug only
        #break
    return res

def crawlReferencePaper(paper):
    # no need to sleep in this method
    paper_id = paper['_id']

    ids = crawlReferenceGivenPaperId(paper_id)

    # no need to return
    paper['references'] = [id for id in ids]
    interface = MongoDBInterface()
    interface.setCollection(main_paper_with_reference)
    interface.saveDocument(paper)