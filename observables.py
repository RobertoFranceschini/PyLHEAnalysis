#should be observable.py
import lorentz
import numpy as np

def make_obs_pair(obs,event=event,values=mUU_values,pidA=1,pidB=-1,statusA=1,statusB=1,flatten=False,return_value=True,default=None,ran=[]):
    """
    Compute the observable *obs* write the result in is *mUU_values* from a pair made of one PIDA and one PIDB
    Assumes only one pair in the event exists!

    Args:
        obs: callable
        ran: 4-elements list of random numbers

    Returns:
        float result of the computation

    Raises:
        KeyError: Raises an exception.
    """

    lvA=lorentz.LorentzVector() # init four vector
    lvB=lorentz.LorentzVector() # init four vector

    mUU=default
    for p in event.particles: # loop on the particles of each event
        #print(p.id)
        get_lv(p,destination=lvA,status=statusA,pid=pidA)#,ran[2:4])
        get_lv(p,destination=lvB,status=statusB,pid=pidB)#,ran[2:4])



    # after loop on particles compute from these fourvectors
    if lorentz.LorentzVector.emptyQ(lvA)==False and lorentz.LorentzVector.emptyQ(lvB) == False:
        #print('not empty')
        if flatten==True:
            lvAB=lvB+lvA
            mUU=obs(lvAB) # obtain the mAB
        else:
            mUU=obs(lvA,lvB) # obtain the deltaEtaAB

    values.append(mUU) # append it to the vector of results, including when particles where not found
    if return_value==True:
        return mUU


def invariant_mass(fv,lv):
    return (fv +  lv).mass()
def delta_eta(fv,lv):
    return np.fabs(fv.eta() -  lv.eta())


def ThetaFromEta(eta):
    return 2.*np.arctan(np.exp(-eta))
