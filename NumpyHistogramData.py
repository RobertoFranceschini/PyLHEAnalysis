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
