import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper

import numpy as np                  # all matrix manipulations & OpenGL args

import simulation_params

class simulation_memory:
  def __init__(self, sim_params):
  
    self.sim_params = sim_params

    #init textures
    self.velx = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.vely = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.velz = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')

    self.sigmaxx = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.sigmayy = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.sigmazz = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.sigmaxy = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')    
    self.sigmaxz = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    self.sigmayz = np.zeros((self.sim_params.sim_size[2], self.sim_params.sim_size[1], self.sim_params.sim_size[0]), dtype='float32')
    
    self.velxTexId = glGenTextures(1)   
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_3D, self.velxTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.velx);

    self.velyTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE1)    
    glBindTexture(GL_TEXTURE_3D, self.velyTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.vely);


    self.velzTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE2)    
    glBindTexture(GL_TEXTURE_3D, self.velzTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.velz);

    
    self.sigmaxxTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE3)    
    glBindTexture(GL_TEXTURE_3D, self.sigmaxxTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.sigmaxx);


    self.sigmaxyTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE4)    
    glBindTexture(GL_TEXTURE_3D, self.sigmaxyTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.sigmaxy);


    self.sigmaxzTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE5)    
    glBindTexture(GL_TEXTURE_3D, self.sigmaxzTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.sigmaxz);

      
    self.sigmayyTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE6)    
    glBindTexture(GL_TEXTURE_3D, self.sigmayyTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.sigmayy);


    self.sigmayzTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE7)    
    glBindTexture(GL_TEXTURE_3D, self.sigmayzTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.sigmayz);


    self.sigmazzTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE8)    
    glBindTexture(GL_TEXTURE_3D, self.sigmazzTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.sigmazz);
     
  def reset(self):
  
    self.velx.fill(0)
    self.vely.fill(0)
    self.velz.fill(0)
    
    self.sigmaxx.fill(0)
    self.sigmayy.fill(0)
    self.sigmazz.fill(0)
    self.sigmaxy.fill(0)
    self.sigmaxz.fill(0)
    self.sigmayz.fill(0)
    
    #v
    glActiveTexture(GL_TEXTURE0);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.velx);
    glActiveTexture(GL_TEXTURE1);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.vely);
    glActiveTexture(GL_TEXTURE2);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.velz);
    #sigma
    glActiveTexture(GL_TEXTURE3);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.sigmaxx);
    glActiveTexture(GL_TEXTURE4);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.sigmaxy);
    glActiveTexture(GL_TEXTURE5);    
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.sigmaxz);
    glActiveTexture(GL_TEXTURE6);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.sigmayy);
    glActiveTexture(GL_TEXTURE7);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.sigmayz);
    glActiveTexture(GL_TEXTURE8);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.sigmazz);
