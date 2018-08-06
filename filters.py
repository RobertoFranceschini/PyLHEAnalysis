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

def filter_by_function(event=None, function=None, inplace=False):
    if event is not None:
        if inplace:
            modified_event = event # reference to object, will affect the original
        else:
            modified_event = deepcopy(event) # clone the event
        new_particles=[]
        for p in event.particles:
            if function(p):
                new_particles.append(p)

        modified_event.particles =  new_particles

        return modified_event
