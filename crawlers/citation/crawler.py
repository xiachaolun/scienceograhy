from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_paper_with_citation
from utility.tool import *
from pprint import pprint

import time
import random


# this crawlers tends to ignore papers with non-English characters
# only download citing context

def crawlCitationPaperGivenUrl(url):
    hmtl = pq(url)
    ids = []
    for item in hmtl('li').filter('.paper-item').items():
        href = item('a').filter(lambda i: '_Title' in str(pq(this).attr('id'))).attr('href')
        citing_paper_id = int(href.split('/')[1])
        ids.append(citing_paper_id)

    return ids

def crawlCitationPaperGivenPaperId(paper_id):
    fail = 0
    start = 1
    ids = set()
    while fail < 3:
        end = start + 9
        url = 'http://academic.research.microsoft.com/' \
              'Detail?entitytype=1&searchtype=5&id=%d&start=%d&end=%d' % (paper_id, start, end)
        print url
        crawled_ids = crawlCitationPaperGivenUrl(url)
        if len(crawled_ids) == 0:
            fail += 1
            #print 'no more citing sentences'
        else:
            for crawled_id in crawled_ids:
                ids.add(crawled_id)
            # reset
            fail = 0

        start += 10
        randomSleep()

    return [id for id in ids]


def crawlCitationPaper(paper):
    # no need to sleep in this method
    paper_id = paper['_id']

    ids = crawlCitationPaperGivenPaperId(paper_id)

    # no need to return
    paper['citing_papers'] = [id for id in ids]
    interface = MongoDBInterface()
    interface.setCollection(main_paper_with_citation)
    interface.saveDocument(paper)
