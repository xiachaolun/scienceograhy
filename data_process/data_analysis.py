import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *


def analysis1():
    context_interface = MongoDBInterface()
    context_interface.setCollection(main_paper_with_context)

    citing_interface = MongoDBInterface()
    citing_interface.setCollection(main_paper_with_citation)

    for paper in citing_interface.getAllDocuments():
        context = context_interface.getOneDocument({'_id':paper['_id']})
        assert context is not None
        citation_cnt = len(paper['citing_papers'])
        context_cnt = len(context['citing_sentences'])
        print float(context_cnt) / citation_cnt

if __name__ == '__main__':
    analysis1()