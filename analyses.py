import pandas as pd

def concatenate_results(list_of_jsons=None,columns=None):
    if columns is not None:
        _w=pd.DataFrame( list_of_jsons[0] ).set_index('event_number')['weight']
        _p=pd.concat(map(lambda x: pd.DataFrame(x).set_index('event_number')['values'], list_of_jsons ),axis=1, sort=False)
        _p.columns = columns
        _p=pd.concat([_p,_w],axis=1, sort=False)
    return _p


class AnalysisResult(object):
    """

    A class to the results of an analysisself.

    histograms: is HistogramContainerList
    cuts_matrix: np.array

    """

    def __init__(self,histograms,cuts_matrix):
        self.histograms = histograms
        self.cuts_matrix = cuts_matrix



def analysis_result_to_pandas(analysis_result=None, names=None):
    _Dexclusive=[analysis_result.histograms.list_of_histograms[name].exclusive for name in names ]
    _Dinclusive=[analysis_result.histograms.list_of_histograms[name].inclusive for name in names ]
    _D=_Dexclusive+_Dinclusive
    _names_inclusive = [ nam+'_inclusive' for nam in names ]
    _names = names +_names_inclusive
    _pd_observables=concatenate_results(_D,columns=_names)
    return _pd_observables
