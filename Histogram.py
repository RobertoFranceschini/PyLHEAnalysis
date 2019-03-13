import numpy as np
import utils as u

class Histogram(object):
    """
    A class able to hold two lists, one meant to store values of an observables, and another for the uncertainties
    """
    def __init__(self):
        #self.name=name
        self.values=np.array([])
        self.uncertainties=np.array([])


    def ratio(self,h2, uncertainties=None):
        result = Histogram()
        result.values = self.values/h2.values


        if uncertainties==None:
            result.uncertainties = None
        if uncertainties == "Gauss":
            # make the gaussian uncertainty as if the values in the histograms were counts subject to sqrt(count) uncertainty
            result.uncertainties = self.values/h2.values * u.sumQuadrature( [ np.sqrt(h2.values)/h2.values ,  np.sqrt(self.values)/self.values  ]  )
        if uncertainties == "Propagate":
            # use the uncertainty of each Histogram
            result.uncertainties = self.values/h2.values * u.sumQuadrature( [ h2.uncertainties/h2.values ,  self.uncertainties/self.values  ]  )
            # result.uncertainties = self.values/h2.values * np.sqrt( np.power(h2.uncertainties/h2.values,2) + np.power(self.uncertainties/self.values,2) )
        if type(uncertainties) == float:
            if uncertainties > 1:
                # assume this is the number of events in each histogram
                _rescaling2 = uncertainties / np.sum(h2.values)
                _rescaling1 = uncertainties / np.sum(self.values)

                result.uncertainties = self.values/h2.values * u.sumQuadrature( [  np.sqrt(h2.values)/h2.values/np.sqrt(_rescaling2) ,  np.sqrt(self.values)/self.values /np.sqrt(_rescaling1) ]  )

        return result
