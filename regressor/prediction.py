import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *

from data_process.data_provider import getAllPaperAbstractInfo

from pprint import pprint

def getAllMainPaper():
    mi = MongoDBInterface()
    mi.setCollection(main_paper_list)
    res = {}
    for paper in mi.getAllDocuments():
        res[paper['_id']] = paper

    mi.setCollection(main_paper_with_citation)
    for paper in mi.getAllDocuments():
        res[paper['_id']] = dict(res[paper['_id']].items() + paper.items())

    res = [v for k, v in res.items()]
    pprint(res[0])


if __name__ == '__main__':
    print len(getAllPaperAbstractInfo())