class HistogramContainer(object):
    """
    A class able to hold two lists, one meant to store values of an inclusive observables (no cuts), and another for the values that pass some cuts.
    Typical use is to contain the spectrum of a variable on which a cut is made, so that the two lists will show the effect of the cut.
    """
    def __init__(self,name):
        self.name=name
        self.inclusive=[]
        self.exclusive=[]


class HistogramContainerList(object):
    """

    A class to hold several histograms at once, usually to have thme passed as return value in an analysis

    list_of_histograms: dictionary of the several histogram contained

    """

    def __init__(self,names):
        self.names = names

        histogram_container_list={}
        for name in names:
            _h = HistogramContainer(name)
            histogram_container_list[name]=(_h)

        self.list_of_histograms=histogram_container_list
