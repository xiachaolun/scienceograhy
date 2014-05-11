import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *

from data_process.data_provider import getAllPaperAbstractInfo

from pprint import pprint


class FeatureExtractor(object):
    def __init__(self):
        self._retrieveAllMainPaper()
        self._retrieveAllCitingPaper()


    def _retrieveAllMainPaper(self):
        mi = MongoDBInterface()
        mi.setCollection(main_paper_list)
        res = {}
        for paper in mi.getAllDocuments():
            res[paper['_id']] = paper

        mi.setCollection(main_paper_with_citation)
        for paper in mi.getAllDocuments():
            res[paper['_id']] = dict(res[paper['_id']].items() + paper.items())

        self.main_paper = [v for k, v in res.items()]

    def _retrieveAllCitingPaper(self):
       self.all_paper_info = getAllPaperAbstractInfo({'meta.year':{'$lte':2009, '$gte':2000}})

    def _computeCitingPaperTimeSeries(self):
        # get all citing papers of main papers between 2000 and 2009

        for i in xrange(len(self.main_paper)):
            paper = self.main_paper[i]
            # print paper['_id']

            citing_time_series = {}
            for year in xrange(2000, 2010):
                citing_time_series[year] = []

            for citing_paper_id in paper['citing_papers']:
                citing_paper = self.all_paper_info.get(citing_paper_id, None)
                if citing_paper is None:
                    continue
                year = citing_paper['meta']['year']
                citing_time_series[year].append(citing_paper['_id'])

            paper['citing_paper_time_series'] = citing_time_series

    def _computeCitingFeature(self):

        paper_features = {}
        for paper in self.main_paper:
            ts = []
            paper = paper_features[paper['_id']]
            sum = 0
            for year in xrange(2000, 2010):
                year_citation_count = len(paper['citing_paper_time_series'][year])
                ts.append(year_citation_count)
                sum += year_citation_count
            ts.append(sum)
            paper_features[paper['_id']] = ts

        return paper_features

    def extractFeatures(self):
        return self._computeCitingFeature()




if __name__ == '__main__':
    fe = FeatureExtractor()
    print fe.extractFeatures()