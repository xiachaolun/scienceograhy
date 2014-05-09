from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import all_venue_with_info
from utility.tool import randomSleep

from pprint import pprint

import re

def _hasNextPage(html):
    #print html('div').filter('.rankList-pageNav-container')('a').attr('title')
    res = html('div').filter('.rankList-pageNav-container')('a')\
        .filter(lambda i: 'Go to next page' in str(pq(this).attr('title')))
    return len(res) > 0


def crawlVenueListGivenUrl(url):
    html = pq(url)
    res = []
    has_next_page =  _hasNextPage(html)
    for row in html('table').filter('.staticTable')('tbody')('tr').items():
        tmp = row('a').attr('href').strip(' /').split('/')
        venue_id = tmp[0] + '/' + tmp[1]
        venue_type = tmp[0]
        field_rating = int(row('td').filter('.staticOrderCol').eq(1).text())
        venue_info = {'_id':venue_id, 'venue_type':venue_type, 'field_rating':field_rating}
        res.append(venue_info)

    randomSleep()
    return res, has_next_page

def crawlVenueListGivenDomain(venue_type, domain_id):
    # 3 indicates Conference and 4 for Journal
    assert venue_type in ['Conference', 'Journal']
    venue_type_id = 3 if venue_type == 'Conference' else 4
    start = 1
    end = 100
    res = []
    while True:
        url = 'http://academic.research.microsoft.com/' \
          'RankList?entitytype=%d&topDomainID=%d&subDomainID=0&last=0&start=%d&end=%d&orderBy=6' \
          % (venue_type_id, domain_id, start, end)

        print url
        res_segment, has_next_page = crawlVenueListGivenUrl(url)
        res += res_segment
        if has_next_page:
            start += 100
            end += 100
        else:
            break
    # clean
    n = len(res)
    for i in xrange(n):
        res[i]['field_ranking'] = i + 1
        res[i]['total_venue_in_field'] = n
        res[i]['field_ranking_percentile'] = round((i + 1) * 100.0 / n, 2)
        res[i]['domain'] = domain_id

    return res

def crawlAndSaveVenueList(venue_type, domain_id):
    res = crawlVenueListGivenDomain(venue_type, domain_id)

    mi = MongoDBInterface()
    mi.setCollection(all_venue_with_info)

    for venue in res:
        if mi.getOneDocument({'_id':venue['_id']}) is None:
            mi.saveDocument(venue)

if __name__ == '__main__':
    res = crawlVenueListGivenDomain('Journal', 22)
    for venue in res:
        pprint(venue)
    # pprint(crawlVenueListGivenUrl('http://academic.research.microsoft.com/'
    #                        'RankList?entitytype=4&topDomainID=2&subDomainID=0&last=0&start=101&end=200&orderBy=6'))