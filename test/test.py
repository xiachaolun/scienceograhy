import sys, os
# add the utility library outside
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import numpy as np

# Pyplot is a module within the matplotlib library for plotting
import matplotlib.pyplot as plt
import random

from pprint import pprint

from regressor.feature_extractor import FeatureExtractor


def getTS():
    fe = FeatureExtractor()
    fe._computeCitingPaperTimeSeries()
    all_ts = []
    all_normalized_ts = []
    for id, t in fe.main_paper.items():
        ts = []
        normalized_ts = []
        sum = 0
        for year in xrange(2000, 2010):
            count = len(t['citing_paper_time_series'][year])
            sum += count
            ts.append(count)

        for i in xrange(len(ts)):
            normalized_ts.append(ts[i] * 1.0 / sum)

        all_ts.append(ts)
        all_normalized_ts.append(normalized_ts)

        print ts, normalized_ts

    return all_ts, all_normalized_ts

def plotAllTS(all_ts, name):
    # Create an array of 100 linearly-spaced points from 0 to 2*pi
    years = range(2000, 2010)
    x = range(1, len(years) + 1)

    for ts in all_ts:
        plt.plot(x, ts)

    plt.xticks(x, years)

    # Save the figure in a separate file
    plt.savefig(name)

    # Draw the plot to the screen
    #plt.show()

if __name__ == '__main__':
    all_ts, all_normalized = getTS()
    plotAllTS(all_ts, 'ts.png')