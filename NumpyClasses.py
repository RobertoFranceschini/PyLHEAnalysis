"""
Classes having the purpose to
1) contain in object the tuples that numpy functions return
2) manipulate the numpy outputs in a way that accomplishes standard tasks, e.g. setting a 1D limit on a signal strenght
"""

class Numpy2DHistogramData(object):
    """
    A class able to hold two in its objects the resutl of histograms, e.g.
    counts , xedges , yedges , image
    from a 2D histogram
    """
    def __init__(self,tup):
        self.counts=tup[0]
        self.xedges=tup[1]
        self.yedges=tup[2]
        self.image=tup[3]

class SignalStrengthData(object):
    """
    A class able to hold the results of searches for maximal signal strenght, both with numerical fast methods and approximate symbolic ones
    """
    def __init__(self, **kwargs):
        self.mu_max=None
        self.mu_of_deltachisqaure_interp = None
        self.deltachisquare_of_mu_interp=None
        self.deltachisquare_of_mu_exact=None
        self.deltachisquare_of_mu_approx=None
