from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import all_venue_with_info
from utility.tool import randomSleep, prepcessCitingSentence, parseTimeSeriesData

from pprint import pprint

import re

def _crawlVenueInfoGivenId(venue_id):
    # venue id: Conference/197
    url = 'http://academic.research.microsoft.com/%s/' % venue_id
    html = pq(url)
    venue_card = html('div').filter('.conference-card')
    # print author_card
    venue_name = venue_card('div').filter('.card-title')('span').filter(lambda i: '_name' in str(pq(this).attr('id'))).text()
    venue_name = str(prepcessCitingSentence(venue_name))

    tmp = venue_card('div').filter('.detailInfo')('span').eq(0).text().strip().split(' ')
    publication_number = int(tmp[1].strip().replace(',', ''))
    citation_number = int(tmp[5].strip().replace(',', ''))
    self_citation_number = int(tmp[7].strip(') ').replace(',', ''))

    ts = venue_card('script').text()
    ts = ts.replace('"', '')

    citation_hist = []
    for text in re.findall('{m_x:.*?,m_y:.*?,m_text:citation.*?}', ts):
        if 'publication' not in text:
            citation_hist.append(text.strip('{} '))

    publication_hist = []
    for text in re.findall('{m_x:.*?,m_y:.*?,m_text:publication.*?}', ts):
        if 'citation' not in text:
            publication_hist.append(text.strip('{} '))

    publication_time_series = parseTimeSeriesData(publication_hist)
    citation_time_series = parseTimeSeriesData(citation_hist)

    venue_info = {}
    venue_info['_id'] = venue_id
    venue_info['name'] = venue_name
    venue_info['total_publication_count'] = publication_number
    venue_info['total_citation_count'] = citation_number
    venue_info['total_self_citation_number'] = self_citation_number
    venue_info['publication_count_time_series'] = publication_time_series
    venue_info['citation_count_time_series'] = citation_time_series

    randomSleep()

    return venue_info

def crawlAndSaveVenueInfo(venue_id):
    venue_info = _crawlVenueInfoGivenId(venue_id)

    ai = MongoDBInterface()
    ai.setCollection(all_venue_with_info)
    old_venue = ai.getOneDocument({'_id':venue_id})
    assert old_venue is not None
    new_venue = dict(old_venue.items() + venue_info.items())
    ai.saveDocument(new_venue)

    ai.disconnect()

if __name__ == '__main__':
    pprint(_crawlVenueInfoGivenId('Conference/838'))