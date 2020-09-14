# with contributions from https://github.com/lukasheinrich/lorentz/blob/master/lorentz/

import math, sys
import numpy as np
import utils as u

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

    def three_components(self):
        return (self.px,self.py,self.pz)

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
        '''
        arctan2 from -Pi to +Pi
        '''
        return np.arctan2( self.py , self.px  )



    def beta_vector(self):
        return  np.array([ self.px/self.e , self.py/self.e , self.pz/self.e ] )

    def beta_scalar(self):
        return  np.sqrt(self.px**2 + self.py**2 + self.pz**2 )/self.e

    def GammaOfBeta(beta):
        return 1./np.sqrt(1.-beta**2)

    def gamma(self):
        return  self.e/np.sqrt(self.e**2 - (self.px**2 + self.py**2 + self.pz**2) )

    def betagamma(self):
        return  np.sqrt(self.px**2 + self.py**2 + self.pz**2 )/np.sqrt(self.e**2 - (self.px**2 + self.py**2 + self.pz**2) )

    def mass(self):
        return  np.sqrt(self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) )

    def mass_safe(self):
        return  np.sqrt(max(0, self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) ) )

    def signed_mass_squared(self):
        return  np.sign(self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) )  * np.sqrt(np.abs(self.e**2 - ( self.px**2 + self.py**2 + self.pz**2) ))

    def mom(self):
        return  np.sqrt( ( self.px**2 + self.py**2 + self.pz**2) )

    def cosTheta(self):
        return np.cos(self.theta())

    def energy(self):
        return self.e

    def pLong(self):
        return self.pz

    def pL(self):
        return self.pz

    def perp(self):
        return  np.sqrt( ( self.px**2 + self.py**2  ) )


    def NewTriadFromLorentzVector(self,second3vector=None):
        """
        Takes a 4-vector and produces a new triad of orthonormal vectors \
    suitable as coordinates for a reference frame with third component \
    oriented along the given 3-vector. The result contains a matrix which applied to x,y,z gives v_i.
    """
        _beta=self.beta_vector()  # is an np.array
        _beta_u=u.versor(_beta)

        if second3vector == None:
            _random_lepton=np.random.rand(3)
        else:
            _random_lepton=second3vector

        _lbetaort=np.cross(_beta,_random_lepton)
        _lbetaort_u=u.versor(_lbetaort)

        _lbetaortort=np.cross(_beta,_lbetaort)
        _lbetaortort_u=u.versor(_lbetaortort)

        result = {}
        result['vectors']=np.array([_lbetaort_u,_lbetaortort_u,_beta_u])
        result['x2prime']=result['vectors']
        result['prime2x']=np.transpose(result['x2prime'])

        return result

    def NewTriadYFromLorentzVector(self,second3vector=None):
        """
        Takes a 4-vector and produces a new triad of orthonormal vectors \
    suitable as coordinates for a reference frame with third component \
    oriented along the given 3-vector. The result contains a matrix which applied to x,y,z gives v_i.

    It differs from NewTriadFromLorentzVector for an exchange x-y, which we prefer to not add as an option.

    """
        _beta=self.beta_vector()
        _beta_u=u.versor(_beta)

        if second3vector == None:
            _random_lepton=np.random.rand(3)
        else:
            _random_lepton=second3vector

        _lbetaort=np.cross(_beta,_random_lepton)
        _lbetaort_u=u.versor(_lbetaort)

        _lbetaortort=np.cross( _lbetaort, _beta )
        _lbetaortort_u=u.versor(_lbetaortort)

        result = {}
        result['vectors']=np.array([_lbetaortort_u, _lbetaort_u ,_beta_u])
        result['x2prime']=result['vectors']
        result['prime2x']=np.transpose(result['x2prime'])

        return result

    def costheta_wrt_reference(self,reference=None, DEBUG=False): #second3vector=(0,0,1),NewTriadFromLorentzVector=NewTriadFromLorentzVector):
        if reference is not None:
            _beta=self.beta_vector() # is an np.array
            _beta_u=u.versor(_beta)
            _reference=reference.beta_vector() # is an np.array
            _reference_u=u.versor(_reference)

            cos = contract_tuples(_beta_u, _reference_u, metric = None)
            if DEBUG:
                print('cos',cos,' theta:',np.arccos(cos))
            return cos
        else:
            print('The named paramter *reference* needs to be specified')
            return np.nan()

    def sintheta_wrt_reference(self,reference=None, DEBUG=False): #second3vector=(0,0,1),NewTriadFromLorentzVector=NewTriadFromLorentzVector):
        if reference is not None:
            _beta=self.beta_vector() # is an np.array
            _beta_u=u.versor(_beta)
            _reference=reference.beta_vector() # is an np.array
            _reference_u=u.versor(_reference)

            _ort = np.cross(_beta_u, _reference_u)

            sin = np.sqrt( contract_tuples(_ort, _ort, metric = None) )

            if DEBUG:
                print('sin',sin,' theta:',np.arcsin(sin))
            return sin
        else:
            print('The named paramter *reference* needs to be specified')
            return np.nan()



    def theta_wrt_referenceY(self,reference=None,second3vector=(0,0,1), DEBUG=False,NewTriadFromLorentzVector=NewTriadYFromLorentzVector):
        return theta_wrt_reference(self,reference=reference,second3vector=second3vector, DEBUG=DEBUG,NewTriadFromLorentzVector=NewTriadFromLorentzVector)

    def theta_wrt_reference(self,reference=None,second3vector=(0,0,1), DEBUG=False,NewTriadFromLorentzVector=NewTriadFromLorentzVector):
        if reference is not None:
            newBasis=reference.NewTriadFromLorentzVector(second3vector=second3vector )
            if DEBUG: print(newBasis['x2prime'])
            if DEBUG: print(newBasis['vectors'])
            newpl=self.Change3DBasis(newBasis['vectors'])
            return newpl.theta()
        else:
            print('The named paramter *reference* needs to be specified')
            return np.nan()

    def phi_wrt_referenceY(self,reference=None,second3vector=(0,0,1), DEBUG=False,NewTriadFromLorentzVector=NewTriadYFromLorentzVector):
        return phi_wrt_reference(self,reference=reference,second3vector=second3vector, DEBUG=DEBUG,NewTriadFromLorentzVector=NewTriadFromLorentzVector)

    def phi_wrt_reference(self,reference=None,second3vector=(0,0,1), DEBUG=False,NewTriadFromLorentzVector=NewTriadFromLorentzVector):
        if reference is not None:
            newBasis=reference.NewTriadFromLorentzVector(second3vector=second3vector )
            if DEBUG: print(newBasis['x2prime'])
            if DEBUG: print(newBasis['vectors'])
            newpl=self.Change3DBasis(newBasis['vectors'])

            newreference=reference.Change3DBasis(newBasis['vectors'])
            if DEBUG: print('newreference')
            if DEBUG: newreference.print_fv()
            return newpl.phi()
        else:
            print('The named paramter *reference* needs to be specified')
            return np.nan()


    def Change3DBasis(self,newBasis):
        _self3=self.three_components()
        _newpxyz=[ np.dot(v,_self3) for v in newBasis ]
        return LorentzVector(px=_newpxyz[0],py=_newpxyz[1],pz=_newpxyz[2],e=self.e)

    def Change3DBasisRotation(self,rotation):
        rotated=np.matmul(rotation,self.three_components() )
        return LorentzVector( e=self.e, px=rotated[0], py=rotated[1], pz=rotated[2])

    def BoostBetaAlongZ(self,beta):
        return LorentzVector( e=self.e/np.sqrt(1 - beta**2) + (self.pz*beta)/np.sqrt(1 - beta**2), px= self.px, py=self.py, pz=self.pz/np.sqrt(1 - beta**2) + (self.e*beta)/np.sqrt(1 - beta**2 ) )

    def ToMothersFrameWithZalongMotherParticleMomentum(self,Mother, DEBUG=False):
        '''
        This function applied to a daughter particle returns its four-vector in the frame where its mother is a rest. The Z axis of this rest frame is chosen so that it coincides with the direction of the boost beetween the rest frame of the mother and lab frame.
        This function is useful to evaluate the angle between the W boson velocity and the lepton velocity in its decay.
        '''
        #Daughter=Self
        if DEBUG: print(np.dot(Mother.NewTriadFromLorentzVector(second3vector=self.three_components() )['prime2x'],np.array([1,0,0]) )
    )
        # new triad with z-axis along mother momentum and y along daughter momentum y component
        newBasis=Mother.NewTriadFromLorentzVector(second3vector=self.three_components() )
        if DEBUG: print(newBasis['x2prime'])

        # Dauther 4V in the new basis
        newpl=self.Change3DBasis(newBasis['vectors'])
        if DEBUG: print(newpl.components()) # same as in Mathematica

        if DEBUG: print(Mother.beta_scalar()) # Same as in Mathematica

        # Daughter 4V after a boost in the direction *opposite* to the boost of the mother
        _lGen4VPrimeBoosted=newpl.BoostBetaAlongZ( -Mother.beta_scalar() )
        if DEBUG: print(_lGen4VPrimeBoosted.components()) # Same as in Mathematica

        # Daughter 4V rotated back to the original X,Y,Z (axes oriented as in the lab)
        _lGen4VPrimeBoostedUnprimed=_lGen4VPrimeBoosted.Change3DBasisRotation( newBasis['prime2x'] )
        print(_lGen4VPrimeBoostedUnprimed.components()) # Same as in Mathematica
        return _lGen4VPrimeBoostedUnprimed
