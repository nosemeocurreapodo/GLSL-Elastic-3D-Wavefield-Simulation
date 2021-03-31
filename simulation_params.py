import numpy as np                  # all matrix manipulations & OpenGL args
import obspy
import math

class simulation_params:
  
  def __init__(self, stationList, sourceList, max_medium_vel, min_medium_vel, mediumParamSize):
  
    #select simulation corners analizing the sources and the stations locations
    
    ini_corner = np.array([stationList[0].pos[0],stationList[0].pos[1],stationList[0].pos[2]])
    fin_corner = np.array([stationList[0].pos[0],stationList[0].pos[1],stationList[0].pos[2]])
      
    for s in stationList:

      if s.pos[0] < ini_corner[0]:
        ini_corner[0] = s.pos[0]
      if s.pos[1] < ini_corner[1]:
        ini_corner[1] = s.pos[1]  
      if s.pos[2] < ini_corner[2]:
        ini_corner[2] = s.pos[2]  
        
      if s.pos[0] > fin_corner[0]:
        fin_corner[0] = s.pos[0]
      if s.pos[1] > fin_corner[1]:
        fin_corner[1] = s.pos[1]  
      if s.pos[2] > fin_corner[2]:
        fin_corner[2] = s.pos[2] 
        
    for s in sourceList:

      if s.pos[0] < ini_corner[0]:
        ini_corner[0] = s.pos[0]
      if s.pos[1] < ini_corner[1]:
        ini_corner[1] = s.pos[1]  
      if s.pos[2] < ini_corner[2]:
        ini_corner[2] = s.pos[2] 
        
      if s.pos[0] > fin_corner[0]:
        fin_corner[0] = s.pos[0]
      if s.pos[1] > fin_corner[1]:
        fin_corner[1] = s.pos[1]  
      if s.pos[2] > fin_corner[2]:
        fin_corner[2] = s.pos[2] 
        
    diff = fin_corner - ini_corner
  
    ini_corner[0] -= diff[0]*0.20
    ini_corner[1] -= diff[1]*0.20
    ini_corner[2] -= diff[2]*0.20
    
    fin_corner[0] += diff[0]*0.20
    fin_corner[1] += diff[1]*0.20  
    fin_corner[2] += diff[2]*2.0 
  
    #calculate dx, dy and dz

    xlen = obspy.geodetics.base.gps2dist_azimuth(ini_corner[0], ini_corner[1], fin_corner[0], ini_corner[1])[0]
    ylen = obspy.geodetics.base.gps2dist_azimuth(ini_corner[0], ini_corner[1], ini_corner[0], fin_corner[1])[0]
    zlen = 120000#(xlen+ylen)*0.1# fin_corner[2] - ini_corner[2]
    
    print("x len: ", xlen, " ylen: ", ylen, " zlen: ", zlen)
    
    print("size of simulation (in m) ", xlen, ylen)
    
    sim_size = np.array([128,128,64])
    print("size of simulation (in steps) ", sim_size)
    dxyz = np.zeros(3)
    dxyz[0] = xlen/sim_size[0]
    dxyz[1] = ylen/sim_size[1]
    dxyz[2] = zlen/sim_size[2]

    print("simulation dx dy dz (cartesian): ", dxyz)
    
    #re calculate ini_corner and fin_corner
    
    self.surface = 0.25 
    
    ini_corner[2] = -dxyz[2]*sim_size[2]*self.surface
    fin_corner[2] = dxyz[2]*sim_size[2]*(1.0-self.surface)
     
    # la superficiel real, usada en la simulacion
    # justo en el medio del pixel de superficie de los parametros de lame
    #self.surface = self.surface + 0.5/mediumParamSize[2]    
    
    print("simulation initial coordinates: ", ini_corner)
    print("simulation final coordinates: ", fin_corner) 
    
    self.ini_corner = ini_corner
    self.fin_corner = fin_corner
  
    self.sim_size = sim_size
    self.dxyz = dxyz    
      
    max_dt = 0.495*np.amin(dxyz)/max_medium_vel
    print("max dt ", max_dt)
    
    aux = 1.0
    value = 1.0
    while(True):
      if(max_dt*aux > 5.0):
        value = 5.0
        break
      if(max_dt*aux > 1.0):
        value = 1.0
        break
      aux*=10.0
      
    #dt = math.trunc(max_dt*aux)/aux)
    dt = value/aux
    print("simulation dt: ", dt)
    
    max_frec = 0.04#min_medium_vel/(10.0*np.amax(dxyz))
    print("max medium frecuency ", max_frec) 
    
    self.max_frec = max_frec
    self.dt = dt