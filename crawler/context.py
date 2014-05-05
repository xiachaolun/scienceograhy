from pyquery import PyQuery as pq
from lxml import etree
import urllib

prefix = 'http://academic.research.microsoft.com/'


def test():
    url = 'http://academic.research.microsoft.com/Detail?entitytype=1&searchtype=7&id=794575&start=81&end=90'
    html = pq(url)

    # get citing sentences
    for citation in html('li').filter('.paper-citation-item').items():
        for d in citation('li')('div')('ul')('li')('li').items():
           print d.text().strip('.').strip()
        print

def test2():
    url = 'http://academic.research.microsoft.com/Detail?entitytype=1&searchtype=7&id=794575&start=81&end=90'
    html = pq(url)

    # get citing sentences
    for citation in html('li').filter('.paper-citation-item').items():
        # author url
        print citation('li')('div')('h3')('a').eq(0).attr('href')
        # paper url
        print citation('li')('div')('h3')('a').eq(1).attr('href')
        break

def test3():
    # url = 'http://academic.research.microsoft.com/RankList?entitytype=1&topDomainID=2&subDomainID=7&' \
    #       'last=0&start=1&end=100'

    # PRIX: Indexing And Querying XML Using Prufer Sequences 2004
    # /Publication/523505/prix-indexing-and-querying-xml-using-pr-fer-sequences 109
    url = 'http://academic.research.microsoft.com/RankList?entitytype=1&topDomainID=2&subDomainID=7&last=0&start=1601&end=1700'
    html = pq(url)
    res = []

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
        year = tmp[len(tmp) - 5 : -1].strip()

        total_citation_count = item('td').filter('.staticOrderCol').text()
        try:
            tuple = [str(title), int(year), str(publication_url), int(total_citation_count)]
            res.append(tuple)
            print tuple
        except:
            # here we ignore those without publication year
            print title, year, publication_url, total_citation_count

def test4():
    start = 1
    while True:
        start += 100
        end = start + 99
        url = 'http://academic.research.microsoft.com/RankList?entitytype=1&topDomainID=2&subDomainID=7&' \
            'last=0&start=%d&end=%d' % (start, end)

if __name__ == '__main__':
    test3()