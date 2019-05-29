import numpy as np
import utils as u
import NumpyClasses

class Histogram(NumpyClasses.Numpy1DHistogramData):
    """
    A class able to hold two lists, one meant to store values of an observables, and another for the uncertainties
    """
    def __init__(self,counts=[],bins=[],uncertainties=[],tup=None, super=None):
        #self.name=name

        if tup != None:
            super().__init__(tup)
        if super !=None:
            self.counts=super.counts
            self.bins=super.bins
        else:
            self.counts=np.array(counts)
            self.bins=np.array(bins) # same as numpy histogram bins output
            self.uncertainties=np.array(uncertainties)


    def ratio(self,h2, uncertainties=None):
        result = Histogram()
        result.counts = self.counts/h2.counts


        if uncertainties==None:
            result.uncertainties = None
        if uncertainties == "Gauss":
            # make the gaussian uncertainty as if the values in the histograms were counts subject to sqrt(count) uncertainty
            result.uncertainties = self.counts/h2.counts * u.sumQuadrature( [ np.sqrt(h2.counts)/h2.counts ,  np.sqrt(self.counts)/self.counts  ]  )
        if uncertainties == "Propagate":
            # use the uncertainty of each Histogram
            result.uncertainties = self.counts/h2.counts * u.sumQuadrature( [ h2.uncertainties/h2.counts ,  self.uncertainties/self.counts  ]  )
            # result.uncertainties = self.counts/h2.counts * np.sqrt( np.power(h2.uncertainties/h2.counts,2) + np.power(self.uncertainties/self.counts,2) )
        if type(uncertainties) == float:
            if uncertainties > 1:
                # assume this is the number of events in each histogram
                _rescaling2 = uncertainties / np.sum(h2.counts)
                _rescaling1 = uncertainties / np.sum(self.counts)

                result.uncertainties = self.counts/h2.counts * u.sumQuadrature( [  np.sqrt(h2.counts)/h2.counts/np.sqrt(_rescaling2) ,  np.sqrt(self.counts)/self.counts /np.sqrt(_rescaling1) ]  )

        return result
