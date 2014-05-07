import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *
from utility.tool import prepcessCitingSentence, nearlySameText
from single_paper import crawlSinglePaper

from pprint import pprint

import time
import random

def findAllPaperID():
    interface = MongoDBInterface()
    interface.setCollection(main_paper_with_citation)
    cur = interface.getAllDocuments()
    all_papers = set()
    all_papers.add(2289659)
    for doc in cur:
        for id in doc['citing_papers']:
            all_papers.add(id)

    return all_papers

def crawlerAllPaper():
    ids = findAllPaperID()

    interface = MongoDBInterface()
    interface.setCollection(other_paper_with_abstract)

    id_list = [id for id in ids]

    random.shuffle(id_list)
    for id in id_list:
        if interface.getOneDocument({'_id':id}) is not None:
            continue
        doc = {}
        doc['_id'] = id
        doc['meta'] = crawlSinglePaper(id)
        interface.saveDocument(doc)
        time.sleep(random.randint(0, 100) % 2 + 1)

if __name__ == '__main__':
    crawlerAllPaper()
