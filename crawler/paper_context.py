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


from base_crawler import BaseCrawler

# this crawler tends to ignore papers with non-English characters
# only download citing context
class PaperContextCrawler(BaseCrawler):
    def __init__(self):
        self.mongodb_interface = MongoDBInterface()
        self.mongodb_interface.setCollection(main_paper_with_context)

    def _crawlCitingContext(self, url):
        hmtl = pq(url)

        #print hmtl

        citing_info = []
        all_sentences = []
        for item in hmtl('li').filter('.paper-citation-item').items():

            # get citing sentences
            citing_sentences = []

            for doc in item('ul').filter('.quot')('li').items():
                citing_sentence = doc.text()
                #print citing_sentence
                citing_sentence = prepcessCitingSentence(citing_sentence)

                # more 20 letters
                if len(citing_sentence) >= 20:
                    similar = False
                    for sentence in all_sentences:
                        if nearlySameText(citing_sentence, sentence):
                            similar = True
                            break
                    if not similar:
                        citing_sentences.append(citing_sentence)
                        all_sentences.append(citing_sentence)

            if len(citing_sentences) > 0:
                # get citing author and paper information
                tmp = item('a')
                #print tmp
                #print str(tmp.eq(1).attr('href'))
                try:
                    citing_author = str(tmp.eq(0).attr('href')).split('/')[2]
                    citing_paper = str(tmp.eq(1).attr('href')).split('/')[1]
                    citing_info.append([citing_sentences, citing_author, citing_paper])
                except Exception, e:
                    print e

        return citing_info

    def crawlCitingContext(self, id):
        id = int(id)
        fail = 0
        start = 1
        res = []
        while fail < 3:
            end = start + 9
            url = 'http://academic.research.microsoft.com/' \
                  'Detail?entitytype=1&searchtype=7&id=%d&start=%d&end=%d' % (id, start, end)
            print url
            tmp_res = self._crawlCitingContext(url)
            if len(tmp_res) == 0:
                fail += 1
                #print 'no more citing sentences'
            else:
                res += tmp_res
                # rest
                fail = 0
            start += 10
            self._sleep('short')

            # for debug only
            #break
        return res

    def getCitingContext(self):
        cnt =  0
        for doc in self.mongodb_interface.getAllDocuments(sorting_info=[('total_citation', 1), ('_id', -1)]):
            cnt += 1
            print cnt
            #print doc
            if len(doc.get('citing_sentences', [])) > 0:
                continue
            res = self.crawlCitingContext(doc['_id'])
            doc['citing_sentences'] = res
            #pprint(res)
            self.mongodb_interface.updateDocument(doc)
            self._sleep('long')



if __name__ == '__main__':
    pl = PaperContextCrawler()
    #pl._crawlCitingContext('http://academic.research.microsoft.com/Detail?entitytype=1&searchtype=7&id=1356162&start=2871&end=2880')
    pl.getCitingContext()
    #print plc._crawlCitingContext('http://academic.research.microsoft.com/Detail?entitytype=1&searchtype=7&id=781416&start=691&end=700')