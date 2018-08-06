# list of LHE particles gets filtered by single particle properties or properties of sets
import lorentz, observables, lhef
import numpy as np

def filter_by_pid(event=None, pids=[]):
    if event is not None:
        ev_info = event.eventinfo
        new_particles=[]
        for p in event.particles:
            if p.id in pids:
                new_particles.append(p)

        modified_event = lhef.LHEEvent(ev_info,new_particles)
        return modified_event

def filter_by_function(event=None, pids=[],function=None):
    if event is not None:
        ev_info = event.eventinfo
        new_particles=[]
        for p in event.particles:
            if function(p):
                new_particles.append(p)

        modified_event = lhef.LHEEvent(ev_info,new_particles)
        return modified_event
