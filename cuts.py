import numpy as np
import matplotlib.pyplot as plt
import utils

def cuts_efficiency_picture(cuts_matrix,begin=0,end=None):
    plt.figure(figsize=(60,10))
    _m=np.transpose(cuts_matrix[begin:end])
    cuts_info=utils.np_sort_by_function_of_row(_m,utils.boolstring2binary,row='column')
    cuts_info=utils.np_sort_by_function_of_row(cuts_info[0:-1],np.average)
    plt.imshow( cuts_info )
    plt.colorbar()
    plt.show()


def cuts_single_efficiency(cuts_matrix,begin=0,end=None):
    _m=np.transpose(cuts_matrix[begin:end])
    return list(map(np.average,_m))

def cuts_total_efficiency(cuts_matrix,begin=0,end=None):
    _m=cuts_matrix[begin:end]
    return np.average(np.array(list(map(all,_m))))

def one_step_efficiency(cuts_matrix):
    _m=np.transpose(_c)
    _m_roll=np.roll(_m,-1,axis=0)
    return np.append(np.array([cuts_single_efficiency(_c)[0]]),np.array([ np.average( _m[i][_m[i]>0]*_m_roll[i][_m[i]>0] )  for i in range(len(_m)-1)  ]) )
