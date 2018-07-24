## should be modifiers.py
import lorentz, observables
import numpy as np


default_one_particle_modifier={ pid:None for pid in range(-25,26,1) if (np.abs(pid) <= 6 or (np.abs(pid)>= 11 and np.abs(pid) <=16) or np.abs(pid) > 20 )}

def smear_eta(lv,rel_unc=0.002,rnd=[]):
    ############################################################################
    # Get eta
    _eta = lv.eta()
    # smear it
    if rnd==[]:
        _new_eta = np.random.normal(_eta, np.fabs(rel_unc*_eta), 1) #improve performance by reading from a list of random variates
    else:
        _new_eta=rnd*_eta
    # transalte it in theta
    _new_theta = observables.ThetaFromEta(_new_eta)
    ############################################################################
    #print(_eta, observables.ThetaFromEta(_eta),lv.theta())

    #print(_new_eta,_new_theta, -np.log(np.tan(_new_theta/2.)) )
    _p=lv.mom()
    _pt=lv.perp()
    # conserve p, change theta
    _new_pz=_p*np.cos(_new_theta)
    #
    #print('p=',_p,' pT=',_pt,' new_pz=',_new_pz)
    _new_pt=_p*np.sin(_new_theta)
    _new_px=lv.px*_new_pt/_pt
    _new_py=lv.py*_new_pt/_pt
    #
    #print('p=',_p,' new_pT=',_new_pt,' new_pz=',_new_pz)

    _new_energy=np.sqrt(lv.mass()**2 + _new_px**2+_new_py**2+_new_pz**2)
    smeared_lv=lorentz.LorentzVector(px=_new_px,py=_new_py,pz=_new_pz,e=_new_energy)  # modifeid four vector
    return smeared_lv

def smear_energetics(lv,rel_unc=0.008,rnd=[]):
    # I want to smear eta, which is not a property. Smearing eta is like smearing pL/pT.
    # I will smear pL and adjust E to be on the mass shell
    # Get eta
    _eta = lv.eta()
    # smear it
    if rnd==[]:
        ec = np.random.normal(1, np.fabs(rel_unc), 1)[0] #improve performance by reading from a list of random variates
    else:
        ec=rnd
    smeared_lv=lorentz.LorentzVector(px=lv.px*ec,py=lv.py*ec,pz=lv.pz*ec,e=lv.e*np.fabs(ec))  # modifeid four vector, the energy correction is so that energy is always positive
    return smeared_lv
