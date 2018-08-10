import numpy as np
import matplotlib as plt
import utils

def cuts_efficiency_picture(cuts_matrix,begin=0,end=-1):
    plt.figure(figsize=(60,10))
    _m=np.transpose(cuts_matrix[begin:end])
    cuts_info=utils.np_sort_by_function_of_row(_m,utils.boolstring2binary,row='column')
    cuts_info=utils.np_sort_by_function_of_row(cuts_info[0:-1],np.average)
    plt.imshow( cuts_info )
    plt.colorbar()
    plt.show()
