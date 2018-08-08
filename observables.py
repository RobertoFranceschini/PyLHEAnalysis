#should be observable.py
import lorentz, lhef
import numpy as np
import pandas as pd

#def count(obs,event=None,values=None,pidA=1,pidB=-1,statusA=1,statusB=1,flatten=False,return_value=True,default=None,ran=[]):

def make_obs_pair(obs,event=None,values=None,pidA=1,pidB=-1,statusA=1,statusB=1,flatten=False,return_value=True,default=None,ran=[]):
    """
    Compute the observable *obs* write the result in is *mUU_values* from a pair made of one PIDA and one PIDB
    Assumes only one pair in the event exists!

    Args:
        obs: callable
        ran: 4-elements list of random numbers
        values: either a DataFrame to which I add rows. Each row has the structur index, n_event, value, weight for each value in the event calculation or a dictionary

    Returns:
        dictionary(values,weight)
            values: float result of the computation
            weight: weight of the event

    Raises:
        KeyError: Raises an exception.
    """

    weight=event.eventinfo.weight

    lvA=lorentz.LorentzVector() # init four vector
    lvB=lorentz.LorentzVector() # init four vector

    mUU=default
    for p in event.particles: # loop on the particles of each event
        #print(p.id)
        lhef.get_lv(p,destination=lvA,status=statusA,pid=pidA)#,ran[2:4])
        lhef.get_lv(p,destination=lvB,status=statusB,pid=pidB)#,ran[2:4])



    # after loop on particles compute from these fourvectors
    if lorentz.LorentzVector.emptyQ(lvA)==False and lorentz.LorentzVector.emptyQ(lvB) == False:
        #print('not empty')
        if flatten==True:
            lvAB=lvB+lvA
            mUU=obs(lvAB) # obtain the mAB
        else:
            mUU=obs(lvA,lvB) # obtain the deltaEtaAB
        if type(mUU) is np.float64:
            _mUU=[mUU]
            mUU=_mUU
        _result=[ {'values':val, 'weight':weight} for val in mUU ]
        if type(values) is pd.core.frame.DataFrame:
            for res in _result:# append it to the vector of results, including when particles where not found
                values.loc[len(values)]=res
        elif type(values) is list:
            for res in _result:  # append it to the vector of results, including when particles where not found
                values.append(res)
        else:
            print('values contained is not dict nor dataframe, cannot handle it')
            return None
        if return_value==True:
            return _result


def invariant_mass_of2(fv,lv):
    return (fv +  lv).mass()
def delta_eta(fv,lv):
    return np.fabs(fv.eta() -  lv.eta())


def ThetaFromEta(eta):
    return 2.*np.arctan(np.exp(-eta))


def invariant_mass(lv_list):
    _lv = lorentz.LorentzVector()
    for lv in lv_list:
        _lv=lv+_lv
    return _lv.mass()
