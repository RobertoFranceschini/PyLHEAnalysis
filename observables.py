#should be observable.py
import lorentz, lhef
import numpy as np
import pandas as pd


def compute_obs_estensively(obs,list_of_LHEevents,output=None,operation=None):
    """
    compute an *extensive* observable on a list of four-vectors, e.g. the invariant mass of the compound system made of the sum of all the four-vectors
    the four vectors are those contained in a (filtered) LHE event, each event being an item of the input list list_of_LHEevents

        obs: the observable. Must be a fuction of a LHE event (from which it reads the list of four-vectors)

        list_of_LHEevents: list of LHE events. Each events contains the list of particles on which to compute the observavble

        operation: how to merge the particles contained in each events, e.g. {a,b} , {c,d} |-> {ac,ad,bc,bd}

    """
    if (output is not None) and (operation is not None):
        mixed_events  = operation(list_of_LHEevents)
        computed_obs_values = [ obs(ev.particles) for ev in mixed_events ]
        try:
            weight=mixed_events[0].eventinfo.weight
        except IndexError:
            pass
        [ output.append( {'values':val, 'weight':weight}  ) for val in computed_obs_values ]


def values_of(Mmumu):
    return pd.DataFrame(Mmumu)['values']
def weights_of(Mmumu):
    return pd.DataFrame(Mmumu)['weight']
def v(x):
    return values_of(x)
def w(x):
    return weights_of(x)



def invariant_mass_of2(fv,lv):
    return (fv +  lv).mass()
def delta_eta(fv,lv):
    return np.fabs(fv.eta() -  lv.eta())


def ThetaFromEta(eta):
    return 2.*np.arctan(np.exp(-eta))

################################################################################
################################################################################
######################## FUCNTIONS OF LHE EVENTS ###############################
################################################################################
################################################################################
################################################################################

def theta(lhe_event):
    _lv = lorentz.LorentzVector()
    for lv in lhe_event:
        _lv=lv.fourvector()+_lv
    return _lv.theta()

def perp(lhe_event):
    _lv = lorentz.LorentzVector()
    for lv in lhe_event:
        _lv=lv.fourvector()+_lv
    return _lv.perp()

def invariant_mass(lhe_event):
    _lv = lorentz.LorentzVector()
    for lv in lhe_event:
        _lv=lv.fourvector()+_lv
    return _lv.mass()

def s_min(lhe_ev_vis,lhe_ev_inv):
    """
        lhe_ev_vis: is a LHE subevent containing all the particles to be considered as visible
        lhe_ev_inv: is a LHE subevent containing the one particle for the missing momentum
        in principle this observable depend on an external parameter, the mass of the invisible system
        this is for now fixed at zero and can be made an optional argument. in that case a dictionary input needs to be implemented in compute_obs_estensively
    """

    SumMinv = 0
    vis_sys=lorentz.LorentzVector()
    for vis in lhe_ev_vis.particles:
        vis_sys=vis_sys+vis.fourvector()

    return np.sqrt( (vis_sys.energy())**2 - (vis_sys.pz)**2 ) + np.sqrt( (lhe_ev_inv.perp())**2 + (SumMinv)**2 )



################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

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
