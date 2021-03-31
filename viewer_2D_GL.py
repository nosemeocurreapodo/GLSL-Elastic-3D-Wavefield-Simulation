import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper 
import numpy as np

import shader

class simulation_viewer_2D:
  def __init__(self, sim_params, sim_reciever, show_size):
  
    self.show_size = show_size
    
    self.frame3DShader = shader.Shader("shaders/2D.vs","shaders/frameVel3D.fs")
  
    glUseProgram(self.frame3DShader.glid)
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velxTex"), 0); 
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velyTex"), 1);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velzTex"), 2);     
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "invRhoTex"), 9);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "lamTex"), 10);      
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "muTex"), 11); 
    
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "width"), sim_params.sim_size[0]); 
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "height"), sim_params.sim_size[1]); 
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "depth"), sim_params.sim_size[2]);
    
    glUniform3fv(glGetUniformLocation(self.frame3DShader.glid, "recieverLoc"), sim_reciever.max_records_num, sim_reciever.rec_pos); 
    
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
    
  def setSource(self, sim_source):
    glUniform3fv(glGetUniformLocation(self.frame3DShader.glid, "sourceLoc"), 1, sim_source.source_pos_normalized);
    
  def draw(self):
      
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
      
    glViewport(0,0, self.show_size[0], self.show_size[1])
    
    glUseProgram(self.frame3DShader.glid)
        
    glBindVertexArray(self.frame_VAO)
    glDrawArrays(GL_TRIANGLES, 0, 6)
        
    #usuario: jdondo@gmail.com
    #password:larry1413 