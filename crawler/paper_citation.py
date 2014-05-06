from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_paper_with_context
from utility.tool import prepcessCitingSentence, nearlySameText
from pprint import pprint

import time
import random

# this crawler tends to ignore papers with non-English characters
# only download citing context
class PaperContextCrawler(object):
    def __init__(self):
        self.mongodb_interface = MongoDBInterface()
        self.mongodb_interface.setCollection(main_paper_with_context)

    def _crawlCitationPaper(self, url):
        hmtl = pq(url)
        for item in hmtl('li').filter('.paper-item').items():
            href = item('a').filter(lambda i: '_Title' in str(pq(this).attr('id'))).attr('href')
            citing_paper_id = href.split('/')[1]

    def crawlCitationPaper(self, id):
        id = int(id)
        fail = 0
        start = 1
        res = []
        while fail < 3:
            end = start + 9
            url = 'http://academic.research.microsoft.com/' \
                  'Detail?entitytype=1&searchtype=5&id=%d&start=%d&end=%d' % (id, start, end)
            print url
            tmp_res = self._crawlCitationPaper(url)
            if len(tmp_res) == 0:
                fail += 1
                #print 'no more citing sentences'
            else:
                res += tmp_res
                fail = 0

            start += 10
            sleep_time = random.randint(0,100) % 3
            time.sleep(sleep_time)

            # for debug only
            #break
        return res

    def getCitationPaper(self):
        cnt =  0
        for doc in self.mongodb_interface.getAllDocuments(sorting_info=[('total_citation', 1), ('_id', -1)]):
            cnt += 1
            print cnt
            #print doc
            if len(doc.get('citing_sentences', [])) > 0:
                continue
            res = self.crawlCitationPaper(doc['_id'])
            doc['citing_sentences'] = res
            #pprint(res)
            self.mongodb_interface.updateDocument(doc)
            sleep_time = random.randint(0, 100) % 10
            time.sleep(sleep_time)



if __name__ == '__main__':
    aa = PaperContextCrawler()
    aa._crawlCitationPaper('http://academic.research.microsoft.com/'
                           'Detail?entitytype=1&searchtype=5&id=762211&start=11&end=20')