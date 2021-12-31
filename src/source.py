import numpy as np

from obspy.core import UTCDateTime

epsilon = 1e-13

class source:
  def __init__(self, time, lat, lon, depth, strike, deep, rake, mw):

    self.lat = lat
    self.lon = lon
    self.depth = depth   
    self.time = time
    #self.mxx = np.array([1.0,1.0,1.0,1.0,1.0,1.0])*mw
    
  def __init__(self, time, lat, lon, depth, peak_freq, isDC, mxx, myy, mzz, mxy, mxz, myz):

    self.lat = lat
    self.lon = lon
    self.depth = depth   
    self.time = time
    self.peak_freq = peak_freq
    self.mt_scale = abs(np.amax([mxx,myy,mzz,mxy,mxz,myz]))
    self.mxx = mxx/self.mt_scale
    self.mxy = mxy/self.mt_scale
    self.mxz = mxz/self.mt_scale
    self.myy = myy/self.mt_scale
    self.myz = myz/self.mt_scale
    self.mzz = mzz/self.mt_scale
    
    self.isDC = isDC
 
    #M = np.array([[mxx,mxy,mxz],[mxy,myy,myz],[mxz,myz,mzz]])
    #M0 = self.standard_decomposition(M)    
    #self.M0 = M0


  def standard_decomposition(self, M):
      """
      Decomposition according Aki & Richards and Jost & Herrmann into

      - isotropic
      - deviatoric
      - DC
      - CLVD

      parts of the input moment tensor.

      results are given as attributes, which can be returned via 'get_<name of attribute>' functions:

      DC
      CLVD
      DC_percentage
      seismic_moment
      moment_magnitude

      """

      #isotropic part
      M_iso   = np.diag( np.array([1./3*np.trace(M),1./3*np.trace(M),1./3*np.trace(M)] ) )
      M0_iso  = abs(1./3*np.trace(M))

      #deviatoric part
      M_devi  = M - M_iso

      #self._isotropic  = M_iso
      #self._deviatoric = M_devi

      #eigenvalues and -vectors
      eigenwtot,eigenvtot  = np.linalg.eig(M_devi)

      #eigenvalues and -vectors of the deviatoric part
      eigenw1,eigenv1  = np.linalg.eig(M_devi)

      #eigenvalues in ascending order:
      eigenw           = np.real( np.take( eigenw1,np.argsort(abs(eigenwtot)) ) )
      eigenv           = np.real( np.take( eigenv1,np.argsort(abs(eigenwtot)) ,1 ) )

      #eigenvalues in ascending order in absolute value!!:
      eigenw_devi           = np.real( np.take( eigenw1,np.argsort(abs(eigenw1)) ) )
      eigenv_devi           = np.real( np.take( eigenv1,np.argsort(abs(eigenw1)) ,1 ) )

      M0_devi          = max(abs(eigenw_devi))

      #named according to Jost & Herrmann:
      a1 = eigenv[:,0]#/N.linalg.norm(eigenv[:,0])
      a2 = eigenv[:,1]#/N.linalg.norm(eigenv[:,1])
      a3 = eigenv[:,2]#/N.linalg.norm(eigenv[:,2])

      # if only isotropic part exists:
      if M0_devi < epsilon:
          F = 0.5
      else:
          F           = -eigenw_devi[0]/eigenw_devi[2]


      M_DC        = np.matrix(np.zeros((9),float)).reshape(3,3)
      M_CLVD      = np.matrix(np.zeros((9),float)).reshape(3,3)

      M_DC        = eigenw[2]*(1-2*F)*( np.outer(a3,a3) - np.outer(a2,a2) )
      M_CLVD      = M_devi - M_DC #eigenw[2]*F*( 2*N.outer(a3,a3) - N.outer(a2,a2) - N.outer(a1,a1))


      #according to Bowers & Hudson:
      M0          = M0_iso + M0_devi

      M_iso_percentage     = int(round(M0_iso/M0 *100,6))
      self._iso_percentage = M_iso_percentage


      M_DC_percentage = int(round(( 1 - 2 * abs(F) )* ( 1 - M_iso_percentage/100.)  * 100,6))


      #self._DC            =  M_DC
      #self._CLVD          =  M_CLVD
      #self._DC_percentage =  M_DC_percentage

      ##self._seismic_moment   = np.sqrt(1./2*N.sum(eigenw**2) )
      #self._seismic_moment   = M0
      #self._moment_magnitude = N.log10(self._seismic_moment*1.0e7)/1.5 - 10.7  

      return M0      


    
