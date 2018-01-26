from SORAD import SORAD_0
from utils import getTSandLabels, plotTSLabels

if __name__ == '__main__':
    (ts, labels) = getTSandLabels('./4.csv')
    print 'data load done'
    ts = ts[200:400]
    labels = labels[200:400]
    plotTSLabels(ts, labels, png_name='x200-400.png')
    """
    #ts = ts[60000:70000]
    sr = SORAD_0.SORAD(ts, f_ms=0.99, threshold=0.9999999999999, window_size=4)
    results_bool = sr.sorad() # 0.97 - 864
    print 'SORAD done'
    cou = 0
    for i in results_bool:
        if i == 1:
            cou += 1
    print 'total anomaly =',cou
    plotTSLabels(ts, results_bool, png_name='4_40000-60000.png')
    """