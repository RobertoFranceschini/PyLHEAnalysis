# list of LHE particles gets filtered by single particle properties or properties of sets
import lorentz, observables, lhef
import numpy as np

def filter_by_pid(event=None, pids=[]):
    if event is not None:
        ev_info = event.eventinfo
        new_particles=[]
        for p in event.particles:
            if p.id is in pids:
                new_particles.append(p)
        modified_event = lhef.LHEEvent()
        modified_event = ev_info
        modified_event.particles = new_particles
        return modified_event
