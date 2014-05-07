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

def checkData():

    interface = MongoDBInterface()
    interface.setCollection(other_paper_with_abstract)

    cur = interface.getAllDocuments()
    print cur.count()
    for doc in interface.getAllDocuments():
        assert 'meta' in doc.keys()

if __name__ == '__main__':
    checkData()
