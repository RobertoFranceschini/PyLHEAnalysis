# with contributions from https://github.com/lukasheinrich/lorentz/blob/master/lorentz/

import math, sys
import numpy as np

METRIC = [-1,-1,-1,1]

def contract_tuples(lhs,rhs,metric = None):
    return sum(m*l*r for m,l,r in zip(metric if metric else [1]*len(lhs),lhs,rhs))

class LorentzVector(object):

    """
    A class for Lorentz four-vectors stuff
    """
    def __init__(self,px=0,py=0,pz=0,e=0):
        self._px = px
        self._py = py
        self._pz = pz
        self._e = e

    def __add__(lhs,rhs):
        return LorentzVector(*[sum(x) for x in zip(lhs.components(),rhs.components())])

    def __sub__(lhs,rhs):
        return LorentzVector(*[sum(x) for x in zip(lhs.components(),rhs.minuscomponents())])

    def __mul__(lhs,rhs):
        return contract_tuples(lhs,rhs,metric = METRIC)



    def assign(self,px=0,py=0,pz=0,e=0):
        self._px = px
        self._py = py
        self._pz = pz
        self._e = e


    def components(self):
        return (self.px,self.py,self.pz,self.e)

    def minuscomponents(self):
        return (-self.px,-self.py,-self.pz,-self.e)

    def print_fv(self):
        print(self.px,self.py,self.pz,self.e)

    def emptyQ(self):
        if  self.px==0 and self.py==0 and self.pz==0 and self.e==0:
            return True
        else:
            return False

    # https://www.programiz.com/python-programming/property

    @property
    def px(self):
        return self._px
    @property
    def py(self):
        return self._py
    @property
    def pz(self):
        return self._pz
    @property
    def e(self):
        return self._e

    # FUNCTIONS

    def eta(self):
        if abs(self.perp()) < sys.float_info.epsilon:
            return float('inf') if self.pz >=0 else float('-inf')
        return -np.log(np.tan(self.theta()/2.))


    def rapidity(self):
        return 0.5*np.log( (self.e + self.pz)/(self.e - self.pz)  )

    # @property
    # def theta_from_pT(self):
    #     return np.arctan2(self.perp(), self.e)

    def theta(self):
        return np.arccos(self.pz / np.sqrt(self.px**2 + self.py**2 + self.pz**2 ) )

    def phi(self):
        return np.arctan( self.py / self.px  )


    def beta_scalar(self):
        return  np.sqrt(self.px**2 + self.py**2 + self.pz**2 )/self.e

    def gamma(self):
        return  self.e/np.sqrt(self.e**2 - (self.px**2 + self.py**2 + self.pz**2) )

    def betagamma(self):
        return  np.sqrt(self.px**2 + self.py**2 + self.pz**2 )/np.sqrt(self.e**2 - (self.px**2 + self.py**2 + self.pz**2) )

    def mass(self):
        return  np.sqrt(self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) )

    def signed_mass_squared(self):
        return  np.sign(self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) )  * np.sqrt(np.abs(self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) ))

    def mom(self):
        return  np.sqrt( ( self.px**2 + self.py**2 + self.pz**2) )

    def cosTheta(self):
        return np.cos(self.theta())

    def energy(self):
        return self.e

    def perp(self):
        return  np.sqrt( ( self.px**2 + self.py**2  ) )
