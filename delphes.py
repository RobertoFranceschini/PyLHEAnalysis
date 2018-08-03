# boostrap from https://github.com/uschnoor

import ROOT
from ROOT import  TLorentzVector
import lhef


def make_LHEparticle(p,id=None):
    if id != None:
        fv=TLorentzVector()
        fv.SetPtEtaPhiM(p.PT, p.Eta, p.Phi, 0.105)
        _dict={'id':id,'status':1,\
                          'mother1':0,'mother2':0,'color1':0,'color2':0,\
                          'px':fv.Px(),'py':fv.Py(),'pz':fv.Pz(),'e':fv.Energy(),'m':fv.M(),'lifetime':0,'spin':0}
        lhepart=lhef.LHEParticle(**_dict)
        return lhepart
    else:
        print("id must be specified")
        pass


def branchToLHEparticles(branchDict,branch=None,id=None):
    muons=[]
    if branch != None and id !=None:
        for p in branchDict[branch]:
            _muon=make_LHEparticle(p,id=int(id*p.Charge) )
            muons.append(_muon)
        return muons
