# boostrap from https://github.com/uschnoor

import ROOT
from ROOT import  TLorentzVector
import lhef


def make_LHEparticle(p,id=None):
    if id != None:
        fv=TLorentzVector()
        
        try:
            m=p.Mass
        except AttributeError:
            m=0

        try:
            pT=p.PT
        except AttributeError:
            pT=p.MET

        fv.SetPtEtaPhiM(pT, p.Eta, p.Phi, m)

        _dict={'id':id,'status':1,\
                          'mother1':0,'mother2':0,'color1':0,'color2':0,\
                          'px':fv.Px(),'py':fv.Py(),'pz':fv.Pz(),'e':fv.Energy(),'m':fv.M(),'lifetime':0,'spin':0}
        lhepart=lhef.LHEParticle(**_dict)
        return lhepart
    else:
        print("id must be specified")
        pass

def charged_pid(p,id):
    if abs(id) in [11,13]:
        return int(id*p.Charge)
    else:
        return int(id)

def branchToLHEparticles(branchDict,branch=None,id=None):
    # btag is added to jet PID = 1
    # tau tag is used to make a PID= +-15
    muons=[]
    tautag = None
    btag = None
    if branch != None and id !=None:
        for p in branchDict[branch]:
            try:
                tautag=p.TauTag
                id=15*int(p.Charge)
            except AttributeError:
                pass
            try:
                btag=p.BTag
                if btag >=4: #loose WP (90%))
                    id=2
                if btag in [2,3,6,7]: #medium WP
                    id=3
                if btag in [1,3,5,7]: #tight WP (50%eff)
                    id=4
            except AttributeError:
                pass
            _muon=make_LHEparticle(p,id=charged_pid(p,id) )
            muons.append(_muon)
        return muons
