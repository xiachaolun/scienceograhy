import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from data_provider import getOtherPaperId

def checkCitation():
    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_citation)

    for doc in ci.getAllDocuments():
        # print len(doc['citing_papers'])
        assert len(doc['citing_papers']) >= 100

def checkContext():
    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_context)

    for doc in ci.getAllDocuments():
        print len(doc['citing_sentences']), doc['_id']

def checkAbstract():
    ids = getOtherPaperId()
    ci = MongoDBInterface()
    ci.setCollection(other_paper_with_abstract)
    for id in ids:
        if ci.getOneDocument({'_id':id}) is None:
            print id

def checkVenueInfo():
    ci = MongoDBInterface()
    ci.setCollection(all_venue_with_info)
    abn = []
    for doc in ci.getAllDocuments():
        if 'publication_count_time_series' not in doc.keys():
            abn.append(doc['_id'])

    print len(abn)
    for id in abn:
        print id

if __name__ == '__main__':
    checkVenueInfo()
    # checkCitation()
    # checkContext()
