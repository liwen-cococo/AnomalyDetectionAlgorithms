import csv
import matplotlib.pyplot as plt
from SORAD_0 import SORAD
# from helper import plt_predicted, plt_time_series, getData


def plt_time_series(file_path):
    csv_reader = csv.reader(open(file_path, 'r'))
    t, v, c = [], [], []
    for (i, row) in enumerate(csv_reader, 0):
        if i > 0:
            t.append(i)
            v.append(float(row[1]))
            if row[2] == '0':
                c.append('')
            else:
                c.append('.')
    plt.plot(t, v)
    ax = plt.gca()
    for x, y, an in zip(t, v, c):
        ax.text(x, y, an, color='r', fontsize=40)
    plt.show()

def plt_predicted(file_path, results):
    csv_reader = csv.reader(open(file_path, 'r'))
    t, v, c = [], [], []
    k = 0
    for (i, row) in enumerate(csv_reader, 0):
        if i > 0:
            t.append(i)
            v.append(float(row[1]))
            if results[i-1] == 0:
                c.append('')
            else:
                c.append('.')
    plt.plot(t, v)
    ax = plt.gca()
    for x, y, an in zip(t, v, c):
        ax.text(x, y, an, color='r', fontsize=40)
    plt.savefig(file_path[-6:] + '.png')
    plt.show()

def getData(file_path):
    data = csv.reader(open(file_path, 'r'))
    values, labels = [], []
    i = 0
    for row in data:
        if i==1:
            values.append(float(row[1]))
            labels.append(int(row[2]))
        else:
            i = 1
    return (values, labels)


if __name__ == '__main__':
    file_path = 'real_4.csv'
    (v,l) = getData(file_path)
    
    print '\npredicted'
    x = SORAD(v, f_rls=0.9, f_ms=0.9, window_size=4)
    result = x.sorad()
    counter = 0
    for i in xrange(result.__len__()):
        if result[i] > 0.9999:
            result[i] = 1
            print i,
            counter += 1
        else:
            result[i] = 0

    print '\nreal abnormaly:'
    for i in xrange(l.__len__()):
        if l[i] == 1:
            print i,
    
    #plt_time_series(file_path)
    #plt.clf()
    plt_predicted(file_path, result)
