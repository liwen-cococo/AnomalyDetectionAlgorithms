import matplotlib.pyplot as plt
from revise import SORAD1
from helper import plt_predicted, plt_time_series, getData


if __name__ == '__main__':
    file_path = 'real_4.csv'
    (v,l) = getData(file_path)
    
    print '\npredicted'
    x = SORAD1(v, f_rls=0.9, f_ms=0.9, window_size=4)
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
