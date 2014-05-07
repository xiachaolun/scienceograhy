import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *


def _getMainPaperId():
    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)
    ids = set()
    for doc in mi.getAllDocuments(fields_to_select=['_id']):
        ids.add(doc['_id'])
    return ids

def _getMainPaperCitationId():
    mi = MongoDBInterface()
    mi.setCollection(main_paper_with_citation)
    ids = set()
    for doc in mi.getAllDocuments(fields_to_select=['citing_papers']):
        for id in doc['citing_papers']:
            ids.add(id)
    return ids

def _getMainPaperContextId():
    # citing sentences
    mi = MongoDBInterface()
    mi.setCollection(main_paper_with_context)
    ids = set()
    for doc in mi.getAllDocuments(fields_to_select=['citing_sentences']):
        for sentences, author_id, paper_id in doc['citing_sentences']:
            ids.add(paper_id)
    return ids

def _getMainPaperReferenceId():
    # citing sentences
    mi = MongoDBInterface()
    mi.setCollection(main_paper_with_reference)
    ids = set()
    for doc in mi.getAllDocuments(fields_to_select=['references']):
        for id in doc['references']:
            ids.add(id)
    return ids

def getAllPaperId():
    data_set =  _getMainPaperContextId().union(_getMainPaperCitationId())\
        .union(_getMainPaperId()).union(_getMainPaperReferenceId())
    return [id for id in data_set]

if __name__ == '__main__':
    print len(getAllPaperId())