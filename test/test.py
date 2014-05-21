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
    for id, t in fe.main_paper.items():
        ts = []
        for year in xrange(2000, 2010):
            ts.append(len(t['citing_paper_time_series'][year]))
        all_ts.append(ts)
        print ts
    return all_ts

def plotAllTS():
    # Create an array of 100 linearly-spaced points from 0 to 2*pi
    years = range(2000, 2010)
    x = range(1, len(years) + 1)

    for k in xrange(10):
        y = [random.randint(0, 100) for i in x]
        plt.plot(x, y)

    plt.xticks(x, years)

    # Save the figure in a separate file
    plt.savefig('sine_function_plain.png')

    # Draw the plot to the screen
    plt.show()

if __name__ == '__main__':
    getTS()