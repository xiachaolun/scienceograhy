from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import *
from pprint import pprint

import time
import random


def crawCitingContextGivenUrl(url):
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


def crawlCitingContextGivenPaperId(paper_id):
    fail = 0
    start = 1
    res_in_dict = {}
    while fail < 3:
        end = start + 9
        url = 'http://academic.research.microsoft.com/' \
              'Detail?entitytype=1&searchtype=7&id=%d&start=%d&end=%d' % (paper_id, start, end)
        print url
        citing_info_within_one_page = crawCitingContextGivenUrl(url)
        if len(citing_info_within_one_page) == 0:
            fail += 1
            #print 'no more citing sentences'
        else:
            for citing_sentences, citing_author, citing_paper in citing_info_within_one_page:
                res_in_dict[citing_paper] = [citing_sentences, citing_author]
            # rest
            fail = 0
        start += 10

        # for debug only
        #break
        res = []
        for k, v in res_in_dict.items():
            res.append([v[0], v[1], k])

        randomSleep()

    return res

def crawlCitingContext(doc):
    # no need to sleep in this method

    res = crawlCitingContextGivenPaperId(doc['_id'])
    doc['citing_sentences'] = res
    interface = MongoDBInterface()
    interface.setCollection(main_paper_with_context)
    interface.saveDocument(doc)

    return doc

