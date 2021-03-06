# STARTED FROM Shttps://github.com/lukasheinrich/pylhe

import os, utils
from copy import copy, deepcopy

class LHEFile(object):
    def __init__(self):
        pass

class LHEEvent(object):
    def __init__(self,eventinfo,particles):
        self.eventinfo = eventinfo
        self.particles = particles
        for p in self.particles:
            p.event = self

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def print_event(self):
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        try:
            print('event number ', self.eventinfo.event_number)
        except AttributeError:
            print('no event number information')
            pass
        self.eventinfo.print_event_info()
        print('-----------------------------------------------------------------')
        for _p in self.particles:
            print('**************')
            _p.print_lhe_particle()



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

    def print_event_info_general(self):
        _attribs =  [a for a in dir(self) if not a.startswith('__')]
        #print( _attribs  )
        for __a in _attribs:
            print( __a, getattr(self,__a) )

    def print_event_info(self):
        #_attribs =  [a for a in dir(self) if not a.startswith('__')]
        #print( _attribs  )
        for __a in self.fieldnames:
            print( __a, getattr(self,__a) )


import lorentz


class LHEParticle(object):
    #fieldnames = fieldnames = ['id','status','mother1','mother2','color1','color2','px','py','pz','e','m','lifetime','spin']
    fieldnames = ['id','status','mother1','mother2','color1','color2','px','py','pz','e','m','lifetime','spin']
    def __init__(self, **kwargs):
        if not set(kwargs.keys()) == set(self.fieldnames):
            raise RuntimeError
        for k,v in kwargs.items():
            setattr(self,k,v)

    @classmethod


    def fromstring(cls,string):
        obj = cls(**dict(list(zip(cls.fieldnames,list(map(float,string.split()))))))
        return obj

    def empty(cls,string=13*'NaN '):
        obj = cls(**dict(list(zip(cls.fieldnames,list(map(float,string.split()))))))
        return obj

    def print_lhe_particle(self):
        for __a in self.fieldnames:
            print( __a, getattr(self,__a) )
        import numpy as np
        print('phi=',self.fourvector().phi() )
        print('theta=',self.fourvector().theta() )
        print('theta=',np.rad2deg(self.fourvector().theta()), 'deg' )

    def print_lhe_particle_general(self):
        _attribs =  [a for a in dir(self) if not a.startswith('__')]
        print( _attribs  )
        for __a in _attribs:
            print( __a, getattr(self,__a) )

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



def event_modifier_reverse_fourmomenta(e,inplace=False):
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
        p.px = -p.px
        p.py = -p.py
        p.pz = -p.pz
        p.e = -p.e
        new_particles.append(p) # append the modified particle to the container
    modified_event.particles = new_particles # change the particles
    return modified_event


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
            #print("eta'/eta",lhe_modified.eta()/original.eta())
        new_particles.append(p) # append the modified particle to the container
    modified_event.particles = new_particles # change the particles
    return modified_event

def outerLHEevents(list_of_LHEevents): # list of LHEevents usually made of filtered particles
    DEBUG=False
    def _testij(i,j):
        if len(list_of_LHEevents) == 2:
            return True
        elif j > i:
            return True
        else:
            False


    def acceptable_shape(list_of_LHEevents):
        _accept=False
        if (type(list_of_LHEevents) is list): # is a list of events
            if (type(list_of_LHEevents[0].particles) is list):
                if len(list_of_LHEevents) == 2: # is a list containing two events
                    _accept=True
                elif  len(list_of_LHEevents) == 1: # is a list containing one event
                    if len(list_of_LHEevents[0].particles)>1: # and it has 2 or more particles
                        _accept=True
        return _accept

    if acceptable_shape(list_of_LHEevents): # for now is only implemented what to do with two lists or one

        muons=list_of_LHEevents[0]
        muonsbar = muons

        if len(list_of_LHEevents) == 2:
            muonsbar = list_of_LHEevents[1]

        _mat=[ [  LHEEvent(muons.eventinfo, [muons.particles[i], muonsbar.particles[j]])  for j in range(len(muonsbar.particles))  if _testij(i,j) ] for i in range(len(muons.particles)) ] # _mat is a matrix of LHEevents

        return utils.flattenOnce(_mat) # this is a 1D list of LHEevents, same as the input, hence it can be made an iterative function if I need it to be
    else:
        if DEBUG: print(list_of_LHEevents)
        return None # not enough or too many particles provided

