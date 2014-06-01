import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from data_provider import getAllPaperAbstractInfo

from pprint import pprint

# def process():
#     interface = MongoDBInterface()
#     interface.setCollection(paper_list)
#     cur = interface.getAllDocuments()
#     for doc in cur:
#         id = str(doc['_id'])
#         if 'Publication' in id:
#             id = id.split('/')[2].strip()
#             interface._deleteDocument(condition={'_id':doc['_id']})
#
#         doc['_id'] = int(id)
#         interface.saveDocument(doc)

def selectMainPapers():
    interface = MongoDBInterface()
    interface.setCollection(all_paper_list)
    cur = interface.getAllDocuments(condition={'total_citation':{'$gte':15},
                                               'year':1999})
    interface2 = MongoDBInterface()
    interface2.setCollection(main_paper_list)

    for doc in cur:
        interface2.saveDocument(doc)

def mergeAllDataOfMainPaper():
    interface = MongoDBInterface()
    interface.setCollection(main_paper_with_abstract)

    interface_context = MongoDBInterface()
    interface_context.setCollection(main_paper_with_context)

    interface_citation = MongoDBInterface()
    interface_citation.setCollection(main_paper_with_citation)

    interface_reference = MongoDBInterface()
    interface_reference.setCollection(main_paper_with_reference)

    interface_all_info = MongoDBInterface()
    interface_all_info.setCollection(main_paper_with_all_info)

    other_papers = getAllPaperAbstractInfo({'meta.year':{'$lte':2009, '$gte':2000}})

    for paper in interface.getAllDocuments():
        context = interface_context.getOneDocument({'_id':paper['_id']})
        citation = interface_citation.getOneDocument({'_id':paper['_id']})
        reference = interface_reference.getOneDocument({'_id':paper['_id']})

        assert context is not None
        assert citation is not None
        assert reference is not None

        paper_with_all_info = dict(paper.items() + context.items() + citation.items() + reference.items())

        citing_time_series = []
        for year in xrange(2000, 2010):
            citing_time_series.append([])

        missing_value = 0
        for citing_paper_id in paper_with_all_info['citing_papers']:
            citing_paper = other_papers.get(citing_paper_id, None)
            if citing_paper is None:
                missing_value += 1
                continue
            year = citing_paper['meta']['year']
            citing_time_series[year - 2000].append(citing_paper['_id'])


        citing_time_series_count = []
        for year in xrange(2000, 2010):
            citing_time_series_count.append(len(citing_time_series[year - 2000]))

        paper_with_all_info['citing_paper_time_series'] = citing_time_series
        paper_with_all_info['citing_paper_time_series_count'] = citing_time_series_count
        print '%lf citation is missing' % (missing_value * 1.00 / len(paper_with_all_info['citing_sentences']))

        # pprint(paper_with_all_info)
        interface_all_info.saveDocument(paper_with_all_info)


def process():
    # transfer context data to int
    ci = MongoDBInterface()
    ci.setCollection(main_paper_with_context)
    for doc in ci.getAllDocuments():
        for i in xrange(len(doc['citing_sentences'])):
            doc['citing_sentences'][i][1] = int(doc['citing_sentences'][i][1])
            doc['citing_sentences'][i][2] = int(doc['citing_sentences'][i][2])
        ci.updateDocument(doc)

if __name__ == '__main__':
    mergeAllDataOfMainPaper()