import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper

import numpy as np                  # all matrix manipulations & OpenGL args

import src.simulation_params as simulation_params

from src.opengl_helpers import *

class medium_memory:
  def __init__(self, sim_params):
  
    self.sim_params = sim_params
    
    self.rho = np.zeros((self.sim_params.med_size[2],self.sim_params.med_size[1],self.sim_params.med_size[0]), dtype='float32')
    self.lam = np.zeros((self.sim_params.med_size[2],self.sim_params.med_size[1],self.sim_params.med_size[0]), dtype='float32')
    self.mu = np.zeros((self.sim_params.med_size[2],self.sim_params.med_size[1],self.sim_params.med_size[0]), dtype='float32')
    
    self.rhoTexId = glGenTextures(1);
    glActiveTexture(rho_texture_unit)
    glBindTexture(GL_TEXTURE_3D, self.rhoTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #print(invRho.shape)
    #print(invRho.shape[0])
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], 0, GL_RED, GL_FLOAT, self.rho);
    #glGenerateMipmap(GL_TEXTURE_3D);

    self.lamTexId = glGenTextures(1);
    glActiveTexture(lam_texture_unit)
    glBindTexture(GL_TEXTURE_3D, self.lamTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], 0, GL_RED, GL_FLOAT, self.lam);
    #glGenerateMipmap(GL_TEXTURE_3D);

    self.muTexId = glGenTextures(1);
    glActiveTexture(mu_texture_unit)
    glBindTexture(GL_TEXTURE_3D, self.muTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], 0, GL_RED, GL_FLOAT, self.mu);
    #glGenerateMipmap(GL_TEXTURE_3D);
    
            
  def setWithLameParams(self, rho, lam, mu):
  
    self.rho = rho
    self.lam = lam
    self.mu = mu
  
    glActiveTexture(rho_texture_unit)
    #glBindTexture(GL_TEXTURE_3D, self.rhoTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], GL_RED, GL_FLOAT, rho) 
    
    glActiveTexture(lam_texture_unit)
    #glBindTexture(GL_TEXTURE_3D, self.lamTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], GL_RED, GL_FLOAT, lam) 

    glActiveTexture(mu_texture_unit)
    #glBindTexture(GL_TEXTURE_3D, self.muTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], GL_RED, GL_FLOAT, mu) 
    
    
  def setWithVelTable(self, veltable):
      
    vp =  np.zeros((self.sim_params.med_size[2],self.sim_params.med_size[1],self.sim_params.med_size[0]), dtype='float32')
    vs =  np.zeros((self.sim_params.med_size[2],self.sim_params.med_size[1],self.sim_params.med_size[0]), dtype='float32')
    rho =  np.zeros((self.sim_params.med_size[2],self.sim_params.med_size[1],self.sim_params.med_size[0]), dtype='float32')        
    
    #print("veltable: ")
    #print(veltable)
      
    for z in range(0,self.sim_params.med_size[2]):
      for y in range(0,self.sim_params.med_size[1]):
        for x in range(0, self.sim_params.med_size[0]):
    
          sim = np.array([x+0.5,y+0.5,z+0.5])/self.sim_params.med_size
          sim = sim*self.sim_params.sim_size*self.sim_params.dxyz
          
          med_step = (self.sim_params.sim_size/self.sim_params.med_size)*self.sim_params.dxyz
          med_step_length = np.amin(med_step)#np.sqrt(med_step[0]**2+med_step[1]**2+med_step[2]**2)

          #print("sim: ", sim)
          #print("med_step: ", med_step)
          #print("med_step_length: ", med_step_length)

          #print("depth: ", depth)
  
          best_vp = 0.0
          best_vs = 0.0
          best_rho = 0.0
          best_diff = 10000000000000000000000.0
          best_num = 0
    
          for layer in veltable:
            lat_veltable = layer[0]
            lon_veltable = layer[1]
            depth_veltable = layer[2]
            
            table = self.sim_params.latlondepth2meters(lat_veltable, lon_veltable, depth_veltable)
            
            diff = table - sim
            diff_length = np.sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)
            
            #print("table: ", table)
            #print("diff: ", diff)
            #print("diff_length: ", diff_length)
            
            #print("depth veltable: ", depth_veltable)
            """
            if diff_length < med_step_length:
              best_vp += layer[3]
              best_vs += layer[4]
              best_rho += layer[5]
              best_diff = diff_length
              best_num += 1
              #print("prom: ", best_num)
            """  
            #if best_diff > med_step_length and diff_length < best_diff:
            if diff_length < best_diff:
              best_vp = layer[3]
              best_vs = layer[4]
              best_rho = layer[5]
              best_diff = diff_length
              best_num = 1              
              #print("no prom: ")        
          #print("x: ", x," y: ",y," z: ",z, " depth: ", depth, " vp: ", vp_, " vs: ", vs_, " rho: ", rho_)      
            
          vp[z,y,x] = best_vp/best_num
          vs[z,y,x] = best_vs/best_num
          rho[z,y,x] = best_rho/best_num

    self.lam = rho*((vp*vp) - 2.0*(vs*vs))
    self.mu = ((vs*vs)*rho)
    self.rho = rho
    
    #print("lam:")
    #print(self.lam)
    #print("mu:")
    #print(self.mu)
    #print("rho:")
    #print(self.rho)
    
    glActiveTexture(rho_texture_unit)
    #glBindTexture(GL_TEXTURE_3D, self.rhoTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], GL_RED, GL_FLOAT, self.rho) 
    
    glActiveTexture(lam_texture_unit)
    #glBindTexture(GL_TEXTURE_3D, self.lamTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], GL_RED, GL_FLOAT, self.lam) 

    glActiveTexture(mu_texture_unit)
    #glBindTexture(GL_TEXTURE_3D, self.muTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.med_size[0], self.sim_params.med_size[1], self.sim_params.med_size[2], GL_RED, GL_FLOAT, self.mu) 
