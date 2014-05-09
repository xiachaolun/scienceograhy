from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_paper_with_abstract, other_paper_with_abstract
from utility.tool import prepcessCitingSentence, randomSleep
from pprint import pprint

import time
import random

def crawlAbstractGivenPaperId(paper_id):
    url = 'http://academic.research.microsoft.com/Publication/%d/' % (int(paper_id))
    print url
    html = pq(url)
    #print html

    # common info
    paper_card = html('div').filter('.paper-card')

    # get author of this paper
    authors = []
    for author in paper_card('a').filter('.author-name-tooltip').items():
        author_id = int(author.attr('href').split('/')[-2].strip())
        authors.append(author_id)

    # get abstract
    abstract = ''
    try:
        abstract = paper_card('div').filter('.abstract').text()
        abstract = prepcessCitingSentence(abstract)
    except Exception, e:
        pass
        # print 'no abstract for this paper'

    # get venue infor
    year = -1
    venue_type = -1
    venue_id = -1

    info = paper_card('div').filter('.conference')

    try:
        year = int(info('span').eq(1).text().strip()[-4:])
    except Exception, e:
        pass
        # print 'no year information: %s' % (e)

    if year == -1 or year == '':
        try:
            year = int(info('span').text().strip('. ')[-4:])
        except Exception, e:
            # print 'bad year information: %s' % (e)
            year = -1

    #print info('span').text(), info('span').text().strip('. ')[-4:]

    try:
        venue_href = info('a').filter('.conference-name').attr('href')
        venue_type = venue_href.split('/')[-3]
        venue_id = venue_type + '/' + venue_href.split('/')[-2]
    except Exception, e:
        pass
        # print 'no venue info: %s' % e

    try:
        assert (year >= 1998 and year <= 2014) or year == -1
    except Exception, e:
        print year, e
        year = -1

    res = {}
    res['authors'] = authors
    res['abstract'] = abstract
    res['venue_type'] = venue_type
    res['venue_id'] = venue_id
    res['year'] = year

    randomSleep()

    return res

def crawlMainPaperAbstract(paper):
    paper['meta'] = crawlAbstractGivenPaperId(paper['_id'])
    interface = MongoDBInterface()
    interface.setCollection(main_paper_with_abstract)
    interface.saveDocument(paper)

def crawlOtherPaperAbstract(paper):
    paper['meta'] = crawlAbstractGivenPaperId(paper['_id'])
    interface = MongoDBInterface()
    interface.setCollection(other_paper_with_abstract)
    interface.saveDocument(paper)

if __name__ == '__main__':
    doc = {}
    doc['_id'] = 298841
    crawlOtherPaperAbstract(doc)
    #crawlAbstractGivenPaperId(298841)