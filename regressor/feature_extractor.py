import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utility.mongodb_interface import MongoDBInterface
from utility.config import *

from data_process.data_provider import getAllPaperAbstractInfo, getAllVenueInfo

from pprint import pprint


class FeatureExtractor(object):
    def __init__(self):
        self._retrieveAllMainPaper()
        self._retrieveAllCitingPaper()
        self._retrieveAllVenue()


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

    def _retrieveAllVenue(self):
        self.all_venue_info = getAllVenueInfo()

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
        self._computeCitingPaperTimeSeries()

        # citation count ts
        paper_features = {}
        for paper in self.main_paper:
            ts_feature = {}
            sum = 0
            for year in xrange(2000, 2010):
                year_citation_count = len(paper['citing_paper_time_series'][year])
                ts_feature[str(year)]= year_citation_count
                sum += year_citation_count
            ts_feature['sum'] = sum
            paper_features[paper['_id']] = ts_feature

        # citing papers' venue. during first k years,
        # how many citing papers are outside from computer science, and what is the percentage
        k = 3
        tire_1 = {'Journal': 5, 'Conference': 3} # top 70, since we have 3500 conference in CS
        tire_2 = {'Journal': 10, 'Conference': 6}
        for paper in self.main_paper:
            sum = 0
            outside_cs_count = 0
            inside_cs_count = 0
            tire_1_count = 0
            tire_2_count = 0
            cs_accumulated_ranking_percentile = 0
            non_cs_accumulated_ranking_percentile = 0
            journal_count = 0 # within cs domain
            conference_count = 0
            for year in xrange(2000, 2000 + k):
                for citing_id in paper['citing_paper_time_series'][year]:
                    citing_paper = self.all_paper_info[citing_id]
                    venue_id = citing_paper['meta']['venue_id']
                    type = citing_paper['meta']['venue_type']
                    venue = self.all_venue_info.get(venue_id, None)

                    #
                    if venue is None:
                        print citing_paper['_id'], venue_id
                        continue

                    if venue['domain'] == 3:
                        # is from cs
                        inside_cs_count += 1
                        if type == 'Journal':
                            journal_count += 1
                        else:
                            conference_count += 1
                        cs_accumulated_ranking_percentile += venue['field_ranking_percentile']
                        if venue['field_ranking_percentile'] <= tire_1[type]:
                            tire_1_count += 1
                        if venue['field_ranking_percentile'] <= tire_2[type]:
                            tire_2_count += 2
                    else:
                        outside_cs_count += 1
                        non_cs_accumulated_ranking_percentile += venue['field_ranking_percentile']
                    sum += 1

            # feature lsit
            # smoothing and make it a real number
            sum += 0.01

            outside_cs_count += 0.01
            outside_cs_percentage = outside_cs_count / sum
            non_cs_average_ranking_percentile = non_cs_accumulated_ranking_percentile / outside_cs_count

            inside_cs_count += 0.01
            tire_1_count = tire_1_count # leave it as a feature
            tire_1_percentage = tire_1_count/ inside_cs_count
            tire_2_count = tire_2_count # leave it as a feature
            tire_2_percentage = tire_2_count / inside_cs_count
            average_ranking_percentile = cs_accumulated_ranking_percentile / inside_cs_count
            journal_count_percentage = journal_count / inside_cs_count

            venue_feature = {}
            venue_feature['outside_cs_percentage'] = outside_cs_percentage
            venue_feature['tire_1_count'] = tire_1_count
            venue_feature['tire_1_percentage'] = tire_1_percentage
            venue_feature['tire_2_count'] = tire_2_count
            venue_feature['tire_2_percentage'] = tire_2_percentage
            venue_feature['average_ranking_percentile'] = average_ranking_percentile
            venue_feature['journal_count_percentage'] = journal_count_percentage
            venue_feature['non_cs_average_ranking_percentile'] = non_cs_average_ranking_percentile

            paper_features[paper['_id']] = dict(paper_features[paper['_id']].items() + venue_feature.items())

        return paper_features

    def extractFeatures(self):
        return self._computeCitingFeature()




if __name__ == '__main__':
    fe = FeatureExtractor()
    features = fe.extractFeatures()
    for id, feature in features:
        pprint(feature)