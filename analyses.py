class AnalysisResult(object):
    """

    A class to the results of an analysisself.

    histograms: is HistogramContainerList
    cuts_matrix: np.array

    """

    def __init__(self,histograms,cuts_matrix):
        self.histograms = histograms
        self.cuts_matrix = cuts_matrix
