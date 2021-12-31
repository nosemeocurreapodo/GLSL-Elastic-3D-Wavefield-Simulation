import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args


from src.opengl_helpers import *

class simulation_surface:

  def __init__(self, sim_params, stationList):
  
    self.sim_params = sim_params
    self.surface = np.zeros((sim_params.sim_size[1],sim_params.sim_size[0]), dtype='float32')
    
    self.surfaceTexId = glGenTextures(1);
    glActiveTexture(surface_texture_unit)
    glBindTexture(GL_TEXTURE_2D, self.surfaceTexId);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    #print(invRho.shape)
    #print(invRho.shape[0])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, sim_params.sim_size[0], sim_params.sim_size[1], 0, GL_RED, GL_FLOAT, self.surface);
    #glGenerateMipmap(GL_TEXTURE_3D);   
    
    self.setSurfaceFromStations(sim_params, stationList)

    
  def setSurfaceFromStations(self, sim_params, stationList):
 
    for x in range(0, self.sim_params.sim_size[0]):
      for y in range(0, self.sim_params.sim_size[1]):
        depth = 0
        normfact = 0.0
        for station in stationList:
          station_pos = sim_params.latlondepth2simulation(station.lat, station.lon, station.depth)                                      
          diff = np.array([x,y]) - station_pos[0:2]
          dist = np.sqrt(diff[0]**2+diff[1]**2)
          if dist == 0.0:
            depth = station_pos[2]
            normfact = 1.0
            break
          depth += station_pos[2]/dist
          normfact += 1.0/dist
        
        depth = (depth/normfact)
        #print("depth ", depth)
        self.surface[y,x] = depth/self.sim_params.sim_size[2] - 1.0/self.sim_params.sim_size[2]        
        
    glActiveTexture(surface_texture_unit)
    #glBindTexture(GL_TEXTURE_2D, self.surfaceTexId);
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.sim_params.sim_size[0], self.sim_params.sim_size[1], GL_RED, GL_FLOAT, self.surface) 
  
