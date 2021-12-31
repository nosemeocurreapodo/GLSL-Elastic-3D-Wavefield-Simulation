import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper 

import numpy as np

import src.shader as shader

from src.opengl_helpers import *

class simulation_viewer_2D:
  def __init__(self, sim_params, stationList, sourceList, show_size):
      
    self.sim_params = sim_params  
    self.show_size = show_size

    # initialize GL by setting viewport and default render characteristics
    
    self.frame3DShader = shader.Shader("shaders/2D.vs","shaders/frameVel3D.fs")
  
    glUseProgram(self.frame3DShader.glid)
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velxTex"), velx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velyTex"), vely_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velzTex"), velz_texture_unit_number);     
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "rhoTex"), rho_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "lamTex"), lam_texture_unit_number);      
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "muTex"), mu_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "surfaceTex"), surface_texture_unit_number);
        
    #print(sim_reciever.rec_pos)
    #print(sim_source.source_pos_normalized)
    
    # triangle position buffer
    position = np.array(((-1.0, 1.0, 0.0, 1.0), (-1.0, -1.0, 0.0, 0.0), (1.0, -1.0, 1.0, 0.0), (-1.0, 1.0, 0.0, 1.0), (1.0, -1.0, 1.0, 0.0), (1.0, 1.0, 1.0, 1.0)), 'f')
    
    self.frame_VAO = glGenVertexArrays(1)  # create OpenGL vertex array id
    self.frame_VBO = glGenBuffers(1)  # create buffer for position attrib
    
    glBindVertexArray(self.frame_VAO)      # activate to receive state below
    glBindBuffer(GL_ARRAY_BUFFER, self.frame_VBO);
    glBufferData(GL_ARRAY_BUFFER, position, GL_STATIC_DRAW)
        
    #position attribute
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0*ctypes.sizeof(ctypes.c_float)));
    #texture coord attribute
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(2*ctypes.sizeof(ctypes.c_float)));

    # cleanup and unbind so no accidental subsequent state update
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    self.setStation(stationList)
    #self.setSource(sourceList)
  
  def setStation(self, stationList):
  
    station_pos_normalized = np.zeros((20,3))    
    for i in range(len(stationList)):
      station = stationList[i]
      station_pos_normalized[i,:] = self.sim_params.latlondepth2simulation_normalized(station.lat, station.lon, station.depth)
  
    glUseProgram(self.frame3DShader.glid)
    glUniform3fv(glGetUniformLocation(self.frame3DShader.glid, "recieverLoc"), 20, station_pos_normalized)
        
  def setSource(self, sourceList):
  
    source_pos_normalized = np.zeros((40,3))    
    for i in range(len(sourceList)):
      source = sourceList[i]
      source_pos_normalized[i,:] = self.sim_params.latlondepth2simulation_normalized(source.lat, source.lon, source.depth)
   
    glUseProgram(self.frame3DShader.glid)   
    glUniform3fv(glGetUniformLocation(self.frame3DShader.glid, "sourceLoc"), 40, source_pos_normalized);
    
  def draw(self):
      
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
      
    glViewport(0,0, self.show_size[0], self.show_size[1])
    
    glUseProgram(self.frame3DShader.glid)
        
    glBindVertexArray(self.frame_VAO)
    glDrawArrays(GL_TRIANGLES, 0, 6)
        
    #usuario: jdondo@gmail.com
    #password:larry1413 
