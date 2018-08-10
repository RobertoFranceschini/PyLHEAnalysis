# boostrap from https://github.com/uschnoor

import ROOT
from ROOT import  TLorentzVector
import lhef
from copy import copy, deepcopy


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

        try:
            status = p.status
        except AttributeError:
            status =1

        _dict={'id':id,'status':status,\
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

    if branch == 'Particle' and id is None:
        # None is used as flag to not alter the ID present in the branch
        for p in branchDict[branch]:
            _muon=make_LHEparticle(p,id=p.PID )
            muons.append(_muon)
        return muons

    if branch != None and id !=None:
        # print('----------------')
        for p in branchDict[branch]:
            final_pid=deepcopy(id)
            #print('----')
            try:
                #print('trying tau')
                tautag=p.TauTag
                if tautag > 0:
                    final_pid=15*int(p.Charge)
                # print('was',tautag,'==>',final_pid)
            except AttributeError:
                pass
            try:
                # print('trying b')
                btag=p.BTag
                if btag >=4: #loose WP (90%))
                    final_pid=2
                if btag in [2,3,6,7]: #medium WP
                    final_pid=3
                if btag in [1,3,5,7]: #tight WP (50%eff)
                    final_pid=4
                # print('was',btag,'==>',final_pid)
            except AttributeError:
                pass
            #print(charged_pid(p,id))
            _muon=make_LHEparticle(p,id=charged_pid(p,final_pid) )
            muons.append(_muon)
        return muons

def ROOTfile2BranchDictTreeReader(inputfile = None, branches=None): #delphesDir+'tautau.s.gt.2TeV.root'
    ####### INIT THE BRANCHES #######
    if branches is not None:
        chain = ROOT.TChain("Delphes")
        chain.Add(inputfile)
        treereader = ROOT.ExRootTreeReader(chain)
        branchDict = {}
        for name in branches:
            branchDict[name] = treereader.UseBranch(name)
        #branchDict["Particle"] = treereader.UseBranch("Particle")
        #branchDict["Event"] = treereader.UseBranch("Event")
        #branchDict["Electron"] = treereader.UseBranch("Electron")
        #branchDict["Muon"] = treereader.UseBranch("Muon")
        #branchDict["Photon"] = treereader.UseBranch("Photon")
        #branchDict["VLCjetR10N4"] = treereader.UseBranch("VLCjetR10N4")
        #branchDict["VLCjetR10N2"] = treereader.UseBranch("VLCjetR10N2")
        #branchDict["MissingET"] = treereader.UseBranch("MissingET")

        return branchDict, treereader

def Tree2LHE(treereader=None,branchDict=None,event=None,branchesIDdict=None):
    if ( treereader is not None ) and ( branchDict is not None) and ( branchesIDdict is not None) and event >= 0:
        treereader.ReadEntry(event) # read from ROOT
        particles=[]

        # read particles into LHE particles objects
        for _branch, _id in branchesIDdict.items():
            _particles=branchToLHEparticles(branchDict,branch=_branch,id=_id)
            particles=particles + _particles
        np = len(particles)


        #electrons=branchToLHEparticles(branchDict,branch="Electron",id=11)
        #photons=branchToLHEparticles(branchDict,branch="Photon",id=22)
        #muons=branchToLHEparticles(branchDict,branch="Muon",id=13)
        #hadrons=branchToLHEparticles(branchDict,branch="VLCjetR10N2",id=1) # makes bjets, jets and had-tau
        #MTM=branchToLHEparticles(branchDict,branch="MissingET",id=0)

        # make list of particles
        #np=len(muons)+len(photons)+len(electrons)+len(hadrons)+len(MTM)
        #particles=particles+muons
        #particles=particles+electrons
        #particles=particles+photons
        #particles=particles+hadrons
        #particles=particles+MTM
        #print(len(particles))

        # make LHE event container
        _event_info_dict={'nparticles':np, 'pid':0, 'weight':1.0, 'scale':0, 'aqed':0, 'aqcd':0}
        lhe_info=lhef.LHEEventInfo(**_event_info_dict)
        lhe_event=lhef.LHEEvent(lhe_info,particles)
        return lhe_event
    else:
        print(treereader,branchDict,event,': all arguments are compulsory')
