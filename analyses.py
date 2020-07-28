import pandas as pd
import logging
import time
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
#https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules

class AnalysisResult(object):
    """

    A class to the results of an analysisself.

    histograms: is HistogramContainerList
    cuts_matrix: np.array

    """

    def __init__(self,histograms,cuts_matrix):
        self.histograms = histograms
        self.cuts_matrix = cuts_matrix


def concatenate_results(list_of_jsons=None,columns=None):
    if columns is not None:
        logger.info("Making pd.DataFrame( list_of_jsons[0] ).set_index('event_number')['weight']")
        start_time = time.time()
        _w=pd.DataFrame( list_of_jsons[0] ).set_index('event_number')['weight'] # DataFrame with the Weight
        logger.info("--- %s seconds ---" % (time.time() - start_time))
        ####
        logger.info("Making _p=pd.concat(map(lambda x: pd.DataFrame(x).set_index('event_number')['values'], list_of_jsons ),axis=1, sort=False)")
        start_time = time.time() # THIS THE SLOW PART
        _p=pd.concat(map(lambda x: pd.DataFrame(x).set_index('event_number')['values'], list_of_jsons ),axis=1, sort=False)
        logger.info("--- %s seconds ---" % (time.time() - start_time))
        ####
        _p.columns = columns
        logger.info("Making _p=pd.concat([_p,_w],axis=1, sort=False)")
        start_time = time.time()
        _p=pd.concat([_p,_w],axis=1, sort=False)
        logger.info("--- %s seconds ---" % (time.time() - start_time))
    return _p


def analysis_result_to_pandas(analysis_result=None, names=None):

    _Dexclusive=[analysis_result.histograms.list_of_histograms[name].exclusive for name in names ] #list [list of JSON ]
    #_Dinclusive=[analysis_result.histograms.list_of_histograms[name].inclusive for name in names ]
    _D= _Dexclusive #_Dinclusive #_Dexclusive#+_Dinclusive
    #_names_inclusive = [ nam+'_inclusive' for nam in names ]
    _names = names #+_names_inclusive
    logger.info('Making concatenate_results')
    start_time = time.time()
    _pd_observables=concatenate_results(list_of_jsons=_D,columns=_names)
    logger.info("--- %s seconds ---" % (time.time() - start_time))
    return _pd_observables
