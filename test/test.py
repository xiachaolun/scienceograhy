import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import numpy as np

# Pyplot is a module within the matplotlib library for plotting
import matplotlib.pyplot as plt
import random

from pprint import pprint

from regressor.feature_extractor import FeatureExtractor
from utility.mongodb_interface import MongoDBInterface
from utility.config import test_data

def preprocess():
    fe = FeatureExtractor()
    fe._computeCitingPaperTimeSeries()
    all_data = []
    for id, t in fe.main_paper.items():
        ts = []
        normalized_ts = []
        accumulated_ts = []
        accumulated_normalized_ts = []
        sum = 0
        for year in xrange(2000, 2010):
            count = len(t['citing_paper_time_series'][year])
            sum += count
            accumulated_ts.append(sum)
            ts.append(count)

        for i in xrange(len(ts)):
            normalized_ts.append(ts[i] * 1.0 / sum)
            accumulated_normalized_ts.append(normalized_ts[-1])

        id = t['_id']
        data = {}
        data['_id'] = id
        data['ts'] = ts
        data['normalized_ts'] = normalized_ts
        data['accumulated_ts'] = accumulated_ts
        data['accumulated_normalized_ts'] = accumulated_normalized_ts

        all_data.append(data)

    mi = MongoDBInterface()
    mi.setCollection(test_data)

    for data in all_data:
        mi.updateDocument(data)

def getAllData():
    mi = MongoDBInterface()
    mi.setCollection(test_data)

    all_data = []
    for data in mi.getAllDocuments():
        all_data.append(data)
    return all_data


def plotAllTS(all_data, name):
    plt.cla()
    # Create an array of 100 linearly-spaced points from 0 to 2*pi
    years = range(2000, 2010)
    x = range(1, len(years) + 1)

    for data in all_data:
        sum = 0
        count_sum = 0

        for i in xrange(10):
            count_sum += data['ts'][i]

        for i in xrange(5):
            sum += data['normalized_ts'][i]

        if count_sum > 500:# and (sum > 0.8 or sum < 0.2):
        # if random.randint(0, 200) > -1:
        #     continue
            plt.plot(x, data[name], label=str(data['_id']))
        # print data[name]

    plt.xticks(x, years)
    plt.xlabel('Years')
    plt.ylabel('Citation count' if name == 'ts' else 'Citation count proportion')
    # plt.legend()
    # Save the figure in a separate file
    plt.savefig(name + '.png')

    # Draw the plot to the screen
    #plt.show()

if __name__ == '__main__':
    preprocess()
    all_data = getAllData()
    plotAllTS(all_data, 'ts')
    plotAllTS(all_data, 'normalized_ts')
    #plotAllTS(all_normalized, 'all_normalized.png')