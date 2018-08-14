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
    _D=[analysis_result.histograms.list_of_histograms[name].exclusive for name in names ]
    _pd_observables=observables.concatenate_results(_D,columns=names)
    return _pd_observables
