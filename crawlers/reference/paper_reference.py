from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import prepcessCitingSentence, nearlySameText
from pprint import pprint

import time
import random

from base_crawler import BaseCrawler

# this crawlers tends to ignore papers with non-English characters
# only download citing context
class PaperReferenceCrawler(BaseCrawler):
    def __init__(self):
        self.mongodb_interface = MongoDBInterface()
        self.mongodb_interface.setCollection(main_paper_with_reference)

    def _crawlReferencePaper(self, url):
        hmtl = pq(url)

        #print hmtl
        ids = []
        for item in hmtl('li').filter('.paper-item').items():
            href = item('a').filter(lambda i: '_Title' in str(pq(this).attr('id'))).attr('href')
            citing_paper_id = int(href.split('/')[1])
            ids.append(citing_paper_id)

        return ids

    def crawlReferencePaper(self, id):
        id = int(id)
        fail = 0
        start = 1
        res = []
        while fail < 3:
            end = start + 9
            url = 'http://academic.research.microsoft.com/' \
                  'Detail?entitytype=1&searchtype=2&id=%d&start=%d&end=%d' % (id, start, end)
            print url
            tmp_res = self._crawlReferencePaper(url)
            if len(tmp_res) == 0:
                fail += 1
                #print 'no more citing sentences'
            else:
                res += tmp_res
                # reset
                fail = 0

            start += 10
            self._sleep('short')

            # for debug only
            #break
        return res

    def getReferencePaper(self):
        cnt =  0
        cur = self.mongodb_interface.getAllDocuments(sorting_info=[('total_citation', 1), ('_id', -1)])
        for doc in cur:
            cnt += 1
            print cnt
            #print doc
            if len(doc.get('references', [])) > 0:
                continue
            res = self.crawlReferencePaper(doc['_id'])
            doc['references'] = res
            #pprint(res)
            self.mongodb_interface.updateDocument(doc)
            self._sleep('long')



if __name__ == '__main__':
    aa = PaperReferenceCrawler()
    aa.getReferencePaper()
    # aa._crawlReferencePaper('http://academic.research.microsoft.com/'
    #                        'Detail?entitytype=1&searchtype=2&id=762211&start=1&end=10')