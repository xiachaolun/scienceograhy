from pyquery import PyQuery as pq
import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import main_paper_with_context
from utility.tool import prepcessCitingSentence, nearlySameText
from pprint import pprint

import time
import random

def crawlAuthor(author_id):
    author_id = int(author_id)
    url = 'http://academic.research.microsoft.com/Author/%d/' % author_id
    html = pq(url)
    print html

if __name__ == '__main__':
    crawlAuthor(594572)