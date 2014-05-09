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

    all_paper_info = getAllPaperAbstractInfo()

    for paper in res:
        citing_time_series = {}
        for year in xrange(2000, 2010):
            citing_time_series[year] = []

        for citing_paper_id in paper['citing_papers']:
            citing_paper = all_paper_info[citing_paper_id]
            year = citing_paper['meta']['year']
            citing_time_series[year].append(citing_paper['_id'])

        paper['citing_paper_time_series'] = citing_time_series
        pprint(paper)
        break




if __name__ == '__main__':
    #print len(getAllPaperAbstractInfo())
    getAllMainPaper()