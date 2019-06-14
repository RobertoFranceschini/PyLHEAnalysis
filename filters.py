# list of LHE particles gets filtered by single particle properties or properties of sets
import lorentz, observables, lhef
import numpy as np
from copy import copy, deepcopy


def filter_by_pid(event=None, pids=[]):
    if event is not None:
        ev_info = event.eventinfo
        new_particles=[]
        for p in event.particles:
            if p.id in pids:
                new_particles.append(p)

        modified_event = lhef.LHEEvent(ev_info,new_particles)
        return modified_event

def filter_by_function(event=None, function=None, inplace=False,stop_at=None,DEBUG=False,**kwargs):
    if DEBUG: print('event ',event)
    if DEBUG: print('function ',function)
    if DEBUG: print('inplace ',inplace)
    if event is not None:
        if inplace:
            modified_event = event # reference to object, will affect the original
        else:
            modified_event = deepcopy(event) # clone the event
        new_particles=[]
        for p in event.particles:
            if function(p):
                new_particles.append(p)
                if stop_at is not None:
                    if len(new_particles)>stop_at:
                        break

        modified_event.particles = new_particles
        return modified_event


def sorted_by_function(event=None, function=None, inplace=False, requested=None, strict=True):
    if (event is not None) and (requested is not None):
        if inplace:
            modified_event = event # reference to object, will affect the original
        else:
            modified_event = deepcopy(event) # clone the event


        new_particles=[] # new particles to be put in the EVENT

        value_particles = [ (function(p),p) for p in event.particles ]
        sorted_value_particles = sorted(value_particles,reverse=True)

        for ind in requested:
            try:
                new_particles.append(sorted_value_particles[ind][1] )
            except IndexError:
                if strict == False:
                    pass
                else:
                    new_particles=[]

        modified_event.particles =  new_particles

        return modified_event
