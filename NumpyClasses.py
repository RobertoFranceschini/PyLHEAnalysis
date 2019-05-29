"""
Classes having the purpose to
1) contain in object the tuples that numpy functions return
2) manipulate the numpy outputs in a way that accomplishes standard tasks, e.g. setting a 1D limit on a signal strenght
"""

import numpy as np
import utils as u
import matplotlib.pyplot as plt

##############################################
def gotLabels(histos):
    ##############################################
    if any([ h.label != "" for h in histos.histograms ]  ):
        return True
    return False


##############################################
def gotUncertainties(h):
    ##############################################
    result = np.all(h.uncertainties != np.array(None))
    #print('tried:',result)
    return result

##############################################
def histoPlot(h,fmt='.',lighter_error=0.75,ax=None,label="",**kwargs):
    ##############################################
    """
    example usage to plot on the same figure
    ax = histoPlot(histosRatios.histograms[1],fmt=',')
    histoPlot(histosRatios.histograms[0],lighter_error=1,fmt='.',ax=ax)

    This function assumes that the label of the histogram is stored in the histogram.label member. This can be superseeded by the label option
    """
    if ax is None:
        ax = plt.axes()
        # to keep plotting on the same axes
        # https://stackoverflow.com/questions/55186273/warning-adding-an-axes-using-the-same-arguments-and-custom-plot-function

    # Get the current color in the cycle     #https://stackoverflow.com/questions/28779559/how-to-set-same-color-for-markers-and-lines-in-a-matplotlib-plot-loop
    color = next(ax._get_lines.prop_cycler)['color']

    if gotUncertainties(h):
        # plot the error bar https://matplotlib.org/gallery/statistics/errorbar_features.html?highlight=error%20plot
        ax.errorbar(u.midpoints(h.bins), h.counts, yerr=h.uncertainties,color = u.lighten_color(color,lighter_error),fmt=fmt )

    _label = h.label
    # plot the histogram
    if label != "":
        _label = label
    ax.step(h.bins,np.append(h.counts,h.counts[-1:]),where='post',color=color,label=_label,**kwargs)
    return ax

##############################################
def make_label(labels,h,histos):
    ##############################################
    if labels == None:
        return histos.histograms[h].label
    else:
        try:
            return labels[h]
        except IndexError:
            return ""
        except TypeError:
            return ""

##############################################
def histoPlots( histos , labels=None,subset=None, **kwargs):
    ##############################################
    """
    Either labels are provided, or labels fro the histogram will be used. Either all the optional input or all the labels stored in the histogram can be used, not a mixed set.
    """
    ax=plt.axes()

    if subset == None:
        subset = range(len(histos.histograms))

    [ histoPlot(histos.histograms[h],label=make_label(labels,h,histos),ax=ax,**kwargs) for h in subset  ]
    if labels != None or gotLabels(histos):
        ax.legend(bbox_to_anchor=[1,1])

    return ax

class Numpy1DHistogramsData(object):
    """
    A class able to hold a number of Numpy1DHistogramData (single histograms).
    The histograms are stored in the member "histograms" as a list of histograms, each of which carries its own bins and counts
    It handles the output of plots and histograms from NumPy and Matplotlib, so it has an optional argument tup.
    Can also be created as an array of histograms, originated each independently.
    """
    def __init__(self, tup=None):
        #for each count vector in counts make a Numpy1DHistogramData

        def make_subtuple(tup, el):
            try:
                res = tup[0][el], tup[1], tup[2]
            except IndexError:
                res = tup[0][el], tup[1]

            return res

        self.histograms = []
        if tup != None:
            self.histograms = [ Numpy1DHistogramData( tup = make_subtuple(tup, el) ) for el in range( len(tup[0]) ) ]

    def ratio(self,wrt=0,uncertainties=None):
        # default is to make the ratio of component-1 over component-0
        # if more than 2 histograms are present the result is the ratio component-I over component-0
        result = Numpy1DHistogramsData()
        hDenominator=self.histograms[wrt]
        result.histograms = [ hNumerator.ratio(hDenominator,uncertainties=uncertainties) for hNumerator in self.histograms ]
        return result



class Numpy1DHistogramData(object):
    """
    A class able to hold two in its objects the resutl of histograms, e.g.
    counts , binedges  from a 1D histogram
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html?highlight=histogram#numpy.histogram
    """
    # def __init__(self,tup):
    #     self.counts=tup[0]
    #     self.bins=tup[1]
    #     try:
    #         self.patches=tup[2]
    #     except IndexError:
    #         pass

    def __init__(self,counts=None,bins=None,uncertainties=None,label="",tup=None):
        # the uncertaintis member is filled in all cases
        # the counts and bins can be valorized with ther the named optional parameters or from the histogram tuple output
        self.uncertainties=np.array(uncertainties)
        self.label=label
        if tup != None:
            self.counts=tup[0]
            self.bins=tup[1]
            try:
                self.patches=tup[2]
            except IndexError:
                pass
        else:
            self.counts=np.array(counts)
            self.bins=np.array(bins) # same as numpy histogram bins output


    def ratio(self,h2, uncertainties=None):
        result = Numpy1DHistogramData() # an empty histogram, with None counts, bin edges, and uncertainties
        result.counts = self.counts/h2.counts
        result.label=self.label+" over "+h2.label
        if  all(self.bins==h2.bins):
            result.bins = self.bins
        else:
            print('bins did not match!','\n',self.bins==h2.bins,'\n',self.bins==h2.bins)

        if uncertainties==None:
            result.uncertainties = None # keep None as uncertainties
        if uncertainties == "Gauss":
            # make the gaussian uncertainty as if the values in the histograms were counts subject to sqrt(count) uncertainty
            result.uncertainties = self.counts/h2.counts * u.sumQuadrature( [ np.sqrt(h2.counts)/h2.counts ,  np.sqrt(self.counts)/self.counts  ]  )
        if uncertainties == "Propagate":
            # use the uncertainty of each Histogram
            result.uncertainties = self.counts/h2.counts * u.sumQuadrature( [ h2.uncertainties/h2.counts ,  self.uncertainties/self.counts  ]  )
            # result.uncertainties = self.counts/h2.counts * np.sqrt( np.power(h2.uncertainties/h2.counts,2) + np.power(self.uncertainties/self.counts,2) )
        if type(uncertainties) == float or type(uncertainties) == int:
            if uncertainties > 1:
                # assume this is the number of events in each histogram
                _rescaling2 = uncertainties / np.sum(h2.counts)
                _rescaling1 = uncertainties / np.sum(self.counts)

                result.uncertainties = self.counts/h2.counts * u.sumQuadrature( [  np.sqrt(h2.counts)/h2.counts/np.sqrt(_rescaling2) ,  np.sqrt(self.counts)/self.counts /np.sqrt(_rescaling1) ]  )

        return result




class Numpy2DHistogramData(object):
    """
    A class able to hold two in its objects the resutl of histograms, e.g.
    counts , xedges , yedges , image
    from a 2D histogram done y matplotlib
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist2d.html
    """
    def __init__(self,tup):
        self.counts=tup[0]
        self.xedges=tup[1]
        self.yedges=tup[2]
        try:
            self.image=tup[3]
        except IndexError:
            pass


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


class generic(object):
    def __init__(self):
        pass
