import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper

import obspy
from obspy.core import UTCDateTime

import numpy as np                  # all matrix manipulations & OpenGL args

import simulation_params

class simulation_source:
  def __init__(self, sim_params):
  
    self.sim_params = sim_params
    
    self.bodyforcex = np.zeros((3,3,2))
    self.bodyforcey = np.zeros((3,2,3))
    self.bodyforcez = np.zeros((2,3,3))

    self.source_pos_normalized = np.zeros((3)) 
    self.source_pos = np.zeros((3))    
    self.source_time = UTCDateTime(1000, 1, 1, 0, 0, 0)
    self.source_frec = 0.0
    
    self.velIni = np.zeros((sim_params.sim_size[2], sim_params.sim_size[1], sim_params.sim_size[0])).astype(np.float32)
    
    self.max_t_steps = 10000
    
    self.source_time_function = np.zeros((self.max_t_steps))
    
    self.fxTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE12)
    glBindTexture(GL_TEXTURE_3D, self.fxTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.velIni);

    self.fyTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE13)
    glBindTexture(GL_TEXTURE_3D, self.fyTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.velIni);

    self.fzTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE14)    
    glBindTexture(GL_TEXTURE_3D, self.fzTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], 0, GL_RED, GL_FLOAT, self.velIni);
        
  def stepBodyForceTimeFunction(self, t_step, time):

    timeDiff = time - self.source_time
    #ricker wavelet
    #tm = (1.0-2.0*pow(np.pi*self.source_frec*timeDiff,2))*np.exp(-pow(np.pi*self.source_frec*timeDiff,2));
    #ricker wavelet time derivative
    #tm = (-6.0*pow(np.pi*self.source_frec,2)*timeDiff+4.0*pow(np.pi*self.source_frec,4)*pow(timeDiff,3))*np.exp(-pow(np.pi*self.source_frec*timeDiff,2));
    #normal function
    alpha = 4.5
    #tm = np.exp(-0.5*pow(timeDiff*self.soure_frec*alpha,2));
    #normal function time derivative
    tm = -timeDiff*self.source_frec*alpha*np.exp(-0.5*pow(timeDiff*self.source_frec*alpha,2));
    
    """
    st = self.source_time[simlvl]*0.5
    tm = 0.0
    if timeDiff <= -st:
      tm = 0.0
    if timeDiff > -st and timeDiff <= 0.0:
      tm = ( st + timeDiff)/st;
      #tm = 2.0/self.source_time;
    if timeDiff > 0.0 and timeDiff <= st:
      tm = ( st - timeDiff)/st;
      #tm = -2.0/self.source_time;
    if timeDiff > st:
      tm = 0.0;
    """
    
    #print("source time ", self.source_time)
    #print("time ", time)
    #print("timeDiff ", timeDiff)
    #print("tm ", tm)
    #print("source_pos ", source_pos)
    
    self.source_time_function[t_step] = tm
   
    datax = self.bodyforcex*tm
    datay = self.bodyforcey*tm
    dataz = self.bodyforcez*tm

    glActiveTexture(GL_TEXTURE12);
    glTexSubImage3D(GL_TEXTURE_3D, 0, int(self.source_pos[0])-1, int(self.source_pos[1])-1, int(self.source_pos[2])-1, 2, 3, 3, GL_RED, GL_FLOAT, datax) 
    glActiveTexture(GL_TEXTURE13);
    glTexSubImage3D(GL_TEXTURE_3D, 0, int(self.source_pos[0])-1, int(self.source_pos[1])-1, int(self.source_pos[2])-1, 3, 2, 3, GL_RED, GL_FLOAT, datay) 
    glActiveTexture(GL_TEXTURE14);
    glTexSubImage3D(GL_TEXTURE_3D, 0, int(self.source_pos[0])-1, int(self.source_pos[1])-1, int(self.source_pos[2])-1, 3, 3, 2, GL_RED, GL_FLOAT, dataz)   
   
  def stepBodyForceTimeFunction_CPU(self, t_step, time):

    timeDiff = time - self.source_time
    #ricker wavelet
    #tm = (1.0-2.0*pow(np.pi*self.source_frec*timeDiff,2))*np.exp(-pow(np.pi*self.source_frec*timeDiff,2));
    #ricker wavelet time derivative
    #tm = (-6.0*pow(np.pi*self.source_frec,2)*timeDiff+4.0*pow(np.pi*self.source_frec,4)*pow(timeDiff,3))*np.exp(-pow(np.pi*self.source_frec*timeDiff,2));
    #normal function
    alpha = 4.5
    #tm = np.exp(-0.5*pow(timeDiff*self.soure_frec*alpha,2));
    #normal function time derivative
    tm = -timeDiff*self.source_frec*alpha*np.exp(-0.5*pow(timeDiff*self.source_frec*alpha,2));
    
    """
    st = self.source_time[simlvl]*0.5
    tm = 0.0
    if timeDiff <= -st:
      tm = 0.0
    if timeDiff > -st and timeDiff <= 0.0:
      tm = ( st + timeDiff)/st;
      #tm = 2.0/self.source_time;
    if timeDiff > 0.0 and timeDiff <= st:
      tm = ( st - timeDiff)/st;
      #tm = -2.0/self.source_time;
    if timeDiff > st:
      tm = 0.0;
    """
    
    #print("source time ", self.source_time)
    #print("time ", time)
    #print("timeDiff ", timeDiff)
    #print("tm ", tm)
    #print("source_pos ", source_pos)
    
    self.source_time_function[t_step] = tm
   
    datax = self.bodyforcex*tm
    datay = self.bodyforcey*tm
    dataz = self.bodyforcez*tm
    
    self.velx[int(self.source_pos[2])-1:int(self.source_pos[2])+2,int(self.source_pos[1])-1:int(self.source_pos[1])+2,int(self.source_pos[0])-1:int(self.source_pos[0])] = datax

    glActiveTexture(GL_TEXTURE12);
    glTexSubImage3D(GL_TEXTURE_3D, 0, int(self.source_pos[0])-1, int(self.source_pos[1])-1, int(self.source_pos[2])-1, 2, 3, 3, GL_RED, GL_FLOAT, datax) 
    glActiveTexture(GL_TEXTURE13);
    glTexSubImage3D(GL_TEXTURE_3D, 0, int(self.source_pos[0])-1, int(self.source_pos[1])-1, int(self.source_pos[2])-1, 3, 2, 3, GL_RED, GL_FLOAT, datay) 
    glActiveTexture(GL_TEXTURE14);
    glTexSubImage3D(GL_TEXTURE_3D, 0, int(self.source_pos[0])-1, int(self.source_pos[1])-1, int(self.source_pos[2])-1, 3, 3, 2, GL_RED, GL_FLOAT, dataz)   
    
    
  def setBodyForcesFromSource(self, source, source_frec):
  
    self.source_pos_normalized = (source.pos - self.sim_params.ini_corner)/(self.sim_params.fin_corner-self.sim_params.ini_corner)
    self.source_pos = np.array([self.source_pos_normalized[0]*self.sim_params.sim_size[0], self.source_pos_normalized[1]*self.sim_params.sim_size[1], self.source_pos_normalized[2]*self.sim_params.sim_size[2]]).astype(np.int32)

    #print("source.pos ", source.pos)  
    #print("source_pos normalized ", self.source_pos_normalized)
    #print("source_pos ", self.source_pos)    
  
    self.source_time = source.time
    self.source_frec = source_frec
     
    # vx 
    #mxx
    self.bodyforcex[1,1,0] = -source.mt[0]/self.sim_params.dxyz[0]
    self.bodyforcex[1,1,1] =  source.mt[0]/self.sim_params.dxyz[0]
    #mxy
    self.bodyforcex[1,0,0] = -source.mt[3]/(4*self.sim_params.dxyz[1])
    self.bodyforcex[1,0,1] = -source.mt[3]/(4*self.sim_params.dxyz[1])    
    self.bodyforcex[1,2,0] =  source.mt[3]/(4*self.sim_params.dxyz[1])  
    self.bodyforcex[1,2,1] =  source.mt[3]/(4*self.sim_params.dxyz[1])   
    #mxz
    self.bodyforcex[0,1,0] = -source.mt[4]/(4*self.sim_params.dxyz[2])  
    self.bodyforcex[0,1,1] = -source.mt[4]/(4*self.sim_params.dxyz[2])      
    self.bodyforcex[2,1,0] =  source.mt[4]/(4*self.sim_params.dxyz[2])  
    self.bodyforcex[2,1,1] =  source.mt[4]/(4*self.sim_params.dxyz[2])   

    # vy
    #myy
    self.bodyforcey[1,0,1] = -source.mt[1]/self.sim_params.dxyz[1]  
    self.bodyforcey[1,1,1] =  source.mt[1]/self.sim_params.dxyz[1]  
    #myx
    self.bodyforcey[1,0,0] = -source.mt[3]/(4*self.sim_params.dxyz[0])
    self.bodyforcey[1,1,0] = -source.mt[3]/(4*self.sim_params.dxyz[0])    
    self.bodyforcey[1,0,2] =  source.mt[3]/(4*self.sim_params.dxyz[0])
    self.bodyforcey[1,1,2] =  source.mt[3]/(4*self.sim_params.dxyz[0])
    #myz
    self.bodyforcey[0,0,1] = -source.mt[5]/(4*self.sim_params.dxyz[2])
    self.bodyforcey[0,1,1] = -source.mt[5]/(4*self.sim_params.dxyz[2])   
    self.bodyforcey[2,0,1] =  source.mt[5]/(4*self.sim_params.dxyz[2])
    self.bodyforcey[2,1,1] =  source.mt[5]/(4*self.sim_params.dxyz[2]) 

    # vz 
    #mzz
    self.bodyforcez[0,1,1] = -source.mt[2]/self.sim_params.dxyz[2]
    self.bodyforcez[1,1,1] =  source.mt[2]/self.sim_params.dxyz[2]
    #mzx
    self.bodyforcez[0,1,0] = -source.mt[4]/(4*self.sim_params.dxyz[0])
    self.bodyforcez[1,1,0] = -source.mt[4]/(4*self.sim_params.dxyz[0])  
    self.bodyforcez[0,1,2] =  source.mt[4]/(4*self.sim_params.dxyz[0])
    self.bodyforcez[1,1,2] =  source.mt[4]/(4*self.sim_params.dxyz[0]) 
    #mzy
    self.bodyforcez[0,0,1] = -source.mt[5]/(4*self.sim_params.dxyz[1])
    self.bodyforcez[1,0,1] = -source.mt[5]/(4*self.sim_params.dxyz[1])   
    self.bodyforcez[0,2,1] =  source.mt[5]/(4*self.sim_params.dxyz[1])
    self.bodyforcez[1,2,1] =  source.mt[5]/(4*self.sim_params.dxyz[1]) 
    
    self.bodyforcex = self.bodyforcex/(self.sim_params.dxyz[0]*self.sim_params.dxyz[1]*self.sim_params.dxyz[2])
    self.bodyforcey = self.bodyforcey/(self.sim_params.dxyz[0]*self.sim_params.dxyz[1]*self.sim_params.dxyz[2])
    self.bodyforcez = self.bodyforcez/(self.sim_params.dxyz[0]*self.sim_params.dxyz[1]*self.sim_params.dxyz[2])  
    
  def reset(self):
  
    self.bodyforcex.fill(0)
    self.bodyforcey.fill(0)
    self.bodyforcez.fill(0)
    
    glActiveTexture(GL_TEXTURE12);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.velIni);
    glActiveTexture(GL_TEXTURE13);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.velIni);
    glActiveTexture(GL_TEXTURE14);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], self.sim_params.sim_size[2], GL_RED, GL_FLOAT, self.velIni);