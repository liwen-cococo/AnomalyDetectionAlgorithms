import csv
import matplotlib.pyplot as plt

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
                c.append('1')
    plt.plot(t, v)
    ax = plt.gca()
    for x, y, an in zip(t, v, c):
        ax.text(x, y, an, color='r', fontsize=12)
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
                c.append('1')
    plt.plot(t, v)
    ax = plt.gca()
    for x, y, an in zip(t, v, c):
        ax.text(x, y, an, color='r', fontsize=12)
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