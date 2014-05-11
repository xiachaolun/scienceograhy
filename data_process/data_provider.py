import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *

from pprint import pprint


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

def getOtherPaperId():
    data_set = _getMainPaperContextId().union(_getMainPaperCitationId())\
        .union(_getMainPaperId()).union(_getMainPaperReferenceId())
    return [id for id in data_set]

def getAllAuthorId():
    mi = MongoDBInterface()
    mi.setCollection(main_paper_with_abstract)
    author_set = set()
    for paper in mi.getAllDocuments():
        for author in paper['meta']['authors']:
            author_set.add(author)
    return [author for author in author_set]

def getAllVenueId():
    venue_ids = set()
    mi = MongoDBInterface()
    mi.setCollection(main_paper_with_abstract)

    for doc in mi.getAllDocuments(fields_to_select=['meta.venue_id']):
        venue_ids.add(doc['meta']['venue_id'])

    mi.disconnect()

    mi = MongoDBInterface()
    mi.setCollection(other_paper_with_abstract)
    for doc in mi.getAllDocuments(fields_to_select=['meta.venue_id']):
        venue_ids.add(doc['meta']['venue_id'])
    mi.disconnect()
    pprint(venue_ids)

def getAllPaperAbstractInfo(condition):

    res = {}
    mi = MongoDBInterface()

    mi.setCollection(main_paper_with_abstract)
    for paper in mi.getAllDocuments(condition):
        res[paper['_id']] = paper
    mi.setCollection(other_paper_with_abstract)
    for paper in mi.getAllDocuments(condition):
        res[paper['_id']] = paper

    return res

def getAllVenueInfo():
    mi = MongoDBInterface()
    mi.setCollection(all_venue_with_info)

    venues = {}
    for venue in mi.getAllDocuments(condition={'domain':3}):
        venues[venue['_id']] = venue

    return venues

if __name__ == '__main__':
    pprint(getAllVenueInfo())