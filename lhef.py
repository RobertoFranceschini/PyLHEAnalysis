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
