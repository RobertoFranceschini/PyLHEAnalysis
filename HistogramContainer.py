class HistogramContainer(object):
    """
    A class able to hold two lists, one meant to store values of an inclusive observables (no cuts), and another for the values that pass some cuts.
    Typical use is to contain the spectrum of a variable on which a cut is made, so that the two lists will show the effect of the cut. 
    """
    def __init__(self):
        self.inclusive=[]
        self.exclusive=[]
