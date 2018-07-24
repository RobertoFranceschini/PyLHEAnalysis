# STARTED FROM Shttps://github.com/lukasheinrich/pylhe

import os

class LHEFile(object):
    def __init__(self):
        pass

class LHEEvent(object):
    def __init__(self,eventinfo,particles):
        self.eventinfo = eventinfo
        self.particles = particles
        for p in self.particles:
            p.event = self

class LHEEventInfo(object):
    fieldnames = ['nparticles', 'pid', 'weight', 'scale', 'aqed', 'aqcd']
    def __init__(self, **kwargs):
        if not set(kwargs.keys()) == set(self.fieldnames):
            raise RuntimeError
        for k,v in kwargs.items():
            setattr(self,k,v)

    @classmethod
    def fromstring(cls,string):
        return cls(**dict(list(zip(cls.fieldnames,list(map(float,string.split()))))))


import lorentz


class LHEParticle(object):
    fieldnames = fieldnames = ['id','status','mother1','mother2','color1','color2','px','py','pz','e','m','lifetime','spin']
    def __init__(self, **kwargs):
        if not set(kwargs.keys()) == set(self.fieldnames):
            raise RuntimeError
        for k,v in kwargs.items():
            setattr(self,k,v)

    @classmethod
    def fromstring(cls,string):
        obj = cls(**dict(list(zip(cls.fieldnames,list(map(float,string.split()))))))
        return obj

    def mothers(self):
        mothers = []
        first_idx  =  int(self.mother1)-1
        second_idx =  int(self.mother2)-1
        for idx in set([first_idx,second_idx]):
            if idx >= 0: mothers.append(self.event.particles[idx])
        return mothers

    def fourvector(self):
        lv=lorentz.LorentzVector(self.px, self.py, self.pz, self.e)
        return lv

def loads():
    pass

import xml.etree.ElementTree as ET
def readLHE(thefile):
    try:
        for event,element in ET.iterparse(thefile,events=['end']):
            if element.tag == 'event':
                data = element.text.split('\n')[1:-1]
                eventdata,particles = data[0],data[1:]
                eventinfo = LHEEventInfo.fromstring(eventdata)
                particle_objs = []
                for p in particles:
                    particle_objs+=[LHEParticle.fromstring(p)]
                yield LHEEvent(eventinfo,particle_objs)

    except ET.ParseError:
        print("WARNING. Parse Error.")
        return

def get_lv(p,destination=None,status=1,pid=-21,modifiers=[],ranlist=[]):
    """
    Get a Lorentz vector from a LHE particle p only if it machtes status and pid
    If ran and modifiers are provided, the modifiers are applied in chain, each with random variate equal to last item of ran (will pop the element).
    """
    lvA=lorentz.LorentzVector()
    if p.status == status and ( p.id == pid  ): # check it is a final state and is a Chi+

        lvA=p.fourvector() # make four vector
        if len(modifiers)>0:
            lvA_smeared=deepcopy(lvA)
            for modifier,rel_unc in modifiers:#[ [modifiers[i],ran[i]] for i in range(len(modifiers))]:
                r=[]
                if len(ranlist)>0:
                    r=ranlist.pop()
                lvA_smeared=modifier(lvA_smeared,rel_unc=rel_unc,rnd=r)
            lvA=lvA_smeared
    if destination==None:
        return lvA
    else:
        if lvA.emptyQ()==False:
            destination.assign(px=lvA.px,py=lvA.py,pz=lvA.pz,e=lvA.e)



def event_modifier_detector(e,rules,ran=[],inplace=False):
    """
    returns a modified LHE event

    ran:
        is either a list of variates.
        If rnd is empty get_lv will make a random number,
        otherwise is passed to the get_lv, which will pop elements out of it.
    """
    new_particles=[] # create container for the new
    if inplace:
        modified_event = e # reference to object, will affect the original
    else:
        modified_event = deepcopy(e) # clone the event
    for p in modified_event.particles: # modify each particle one by one
        if p.status == 1 and rules[p.id] !=None:
            #apply list of functions
            #original=get_lv(p,status=1,pid=p.id) # gets the lorentz vector from this LHE particle
            #
            modified=get_lv(p,status=1,pid=p.id,modifiers=rules[p.id],ranlist=ran) # gets and smears the lorentz vector from this LHE particle. Random variates are popped out of ran
            p.px = modified.px
            p.py = modified.py
            p.pz = modified.pz
            p.e = modified.e
            lhe_modified=get_lv(p,status=1,pid=p.id)
            #print("η'/η",lhe_modified.eta()/original.eta())
        new_particles.append(p) # append the modified particle to the container
    modified_event.particles = new_particles # change the particles
    return modified_event
