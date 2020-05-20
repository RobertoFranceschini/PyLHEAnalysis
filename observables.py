import lorentz, lhef
import numpy as np
import pandas as pd
import utils
import HistogramContainer



def compute_obs_estensively(obs,list_of_LHEevents,output=None,operation=None,return_value=False,check_value=None):
    """
    compute an *extensive* observable on a list of four-vectors, e.g. the invariant mass of the compound system made of the sum of all the four-vectors
    the four vectors are those contained in a (filtered) LHE event, each event being an item of the input list list_of_LHEevents

        obs: the observable. Must be a fuction of a LHE event (from which it reads the list of four-vectors)

        list_of_LHEevents: list of LHE events. Each events contains the list of particles on which to compute the observavble
             they must contain accessory information such as the weight

        operation: how to merge the particles contained in each events, e.g. {a,b} , {c,d} |-> {ac,ad,bc,bd}

        check_value: is a dictionary e.g. {'relation':bt,'threshold':[2,3],which:any} with the type of check and the threshold to be used to which I add a new property for the current value and pass it to a tester that uses a dict variable input. example it must contain relation and threshold

    """

    DEBUG=False

    #if len(list_of_LHEevents) > 0:
    if (output is not None) and (operation is not None):
        if DEBUG: print('~~~~~~~~~~~~~~~~~~')
        if DEBUG: print('computing',str(obs))
        if DEBUG: print('lenght of list of sub-events', len(list_of_LHEevents))
        if DEBUG:
            for _ev in list_of_LHEevents:
                _ev.print_event()

        mixed_events  = operation(list_of_LHEevents)
        if mixed_events is not None: # if it is none it means the necessay particles were not found
            if DEBUG: print('mixed events', mixed_events, 'under ',str(operation))
            computed_obs_values = [ obs(ev.particles) for ev in mixed_events ]
            #try:
            weight=mixed_events[0].eventinfo.weight # it is not a "try" becasue it must be there. weight is a standard attribute of LHE events
            #except IndexError:
            #    if DEBUG: print('weight not found!')
            #    #_result = [  {'values':np.nan, 'weight':weight, 'event_number':_nev, 'sample_label':_label }  for val in computed_obs_values ]
            #    pass
            try: # it is a try because this attribute is not standard of LHE and needs to be set in the analysis
                _nev=mixed_events[0].eventinfo.event_number
            except IndexError:
                print('empty set of LHEevents')
                _nev='event_number'
                pass
            except AttributeError:
                print('missing attribute eventinfo.event_number')
                _nev='event_number'
                pass
            try: # it is a try because this attribute is not standard of LHE and needs to be set in the analysis
                _label=mixed_events[0].eventinfo.sample_label
            except IndexError:
                print('empty set of LHEevents')
                _label='sample_label'
                pass
            except AttributeError:
                print('missing attribute eventinfo.sample_label')
                _label='sample_label'
                pass
            #[ output.append( {'values':val, 'weight':weight}  ) for val in computed_obs_values ]
            #_result = [  {'values':val, 'weight':weight, 'event_number':_nev, 'sample_label':_label }  for val in computed_obs_values ]
            _result = [ {**{'values':val, 'weight':weight, 'event_number':_nev, 'sample_label':_label }, **_label}  for val in computed_obs_values ]
             # merged_dict = {**dict1, **dict2}

            if DEBUG: print(_result)
        else: #mixed events was None, weight set to zero
            if DEBUG: print('result should be NaN')
            _result = [  {'values':np.nan, 'weight':0} ] #, 'weight':weight, 'event_number':_nev, 'sample_label':_label } ]
            # np.nan gives always False when comapred to a number , all checks will fail
        if type(output) is pd.core.frame.DataFrame:
            for res in _result:# append it to the vector of results, including when particles where not found
                output.loc[len(output)]=res
        elif type(output) is list:
            for res in _result:  # append it to the vector of results, including when particles where not found
                output.append(res)
        elif type(output) is HistogramContainer.HistogramContainer:
            #print('is a HistogramContainer.HistogramContainer')
            for res in _result:
                if check_value is not None:
                    output.inclusive.append(res)
                    #print(output.inclusive)
                else:
                    output.exclusive.append(res)
                    #print(output.exclusive)

        if check_value is not None: # it is a cut
            bool_result = check_value['which']([ utils.test( {**_r,**check_value} ) for _r in _result ])

            _result = bool_result*(_result[0]['weight'])  # 0 if bool_result was False; gives the weight if results was True
        if return_value==True:
            return _result


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

