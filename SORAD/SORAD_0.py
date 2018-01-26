# -*- coding:utf-8 -*-
import math
import numpy as np
from numpy.linalg import LinAlgError
from scipy import stats
from OEMV import OEMV


class SORAD(object):
    def __init__(self, time_series, f_rls=0.9, f_ms=0.9, threshold=0.999999, window_size=3):
        """
        time_series: time series data.It is a list
        f_rls: forgetting factor of RLS
        f_ms: forgetting factor of "online estimation of sample mean and standard_deviation"
        threshold: anomaly threshold used in calculating quantile
        window_size: use previous window_size points to predict next point
        """
        self.ts = time_series
        self.f_rls = f_rls
        self.f_ms = f_ms
        self.threshold = threshold
        self.ws = window_size
        (self.__P, self.theta) = self.initialize()

    def initialize(self):
        """ initialize matrix P and theta """
        u0 = np.matrix([1] + [self.ts[self.ws-i-1] for i in xrange(self.ws)])
        u1 = np.matrix([1] + [self.ts[self.ws-i] for i in xrange(self.ws)])
        try:
            P_matrix = np.linalg.inv(u0.T * u0 + self.f_rls * u1.T * u1)
        except LinAlgError:
            print 'exception in P_matrix-initialization'
            P_matrix = np.eye(self.ws + 1)
        
        d0 = np.matrix(self.ts[self.ws])
        d1 = np.matrix(self.ts[self.ws+1])
        Z = u0.T * d0 + self.f_rls * u1.T * d1

        theta = P_matrix * Z

        return (P_matrix, theta)

    def update_p_theta(self, delta, X_k):
        """
        delta: prediction error (float)
        X_k: matrix(Nx1)
        """
        temp = 1.0 / (self.f_rls + (X_k.T * self.__P * X_k).getA()[0][0])
        self.__P = (self.__P - temp * self.__P * X_k * X_k.T * self.__P) / self.f_rls
        self.theta = self.theta + delta * self.__P * X_k

    def sorad(self):
        ts_len = self.ts.__len__()
        anomaly_flags = [0 for _ in xrange(ts_len)]
        oemv = OEMV(self.f_ms)
        flag_ms = 0
        
        k = self.ws + 1
        while k < ts_len - 1:
            X_k = np.matrix([1] + [self.ts[k-i] for i in xrange(self.ws)]).T
            predict_Y = self.theta.T * X_k
            prediction_error = self.ts[k+1] - predict_Y.getA()[0][0] # Y_k+1 = self.ts[k+1]
            if flag_ms < 4: # transient phase: 4 can be substituted by 3,5,6
                # update anyway
                oemv.update(prediction_error)
                self.update_p_theta(prediction_error, X_k)
                flag_ms += 1
            else:
                (mean, sd) = oemv.getMeanSD()
                # mean = 0 calculate quantile
                z_epsilon = stats.norm(0, sd).ppf((1-self.threshold) / 2.0) # minus !!
                if mean + z_epsilon < prediction_error < mean - z_epsilon or z_epsilon < prediction_error < - z_epsilon: # normal
                    oemv.update(prediction_error)
                    self.update_p_theta(prediction_error, X_k)
                else: # abnormal
                    anomaly_flags[k+1] = 1
                    k = k + self.ws
                    # no updating operation 
            k += 1 # ATTENTION!!!

        return anomaly_flags


if __name__ == '__main__':
    pass
