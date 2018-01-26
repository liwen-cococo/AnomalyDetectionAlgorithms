import csv
import matplotlib.pyplot as plt

def getTSandLabels(file_path):
    """ 
    Input:  file_path 
    Output: TS(list), labels(list)
    """
    content = csv.reader(open(file_path, 'r'))
    TS, Labels = [], []
    for c in content:
        TS.append(float(c[2]))
        Labels.append(int(c[3]))
    return (TS, Labels)


def plotTSLabels(ts, labels, png_name):
    t = range(len(ts))
    c = []
    for l in labels:
        if l == 0:
            c.append('')
        else:
            c.append('1')
    plt.plot(t, ts)
    ax = plt.gca()
    for x, y, node in zip(t, ts, c):
        ax.text(x, y, node, color='r', fontsize=12)
    plt.savefig(png_name)
    #plt.show()

if __name__ == '__main__':
    (ts, labels) = getTSandLabels('./1_02e99bd4f6cfb33f_train.csv')
    print 'data load done'
    plotTSLabels(ts[:10000], labels[:10000])
    
