import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper

import obspy
from obspy.core import UTCDateTime

import numpy as np                  # all matrix manipulations & OpenGL args

import src.simulation_params as simulation_params

from src.opengl_helpers import *

class simulation_source:
  def __init__(self, sim_params, sourceList):
  
    self.sim_params = sim_params

    self.max_t_steps = 100000
            
    self.bodyforcex = []
    self.bodyforcey = []
    self.bodyforcez = []
          
    self.source_pos = [] 
    self.source_time = []
    self.source_peak_freq = []
    self.source_vel_time_function = [] 
    self.source_acc_time_function = []
                
    self.fx = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.fy = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.fz = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')

    self.fxTexId = glGenTextures(1)
    glActiveTexture(fx_texture_unit)
    glBindTexture(GL_TEXTURE_3D, self.fxTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.fx);

    self.fyTexId = glGenTextures(1)
    glActiveTexture(fy_texture_unit)
    glBindTexture(GL_TEXTURE_3D, self.fyTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.fy);

    self.fzTexId = glGenTextures(1)
    glActiveTexture(fz_texture_unit)    
    glBindTexture(GL_TEXTURE_3D, self.fzTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.fz);
  
    #self.setSource(sourceList)
  
  def setSource(self, sourceList):
    
    self.reset()
    self.setTimeFunction(sourceList)
    self.setBodyForcesFromSources(sourceList)
    
  def setTimeFunction(self, sourceList):
  
    self.source_vel_time_function = [] 
    self.source_acc_time_function = []
    self.source_time = []
    self.source_peak_freq = []
    
    for i in range(len(sourceList)):
    
      vel_time_function = np.zeros((self.sim_params.t_steps))
      acc_time_function = np.zeros((self.sim_params.t_steps))
      
      peak_freq = sourceList[i].peak_freq #total rupture time = 6 sigma, 3 sigma por cada lado
      source_time = sourceList[i].time
      
      sigma = 1.0/self.sim_params.max_frec#rupture_time/6.0
      
      #print("peak frec: ", peak_frec)
      #norm = ((np.sqrt(np.pi)*peak_freq)/(np.exp(-1)*2.0))/self.sim_params.dt
      norm = 1.0#(np.sqrt(np.pi)*peak_freq)/(np.exp(-1)*2.0)
      pi_freq_square = pow(np.pi*peak_freq,2.0)
      for step in range(self.sim_params.t_steps):
        time = self.sim_params.starttime + self.sim_params.dt*step
    
        timeDiff = time - source_time
        #ricker wavelet
        time_diff_square = pow(timeDiff,2)
        tm_vel = norm*(1.0-2.0*pi_freq_square*time_diff_square)*np.exp(-pi_freq_square*time_diff_square);
        #ricker wavelet time derivative
        tm = norm*(3-2*pi_freq_square*time_diff_square)*2.0*pi_freq_square*timeDiff*np.exp(-pi_freq_square*time_diff_square);
        #normal function
        #tm_vel = np.exp(-0.5*pow(timeDiff/sigma,2))#*(1.0/(sigma*np.sqrt(2*np.pi)))/self.sim_params.dt 
        #normal function time derivative (la potencia es 1 porque es la derivada de una gaussiana que integra a 1!!)
        #tm = (timeDiff/pow(sigma,2))*tm_vel
        
        vel_time_function[step] = tm_vel
        acc_time_function[step] = tm
                   
      self.source_vel_time_function.append(vel_time_function)
      self.source_acc_time_function.append(acc_time_function)
      self.source_time.append(source_time)
      self.source_peak_freq.append(peak_freq)
           
  def setBodyForcesFromSources(self, sourceList):
  
    self.bodyforcex = []
    self.bodyforcey = []
    self.bodyforcez = []
          
    self.source_pos = [] 
  
    for i in range(len(sourceList)):
    
      source = sourceList[i]
    
      forcex = np.zeros((3,3,2))
      forcey = np.zeros((3,2,3))
      forcez = np.zeros((2,3,3))
 
      source_pos = self.sim_params.latlondepth2simulation(source.lat, source.lon, source.depth)    
        
      # vx 
      #mxx    
      forcex[1,1,0] = -source.mxx/(self.sim_params.dxyz[0])
      forcex[1,1,1] =  source.mxx/(self.sim_params.dxyz[0])
    
      #print("bodyforcex_time ", self.bodyforcex_time[1,1,0]," ", self.bodyforcex_time[1,1,1])
    
      
      #segun graves
      forcex[1,0,0] = -source.mxy/(4*self.sim_params.dxyz[1])
      forcex[1,0,1] = -source.mxy/(4*self.sim_params.dxyz[1])    
      forcex[1,2,0] =  source.mxy/(4*self.sim_params.dxyz[1]) 
      forcex[1,2,1] =  source.mxy/(4*self.sim_params.dxyz[1])
    
      """ 
      #segun mi logica
      #mxy tendria que ser una rotacion en z, con fuerzas en direccion x y ejes +y y -y, entonces en +y va en direccion -x, segun regla de mano derecha
      forcex[1,0,0] =  source.mxy/(4*self.sim_params.dxyz[1])
      forcex[1,0,1] =  source.mxy/(4*self.sim_params.dxyz[1])    
      forcex[1,2,0] = -source.mxy/(4*self.sim_params.dxyz[1])  
      forcex[1,2,1] = -source.mxy/(4*self.sim_params.dxyz[1])    
      """
      
      #mxz
      forcex[0,1,0] = -source.mxz/(4*self.sim_params.dxyz[2])  
      forcex[0,1,1] = -source.mxz/(4*self.sim_params.dxyz[2])
      forcex[2,1,0] =  source.mxz/(4*self.sim_params.dxyz[2])
      forcex[2,1,1] =  source.mxz/(4*self.sim_params.dxyz[2])
      """
      forcex[0,1,0] =  source.mxz/(4*self.sim_params.dxyz[2])  
      forcex[0,1,1] =  source.mxz/(4*self.sim_params.dxyz[2])
      forcex[2,1,0] = -source.mxz/(4*self.sim_params.dxyz[2])
      forcex[2,1,1] = -source.mxz/(4*self.sim_params.dxyz[2])
      """
      # vy
      #myy
      forcey[1,0,1] = -source.myy/(self.sim_params.dxyz[1])
      forcey[1,1,1] =  source.myy/(self.sim_params.dxyz[1])
    
      
      #myx
      forcey[1,0,0] = -source.mxy/(4*self.sim_params.dxyz[0])
      forcey[1,1,0] = -source.mxy/(4*self.sim_params.dxyz[0]) 
      forcey[1,0,2] =  source.mxy/(4*self.sim_params.dxyz[0])
      forcey[1,1,2] =  source.mxy/(4*self.sim_params.dxyz[0])
      """
      forcey[1,0,0] =  source.mxy/(4*self.sim_params.dxyz[0])
      forcey[1,1,0] =  source.mxy/(4*self.sim_params.dxyz[0]) 
      forcey[1,0,2] = -source.mxy/(4*self.sim_params.dxyz[0])
      forcey[1,1,2] = -source.mxy/(4*self.sim_params.dxyz[0])
      """
      #myz
      
      #segun graves
      forcey[0,0,1] = -source.myz/(4*self.sim_params.dxyz[2])
      forcey[0,1,1] = -source.myz/(4*self.sim_params.dxyz[2])
      forcey[2,0,1] =  source.myz/(4*self.sim_params.dxyz[2])
      forcey[2,1,1] =  source.myz/(4*self.sim_params.dxyz[2])
    
      """
      #segun mi logica
      forcey[0,0,1] =  source.myz/(4*self.sim_params.dxyz[2])
      forcey[0,1,1] =  source.myz/(4*self.sim_params.dxyz[2])   
      forcey[2,0,1] = -source.myz/(4*self.sim_params.dxyz[2])
      forcey[2,1,1] = -source.myz/(4*self.sim_params.dxyz[2]) 
      """
      # vz 
      #mzz
      forcez[0,1,1] = -source.mzz/(self.sim_params.dxyz[2])
      forcez[1,1,1] =  source.mzz/(self.sim_params.dxyz[2])
    
      #mzx
      #segun graves
      
      forcez[0,1,0] = -source.mxz/(4*self.sim_params.dxyz[0])
      forcez[1,1,0] = -source.mxz/(4*self.sim_params.dxyz[0])
      forcez[0,1,2] =  source.mxz/(4*self.sim_params.dxyz[0])
      forcez[1,1,2] =  source.mxz/(4*self.sim_params.dxyz[0])
      """
      #segun mi logica
      forcez[0,1,0] =  source.mxz/(4*self.sim_params.dxyz[0])
      forcez[1,1,0] =  source.mxz/(4*self.sim_params.dxyz[0])  
      forcez[0,1,2] = -source.mxz/(4*self.sim_params.dxyz[0])
      forcez[1,1,2] = -source.mxz/(4*self.sim_params.dxyz[0]) 
      """
      
      #mzy
      forcez[0,0,1] = -source.myz/(4*self.sim_params.dxyz[1])
      forcez[1,0,1] = -source.myz/(4*self.sim_params.dxyz[1])
      forcez[0,2,1] =  source.myz/(4*self.sim_params.dxyz[1])
      forcez[1,2,1] =  source.myz/(4*self.sim_params.dxyz[1])
      """
      forcez[0,0,1] =  source.myz/(4*self.sim_params.dxyz[1])
      forcez[1,0,1] =  source.myz/(4*self.sim_params.dxyz[1])
      forcez[0,2,1] = -source.myz/(4*self.sim_params.dxyz[1])
      forcez[1,2,1] = -source.myz/(4*self.sim_params.dxyz[1])
      """
      #print("bodyforcex: ", self.bodyforcex)
    
      forcex = source.mt_scale*forcex/(self.sim_params.dxyz[0]*self.sim_params.dxyz[1]*self.sim_params.dxyz[2])
      forcey = source.mt_scale*forcey/(self.sim_params.dxyz[0]*self.sim_params.dxyz[1]*self.sim_params.dxyz[2])
      forcez = source.mt_scale*forcez/(self.sim_params.dxyz[0]*self.sim_params.dxyz[1]*self.sim_params.dxyz[2]) 
      
      self.bodyforcex.append(forcex)
      self.bodyforcey.append(forcey)
      self.bodyforcez.append(forcez)
      
      self.source_pos.append(source_pos)
                  
    #print("bodyforcex: ", self.bodyforcex)    
    
  def stepBodyForceTimeFunction(self, t_step):

    for i in range(len(self.source_pos)):
        
      datax = self.bodyforcex[i]*self.source_acc_time_function[i][t_step]
      datay = self.bodyforcey[i]*self.source_acc_time_function[i][t_step]
      dataz = self.bodyforcez[i]*self.source_acc_time_function[i][t_step]
 
      #print("datax")
      #print(datax)
 
      source_pos = self.source_pos[i]
      
      #maxi = np.amax(datax)
      #print("max: ", maxi)
      
      glActiveTexture(fx_texture_unit);
      glTexSubImage3D(GL_TEXTURE_3D, 0, source_pos[0]-1, source_pos[1]-1, source_pos[2]-1, 2, 3, 3, GL_RED, GL_FLOAT, datax) 
      glActiveTexture(fy_texture_unit);
      glTexSubImage3D(GL_TEXTURE_3D, 0, source_pos[0]-1, source_pos[1]-1, source_pos[2]-1, 3, 2, 3, GL_RED, GL_FLOAT, datay) 
      glActiveTexture(fz_texture_unit);
      glTexSubImage3D(GL_TEXTURE_3D, 0, source_pos[0]-1, source_pos[1]-1, source_pos[2]-1, 3, 3, 2, GL_RED, GL_FLOAT, dataz)   
    
  def reset(self):
  
    self.fx.fill(0)
    self.fy.fill(0)
    self.fz.fill(0)
  
    glActiveTexture(fx_texture_unit);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.fx);
    glActiveTexture(fy_texture_unit);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.fy);
    glActiveTexture(fz_texture_unit);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.fz);
