from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_author_list
from utility.tool import hasNextPage, randomSleep, prepcessCitingSentence, parseTimeSeriesData

from pprint import pprint

import re

def _crawlPaperGivenUrl(url):
    # this method is equivalent to crawlReferenceGivenUrl
    hmtl = pq(url)

    #print hmtl
    ids = set()
    for item in hmtl('li').filter('.paper-item').items():
        href = item('a').filter(lambda i: '_Title' in str(pq(this).attr('id'))).attr('href')
        citing_paper_id = int(href.split('/')[1])
        ids.add(citing_paper_id)

    return ids

def _crawlAuthorPublication(author_id):
    start = 1
    end = 100
    all_ids = set()
    while True:
        publication_url = 'http://academic.research.microsoft.com/' \
                          'Detail?entitytype=2&searchtype=2&id=%d&start=%d&end=%d' % (author_id, start, end)
        print publication_url
        ids = _crawlPaperGivenUrl(publication_url)
        for id in ids:
            all_ids.add(id)
        randomSleep()
        if hasNextPage(publication_url):
            start += 100
            end += 100
        else:
            break
    return [id for id in all_ids]

def _crawlAuthorInfoGivenId(author_id):
    url = 'http://academic.research.microsoft.com/Author/%d/' % author_id
    html = pq(url)
    author_card = html('div').filter('.author-card')
    # print author_card
    author_name = author_card('span').filter(lambda i: '_authorName' in str(pq(this).attr('id'))).text()
    author_name = str(prepcessCitingSentence(author_name))

    organization_href = author_card('a').filter(lambda i: '_affiliation' in str(pq(this).attr('id'))).attr('href')
    organization_name = author_card('a').filter(lambda i: '_affiliation' in str(pq(this).attr('id'))).attr('title')
    try:
        organization_name = str(prepcessCitingSentence(organization_name))
        organization_id = int(organization_href.strip().split('/')[-2])
    except:
        print 'has no organization'
        organization_name = ''
        organization_id = -1

    publication_number = author_card('a').filter(lambda i: 'publication' in str(pq(this).attr('id'))).text()
    publication_number = int(publication_number)

    citation_number = author_card('a').filter(lambda i: 'citedBy' in str(pq(this).attr('id'))).text()
    citation_number = int(citation_number)

    tmp = author_card('a').filter(lambda i: 'VisualExplore' in str(pq(this).attr('href')))
    try:
        coauthor_number = int(str(tmp.eq(0).text().split()[0]).strip())
    except:
        print 'no coauthor information'
        coauthor_number = -1

    try:
        citing_author_number = int(str(tmp.eq(1).text().split()[0]).strip())
    except:
        print 'no citing author information'
        citing_author_number = -1

    ts = author_card('script').text()
    ts = ts.replace('"', '')
    citation_hist = []
    # for text in ts.split('},{'):
    #     if 'citations' in text and 'year' in text and 'm_Visible:true' in text and 'YTD' not in text:
    #         citation_hist.append(text)

    for text in re.findall('{m_x:.*?,m_y:.*?,m_text:citation.*?}', ts):
        if 'publication' not in text:
            citation_hist.append(text.strip('{} '))

    publication_hist = []
    for text in re.findall('{m_x:.*?,m_y:.*?,m_text:publication.*?}', ts):
        if 'citation' not in text:
            publication_hist.append(text.strip('{} '))


    # for text in ts.split('},{'):
    #     if 'publications' in text and 'year' in text and 'm_Visible:true' in text and 'YTD' not in text:
    #         publication_hist.append(text)

    publication_time_series = parseTimeSeriesData(publication_hist)
    citation_time_series = parseTimeSeriesData(citation_hist)

    publication_paper_ids = _crawlAuthorPublication(author_id)

    author_info = {}
    author_info['_id'] = author_id
    author_info['name'] = author_name
    author_info['organization'] = {}
    author_info['organization']['name'] = organization_name
    author_info['organization']['id'] = organization_id
    author_info['total_publication_count'] = publication_number
    author_info['total_coauthor_count'] = coauthor_number
    author_info['total_citing_author_count'] = citing_author_number
    author_info['total_citation_count'] = citation_number
    author_info['publication_count_time_series'] = publication_time_series
    author_info['citation_count_time_series'] = citation_time_series
    author_info['publication_list'] = publication_paper_ids

    randomSleep()

    return author_info

def crawlAndSaveAuthorInfo(author_id):
    author_info = _crawlAuthorInfoGivenId(author_id)

    ai = MongoDBInterface()
    ai.setCollection(main_author_list)
    ai.saveDocument(author_info)
    ai.disconnect()

# for debug
# def crawlAndSaveAuthorInfo(author_id):
#     ai = MongoDBInterface()
#     ai.setCollection(main_author_list)
#
#     try:
#         author_info = _crawlAuthorInfoGivenId(author_id)
#     except:
#         ai.saveDocument({'_id':author_id})
#
#     #ai.saveDocument(author_info)
#
#     ai.disconnect()


if __name__ == '__main__':
    _crawlAuthorInfoGivenId(49963643)