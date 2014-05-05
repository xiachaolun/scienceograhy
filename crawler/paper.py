from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import paper_list_collection
from utility.tool import prepcessCitingSentence, nearlySameText

# this crawler tends to ignore papers with non-English characters
class PaperCrawler(object):
    def __init__(self):

        self.mongodb_interface = MongoDBInterface()
        #self.mongodb_interface.setCollection(paper_list_collection)

    def _crawlCitingContext(self, url):
        hmtl = pq(url)

        #print hmtl

        citing_info = []
        for item in hmtl('li').filter('.paper-citation-item').items():

            # get citing sentences
            citing_sentences = []
            for doc in item('ul').filter('.quot')('li').items():
                citing_sentence = doc.text()
                #print citing_sentence
                citing_sentence = prepcessCitingSentence(citing_sentence)
                citing_sentences.append(citing_sentence)

            # get citing author and paper information
            tmp = item('a')
            citing_author = str(tmp.eq(0).attr('href')).split('/')[2]
            citing_paper = str(tmp.eq(1).attr('href')).split('/')[1]
            citing_info.append([citing_sentences, citing_author, citing_paper])

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
                print 'no more citing sentences'
            else:
                res += tmp_res
            start += 10

if __name__ == '__main__':
    plc = PaperCrawler()
    plc.crawlCitingContext('781416')
    #print plc._crawlCitingContext('http://academic.research.microsoft.com/Detail?entitytype=1&searchtype=7&id=781416&start=691&end=700')