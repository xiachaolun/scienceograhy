import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import paper_list_collection, main_paper_with_context

def process():
    interface = MongoDBInterface()
    interface.setCollection(paper_list_collection)
    cur = interface.getAllDocuments()
    for doc in cur:
        id = str(doc['_id'])
        if 'Publication' in id:
            id = id.split('/')[2].strip()
            interface._deleteDocument(condition={'_id':doc['_id']})

        doc['_id'] = int(id)
        interface.saveDocument(doc)

def process2():
    interface = MongoDBInterface()
    interface.setCollection(paper_list_collection)
    cur = interface.getAllDocuments(condition={'total_citation':{'$gte':100},
                                               'year':{'$gte':1998, '$lte':2003}})

    interface2 = MongoDBInterface()
    interface2.setCollection(main_paper_with_context)

    for doc in cur:
        interface2.saveDocument(doc)

if __name__ == '__main__':
    process2()