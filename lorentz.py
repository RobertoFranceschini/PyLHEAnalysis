# with contributions from https://github.com/lukasheinrich/lorentz/blob/master/lorentz/

import math

METRIC = [-1,-1,-1,1]

def contract_tuples(lhs,rhs,metric = None):
    return sum(m*l*r for m,l,r in zip(metric if metric else [1]*len(lhs),lhs,rhs))

class LorentzVector(object):

    """
    A class for Lorentz four-vectors stuff
    """
    def __init__(self,px,py,pz,e):
        self._px = px
        self._py = py
        self._pz = pz
        self._e = e

    def components(self):
        return (self.px,self.py,self.pz,self.e)

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

    # @property
    # def theta_from_pT(self):
    #     return math.atan2(self.perp(), self.e)
    @property
    def theta(self):
        return math.acos(self.pz / math.sqrt(self.px**2 + self.py**2 + self.pz**2 ) )

    @property
    def beta_scalar(self):
        return  math.sqrt(self.px**2 + self.py**2 + self.pz**2 )/self.e

    def cosTheta(self):
        return math.cos(self.theta)

    def perp2(self):
        transvers_comps = self.components()[0:1]
        return contract_tuples(transvers_comps,transvers_comps)
    def perp(self):
        return math.sqrt(self.perp2())
