import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt
from SORAD.SORAD_0 import SORAD
FILE_PATH = 'train.csv'


def getSingleTS(content, kpiID):
    time_series, labels = [], []

    for c in content:
        if c[0] == kpiID:
            time_series.append(c[2])
            labels.append(c[3])

    return (time_series, labels)

def plot_1(values, predicted):
    len = values.__len__()
    plt.plot(range(len), values)
    c = []
    for i in xrange(len):
        if predicted[i] == '0':
            c.append()
        else:
            c.append('1')
    ax = plt.gca()
    for x, y, an in zip(range(len), values, c):
        ax.text(x, y, an, color='r', fontsize=12)
    plt.show()
    

if __name__ == '__main__':
    # get time series data
    content = pd.read_csv(FILE_PATH).values
    (time_series, labels) = getSingleTS(content, '40e25005ff8992bd')

    # analyse this time series
    analysis = SORAD(time_series)
    predict_results = analysis.sorad()
    for i, pr in enumerate(predict_results):
        if pr == 1:
            print i,
    print ''
    plot_1(time_series[:1400], predict_results[:1400])
    plt.clf()
