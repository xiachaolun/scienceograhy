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
        self._retrieveAllMainAuthor()
        self.k = 3

    def _retrieveAllMainPaper(self):
        mi = MongoDBInterface()
        mi.setCollection(main_paper_list)
        self.main_paper = {}
        for paper in mi.getAllDocuments():
            self.main_paper[paper['_id']] = paper

        mi.setCollection(main_paper_with_citation)
        for paper in mi.getAllDocuments():
            self.main_paper[paper['_id']] = dict(self.main_paper[paper['_id']].items() + paper.items())

        mi.setCollection(main_paper_with_abstract)
        for paper in mi.getAllDocuments():
            self.main_paper[paper['_id']] = dict(self.main_paper[paper['_id']].items() + paper.items())

    def _retrieveAllCitingPaper(self):
       self.all_paper_info = getAllPaperAbstractInfo({'meta.year':{'$lte':2009, '$gte':2000}})

    def _retrieveAllVenue(self):
        self.all_venue_info = getAllVenueInfo()

    def _retrieveAllMainAuthor(self):
        mi = MongoDBInterface()
        mi.setCollection(main_author_list)
        self.authors = {}
        for author in mi.getAllDocuments():
            self.authors[author['_id']] = author


    def _computeCitingPaperTimeSeries(self):
        # get all citing papers of main papers between 2000 and 2009

        for id in self.main_paper.keys():
            paper = self.main_paper[id]

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

    def _getCitingMetaFeature(self):
        self._computeCitingPaperTimeSeries()

        # citation count ts
        features = {}
        for k, paper in self.main_paper.items():
            ts_feature = {}
            sum = 0
            for year in xrange(2000, 2010):
                year_citation_count = len(paper['citing_paper_time_series'][year])
                ts_feature[str(year)]= year_citation_count
                sum += year_citation_count
            ts_feature['sum'] = sum
            features[paper['_id']] = ts_feature

        # citing papers' venue. during first k years,
        # how many citing papers are outside from computer science, and what is the percentage
        tire_1 = {'Journal': 5, 'Conference': 3} # top 70, since we have 3500 conference in CS
        tire_2 = {'Journal': 10, 'Conference': 6}
        for k, paper in self.main_paper.items():
            sum = 0
            outside_cs_count = 0
            inside_cs_count = 0
            tire_1_count = 0
            tire_2_count = 0
            cs_accumulated_ranking_percentile = 0
            non_cs_accumulated_ranking_percentile = 0
            journal_count = 0 # within cs domain
            conference_count = 0
            for year in xrange(2000, 2000 + self.k):
                for citing_id in paper['citing_paper_time_series'][year]:
                    citing_paper = self.all_paper_info[citing_id]
                    venue_id = citing_paper['meta']['venue_id']
                    type = citing_paper['meta']['venue_type']
                    venue = self.all_venue_info.get(venue_id, None)

                    if venue is None:
                        continue

                    if venue['domain'] == 2:
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
                            tire_2_count += 1
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
            cs_average_ranking_percentile = cs_accumulated_ranking_percentile / inside_cs_count
            journal_count_percentage = journal_count / inside_cs_count

            venue_feature = {'_id':paper['_id']}
            venue_feature['outside_cs_percentage'] = outside_cs_percentage
            venue_feature['tire_1_count'] = tire_1_count
            venue_feature['tire_1_percentage'] = tire_1_percentage
            venue_feature['tire_2_count'] = tire_2_count
            venue_feature['tire_2_percentage'] = tire_2_percentage
            venue_feature['cs_average_ranking_percentile'] = cs_average_ranking_percentile
            venue_feature['journal_count_percentage'] = journal_count_percentage
            venue_feature['non_cs_average_ranking_percentile'] = non_cs_average_ranking_percentile

            features[paper['_id']] = dict(features[paper['_id']].items() + venue_feature.items())

        return features

    def _computeAuthorInfo(self):
        for author_id in self.authors.keys():
            author = self.authors[author_id]
            total_publication = 0
            total_citation = 0

            for year, count in author['publication_count_time_series'].items():
                if int(year) <= 1998:
                    total_publication += count
            for year, count in author['citation_count_time_series'].items():
                if int(year) <= 1998:
                    total_citation += count

            # note that this feature should be recomputed because author['total_coauthor_count']
            # contatins the co-authors after 1998
            # total_coauthor = author['total_coauthor_count']
            author['total_publication'] = total_publication
            author['total_citation'] = total_citation
            author['average_citation'] = total_citation * 1.0 / (total_publication + 0.01)

    def _getAuthorFeature(self):
        self._computeAuthorInfo()
        features = {}
        for k, paper in self.main_paper.items():
            max_publication = -1
            max_citation = -1
            max_average_citation = -1
            max_coauthor = -1
            accumulated_publication = 0
            accumulated_citation = 0
            accumulated_average_citation = 0
            accumulated_coauthor = 0

            for author_id in paper['meta']['authors']:
                author = self.authors[author_id]
                accumulated_publication += author['total_publication']
                if author['total_publication'] > max_publication:
                    max_publication = author['total_publication']

                accumulated_citation += author['total_citation']
                if author['total_citation'] > max_citation:
                    max_citation = author['total_citation']

                accumulated_average_citation += author['average_citation']
                if author['average_citation'] > max_average_citation:
                    max_average_citation = author['average_citation']

                accumulated_coauthor += author['total_coauthor_count']
                if author['total_coauthor_count'] > max_coauthor:
                    max_coauthor = author['total_coauthor_count']

            n_author = len(paper['meta']['authors'])

            if n_author > 0:
                average_publication = accumulated_publication * 1.0 / len(paper['meta']['authors'])
                average_citation = accumulated_citation * 1.0 / len(paper['meta']['authors'])
                average_average_citation = accumulated_average_citation * 1.0 / len(paper['meta']['authors'])
                average_coauthor = accumulated_coauthor * 1.0 / len(paper['meta']['authors'])
            else:
                average_publication = 0
                average_citation = 0
                average_average_citation = 0
                average_coauthor = 0

            features[paper['_id']] = {}
            features[paper['_id']]['_id'] = paper['_id']
            features[paper['_id']]['max_publication'] = max_publication
            features[paper['_id']]['max_citation'] = max_citation
            features[paper['_id']]['max_average_citation'] = max_average_citation
            features[paper['_id']]['max_coauthor'] = max_coauthor
            features[paper['_id']]['average_publication'] = average_publication
            features[paper['_id']]['average_citation'] = average_citation
            features[paper['_id']]['average_average_citation'] = average_average_citation
            features[paper['_id']]['average_coauthor'] = average_coauthor

        return features

    def _getPublishingVenueFeature(self):
        features = {}
        for k, paper in self.main_paper.items():
            features[paper['_id']] = {'_id':paper['_id']}
            venue_id = paper['meta']['venue_id']
            if venue_id != -1:
                venue = self.all_venue_info[venue_id]
                # emurate
                venue_type = venue['venue_type']
                venue_ranking_percentile = venue['field_ranking_percentile']
                venue_average_citation = venue['total_citation_count'] * 1.0 / (venue['total_publication'] + 0.01)
            else:
                venue_type = 'Unknown'
                venue_ranking_percentile = 0
                venue_average_citation = 0

            features[paper['_id']]['venue_type'] = venue_type
            features[paper['_id']]['venue_ranking_percentile'] = venue_ranking_percentile
            features[paper['_id']]['venue_average_citation'] = venue_average_citation

        return features

    def extractFeatures(self):
        features = self._getAuthorFeature()

        for id, feature in self._getPublishingVenueFeature().items():
            features[id] = dict(features[id].items() + feature.items())

        for id, feature in self._getCitingMetaFeature().items():
            features[id] = dict(features[id].items() + feature.items())

        return features

    def generateArff(self):
        features = self.extractFeatures()
        featuren_names = features.iteritems().next()

        print featuren_names

if __name__ == '__main__':
    fe = FeatureExtractor()
    fe.generateArff()