def acceptable_shape_at_least_N(list_of_LHEevents,nmin=0):
    _accept=False
    if (type(list_of_LHEevents) is list): # is a list of events
        if len(list_of_LHEevents) > 0:
            if (type(list_of_LHEevents[0].particles) is list):
                if (len(list_of_LHEevents[0].particles) > nmin ):
                    _accept=True
    return _accept


def splitterLHEevents(list_of_LHEevents): # list of LHEevents usually made of filtered particle
    '''
    TOCHECK
    Take an event containing N>0 particles and returns a list of events with one particle in each event
    '''
    if acceptable_shape_at_least_N(list_of_LHEevents,nmin=0):
        muons=list_of_LHEevents[0]

        _mat=[ LHEEvent(muons.eventinfo, [muon])  for muon in muons.particles ] # _mat is a matrix of LHEevents

        return _mat #utils.flattenOnce(_mat) # this is a 1D list of LHEevents, same as the input, hence it can be made an iterative function if I need it to be
    else:
        return None

def mergeLHEevents(LHEevent): # list of LHEevents usually made of filtered particle

    if type(LHEevent) is list: # How can it be a list here and then have a particle member later????
        muons=deepcopy(LHEevent)

        lv =lorentz.LorentzVector()
        p=None
        for muon in muons.particles:
            p=muon
            _lv=muon.fourvector()
            lv=lv+_lv
            p.px = lv.px
            p.py = lv.py
            p.pz = lv.pz
            p.e = lv.e

        muons.particles=[p]

        _res = LHEEvent(muons.eventinfo, muons.particles)
        return _res #utils.flattenOnce(_mat) # this is a 1D list of LHEevents, same as the input, hence it can be made an iterative function if I need it to be
    else:
        return None

def sumLHEevents(LHEevents, DEBUG=False): # list of LHEevents usually made of filtered particle
    '''
    Take a list of events and returns a single event made of a single particle
    with no PID and four-vector equal to the sum of the particles of the events
    that have been passed as input
    '''
    if type(LHEevents) is list:
        flat_event=deepcopy(LHEevents[0])
        p=LHEParticle.fromstring(13*'NaN ')
        lv =lorentz.LorentzVector()
        for subev in LHEevents:
            for muon in subev.particles:
                _lv=muon.fourvector()
                if DEBUG: _lv.print_fv()
                lv=lv+_lv

        p.px = lv.px
        p.py = lv.py
        p.pz = lv.pz
        p.e = lv.e

        flat_event.particles=[p]

        _res = LHEEvent(flat_event.eventinfo, flat_event.particles)
        return _res

def flattenLHEevents(LHEevents): # list of LHEevents usually made of filtered particle
    '''
    Take a list of events and returns a single event made of all the particles
    '''
    if type(LHEevents) is list:
        flat_event=deepcopy(LHEevents[0])
        p=[]
        for subev in LHEevents:
            for muon in subev.particles:
                p+=[muon]

        flat_event.particles=p

        _res = LHEEvent(flat_event.eventinfo, flat_event.particles)
        return _res #utils.flattenOnce(_mat) # this is a 1D list of LHEevents, same as the input, hence it can be made an iterative

def identiyLHEevents(list_of_LHEevents): # list of LHEevents usually made of filtered particle
    """
        does not check if the list contains events or not
    """
    if acceptable_shape_at_least_N(list_of_LHEevents,nmin=-1):
        return list_of_LHEevents
    else:
        return None

def passLHEevents(list_of_LHEevents): # list of LHEevents usually made of filtered particle
    """
        does not check if the list contains events or not
    """
    if type(list_of_LHEevents) is list:
        return list_of_LHEevents
    else:
        return None