def phi(lhe_particles):
    '''
    lhe_particles is a LHEEvent.particles list
    '''
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.phi()


def theta(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.theta()

def eta(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.eta()

def rapidity(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.rapidity()

def number(lhe_particles):
    res=0
    for lv in lhe_particles:
        res=res+1
    return res

def energy(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.energy()

def perp(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.perp()

def pLong(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.pLong()

def pL(lhe_particles):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.pL()

def SinThetaStar_of2(lhe_particles):
    kZ=lhe_particles[0].fourvector()
    kW=lhe_particles[1].fourvector()
    kZ3 = np.array(kZ.three_components())
    kW3 = np.array(kW.three_components())
    #print(kZ3)
    #print(kW3)
    cross=np.sqrt(np.sum( np.cross(kZ3,kW3)**2 ) )
    #print(cross)
    kZ3+kW3
    norm=np.sqrt(np.sum( (kZ3+kW3)**2) )

    mW=kW.mass_safe()
    mZ=kZ.mass_safe()
    sZW=( (kZ+kW).mass() )**2

    pStar=np.sqrt( ( sZW - (mZ-mW)**2 )*( sZW - (mZ+mW)**2 )/(4*sZW) )

    res=cross/norm/pStar
    #print(res)
    return res





def missing_invariant_mass_fixed_com(lhe_particles,com=3000):
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv

    initial_state=lorentz.LorentzVector(px=0,py=0,pz=0,e=-com)

    missing = initial_state + _lv #this relies on making the vector with e= - COM

    return missing.signed_mass_squared()

def missing_invariant_mass(lhe_particles):

    initial_particles = [ p for p in lhe_particles if p.status == -1 ]
    final_particles = [ p for p in lhe_particles if p.status == 1 ]
    i_lv = lorentz.LorentzVector()
    f_lv = lorentz.LorentzVector()

    for lv in final_particles:
        f_lv=lv.fourvector()+f_lv
    for lv in initial_particles:
        i_lv=lv.fourvector()+i_lv

    missing = i_lv - f_lv

    return missing.signed_mass_squared()


def invariant_mass(lhe_particles):
    '''
    lhe_particles are LHEEvent.particles made in the function compute_obs_estensively
    computed_obs_values = [ obs(ev.particles) for ev in mixed_events ]
    '''
    _lv = lorentz.LorentzVector()
    for lv in lhe_particles:
        _lv=lv.fourvector()+_lv
    return _lv.mass()

def phi_wrt_ref(part_ref,DEBUG=False):
    """
        part_ref are LHEEvent.particles made in the function compute_obs_estensively
        computed_obs_values = [ obs(ev.particles) for ev in mixed_events ]
    """

    lhe_ev_part= part_ref[0]
    lhe_ev_ref= part_ref[1:]

    reference=lorentz.LorentzVector()
    for r in lhe_ev_ref:
        reference=reference+r.fourvector()
    parf_fv=lhe_ev_part.fourvector()
    if DEBUG: print('reference')
    if DEBUG: reference.print_fv()
    if DEBUG: print('vector')
    if DEBUG: parf_fv.print_fv()
    phi=parf_fv.phi_wrt_reference(reference=reference,second3vector=(0,0,1), DEBUG=False)

    return phi

def s_min(vis_inv):
    """
        lhe_ev_vis: is a LHE subevent containing all the particles to be considered as visible
        lhe_ev_inv: is a LHE subevent containing the one particle for the missing momentum
        in principle this observable depend on an external parameter, the mass of the invisible system
        this is for now fixed at zero and can be made an optional argument. in that case a dictionary input needs to be implemented in compute_obs_estensively
    """
    lhe_ev_vis=vis_inv[0]
    lhe_ev_inv=vis_inv[1]
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
