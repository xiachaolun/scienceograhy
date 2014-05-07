import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *

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

def process2():
    interface = MongoDBInterface()
    interface.setCollection(all_paper_list)
    cur = interface.getAllDocuments(condition={'total_citation':{'$gte':100},
                                               'year':1999})

    interface2 = MongoDBInterface()
    interface2.setCollection(main_paper_list)

    for doc in cur:
        interface2.saveDocument(doc)

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
    process()