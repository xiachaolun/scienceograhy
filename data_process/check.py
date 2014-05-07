import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *


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


if __name__ == '__main__':
    checkCitation()
    checkContext()
