from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import prepcessCitingSentence
from base_crawler import BaseCrawler


# this crawler tends to ignore papers with non-English characters
class PaperListCrawler(BaseCrawler):
    def __init__(self):

        self.mongodb_interface = MongoDBInterface()
        #self.mongodb_interface.setCollection(paper_list)
        self.mongodb_interface.setCollection(all_paper_list)

    def _crawl(self, domain):
        # url = 'http://academic.research.microsoft.com/RankList?entitytype=1&topDomainID=2&subDomainID=7&' \
        #       'last=0&start=1&end=100'
        html = pq(self.url)

        cnt = 0
        is_first = True
        # we should ignore the first item because it is the title of the table
        for item in html('table').filter('.staticTable')('tr').items():
            if is_first:
                is_first = False
                continue
            title_year_info =  item('a')
            publication_url = title_year_info.attr('href')
            tmp = title_year_info.text().strip()

            # example: Classification and Regression Trees (1984)
            title = tmp[0:len(tmp) - 7].strip()
            title = prepcessCitingSentence(title)

            year = tmp[len(tmp) - 5 : -1].strip()

            total_citation_count = item('td').filter('.staticOrderCol').text()

            # here we ignore papers with less than 100 citations
            if int(total_citation_count) < 100:
                continue

            try:
                tuple = [str(title), int(year), str(publication_url), int(total_citation_count), domain]
                cnt += 1
                self._save_to_db(tuple)
                #print tuple
            except Exception, e:
                # here we ignore those without publication year
                pass
                #print e
                #print title, year, publication_url, total_citation_count

        if cnt == 0:
            print 'did not get valid paper from this URL'
            return False

        return True

    def _save_to_db(self, tuple):
        doc = {}
        doc['title'] = tuple[0]
        doc['year'] = tuple[1]
        #doc['url'] = tuple[2]
        doc['total_citation'] = tuple[3]
        doc['field'] = tuple[4]

        tmp = tuple[2].split('/')
        doc['_id'] = int(tmp[2].strip())

        #print doc
        self.mongodb_interface.saveDocument(doc)

    def crawl(self):
        for domain in xrange(1, 25):
            start = 1
            failed = 0
            print 'start crawling papers from domain %d' % domain
            while failed < 3:
                end = start + 99
                # all
                self.url = 'http://academic.research.microsoft.com/' \
                           'RankList?entitytype=1&topDomainID=2&subDomainID=%d&last=0&start=%d&end=%d' % \
                           (domain, start, end)

                print self.url
                if not self._crawl(domain):
                    failed += 1
                else:
                    failed = 0

                # enter into next iteration
                start += 100
                self._sleep('short')

if __name__ == '__main__':
    plc = PaperListCrawler()
    plc.crawl()

# done for ML&PR
# http://academic.research.microsoft.com/RankList?entitytype=1&topDomainID=2&subDomainID=6&last=0&start=146101&end=146200
