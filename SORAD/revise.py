import math
import numpy as np
from scipy import stats
from OEMV import OEMV
from SORAD_0 import SORAD


class SORAD1(SORAD):

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
            
            if flag_ms < 10: # update anyway
                oemv.update(prediction_error)
                self.update_p_theta(prediction_error, X_k)
                flag_ms += 1
            else:
                (mean, sd) = oemv.getMeanSD()
                probility_abnormal = stats.norm(0, sd).cdf(prediction_error)
                probility_abnormal = 2 * probility_abnormal - 1 # the larger the value is, the more abnormal
                # mean = 0, calculate quantile
                z_epsilon = stats.norm(0, sd).ppf((1-self.threshold) / 2.0) # minus !!
                if mean + z_epsilon < prediction_error < mean - z_epsilon or z_epsilon < prediction_error < - z_epsilon: # normal
                    oemv.update(prediction_error)
                    self.update_p_theta(prediction_error, X_k)
                    anomaly_flags[k+1] = probility_abnormal
                else: # abnormal (no updating operation)
                    anomaly_flags[k+1] = probility_abnormal
                    k = k + self.ws            
            # ATTENTION!!!
            k += 1

        return anomaly_flags
