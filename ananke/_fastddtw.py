### derivative dynamic time warping implementation of fastdtw
### this implementation is based on fastdtw (https://github.com/slaypni/fastdtw)

import numpy as np
import numpy
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

import matplotlib
import matplotlib.pyplot as plt

def est_derivatives(sig):
    '''
    Computing drivative differences between dx and dy
    Arguments:
           sig -- signal, numpy array of shape ( n,  )
    Result:
         d_sig -- estimated derivatives of input signal, numpy array of shape ( n-2,  )
    '''
    assert len(sig) >= 3, '''The length of your signal should be 
                           greater than 3 to implement DDTW.'''
    if type(sig) != numpy.ndarray :
        sig = np.array(sig)
    d_0 = sig[:-2]
    d_1 = sig[1:-1]
    d_2 = sig[2:]
    d_sig = ((d_1 - d_0) + (d_2 - d_0)/2)/2
    return d_sig    

def fast_ddtw(signal_1, signal_2):
    '''
    Arguments:
        signal_1 -- first time series, numpy array of shape ( n1,  )
        signal_2 -- second time series, numpy array of shape ( n2,  )
    Results:
        distance -- distance between two input time series
            path -- aligned indices, list of indices
    ''' 
    d_sig1 = est_derivatives(signal_1)
    d_sig2 = est_derivatives(signal_2)
    distance, path = fastdtw(d_sig1, d_sig2, dist=euclidean)
    return distance, path

def plot_raw_signals(signal_1, signal_2, title = 'raw_signals'):
    '''
    Arguments:
        signal_1 -- first time series, numpy array of shape ( n1,  )
        signal_2 -- second time series, numpy array of shape ( n2,  )
    Results:
          Figure 
    ''' 
    plt.plot(signal_1)
    plt.plot(signal_2)
    plt.grid()
    plt.title(title)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.show()

def plot_alignment_path(path, title = 'alignment_path'):
    '''
    Arguments:
          path -- aligned indices, list of indices
    Results:
        Figure
    '''
    plt.plot([index_pair[0] for index_pair in path], [index_pair[1] for index_pair in path])
    plt.grid()
    plt.title(title)
    plt.xlabel('signal 1')
    plt.ylabel('signal 2')
    plt.show()
    
def plot_aligned_signals(signal_1, signal_2, path, title = 'aligned_signals'):
    '''
    Arguments:
        signal_1 -- first time series, numpy array of shape ( n1,  )
        signal_2 -- second time series, numpy array of shape ( n2,  )
            path -- aligned indices, list of indices
    Results:
          Figure 
    ''' 
    plt.plot([signal_1[index_pair[0]] for index_pair in path])
    plt.plot([signal_2[index_pair[1]] for index_pair in path])
    plt.grid()
    plt.title(title)
    plt.xlabel('time')
    plt.ylabel('value')
    plt.show()