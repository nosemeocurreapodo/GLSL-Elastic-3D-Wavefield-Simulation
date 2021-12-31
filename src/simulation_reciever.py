import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper
import numpy as np
import obspy

import src.shader as shader
import src.simulation_params as simulation_params
from src.opengl_helpers import *

class simulation_reciever:
  def __init__(self, sim_params, recieverList):
  
    self.sim_params = sim_params
    self.recieverList = recieverList
    
    self.max_t_steps = 10000
    self.max_reciever_num = 20
    
    self.rec_t_step = 0
    
    self.rec_pos_normalized = np.zeros((self.max_reciever_num,3)) 
    self.rec_name = []
    
    for i in range(0,len(recieverList)):
      reciever = recieverList[i]
      self.rec_pos_normalized[i,:] = sim_params.latlondepth2simulation_normalized(reciever.lat, reciever.lon, reciever.depth)
      self.rec_name.append(reciever.name)
    
    self.recieverData = np.zeros((self.max_t_steps, 9*self.max_reciever_num)).astype(np.float32)
    
    self.recieverDataTexId = glGenTextures(1)
    
    glActiveTexture(reciever_texture_unit)
    glBindTexture(GL_TEXTURE_2D, self.recieverDataTexId);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, 9*self.max_reciever_num, self.max_t_steps, 0, GL_RED, GL_FLOAT, self.recieverData);
    #glGenerateMipmap(GL_TEXTURE_2D); 
    
    self.recieverShader = shader.Shader("shaders/2D.vs","shaders/reciever.fs")
    
    glUseProgram(self.recieverShader.glid)
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "velxTex"), velx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "velyTex"), vely_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "velzTex"), velz_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmaxxTex"), sigmaxx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmaxyTex"), sigmaxy_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmaxzTex"), sigmaxz_texture_unit_number);   
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmayyTex"), sigmayy_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmayzTex"), sigmayz_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmazzTex"), sigmazz_texture_unit_number); 
    
    glUniform3fv(glGetUniformLocation(self.recieverShader.glid, "recieverLoc"), self.max_reciever_num, self.rec_pos_normalized); 
        
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
    
    self.frameBuffer = glGenFramebuffers(1);
    glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer);
  
    
  def reset(self):
    self.rec_t_step = 0
    
  def saveData(self, t_step):
  
    if(t_step % self.sim_params.decimation_factor != 0):
      return    
      
    if(self.rec_t_step > self.max_t_steps):
      print("trying to save too many data")
      print(t_step)
      print("not saving")
      return
  
    glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer);
      
    glViewport(0,0,9*self.max_reciever_num,self.max_t_steps)
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.recieverDataTexId, 0);       
    drawbuffers=[GL_COLOR_ATTACHMENT0]
    glDrawBuffers(drawbuffers);
    
    glUseProgram(self.recieverShader.glid)
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "t_step"), self.rec_t_step);
        
    glBindVertexArray(self.frame_VAO)
    glDrawArrays(GL_TRIANGLES, 0, 6)
    
    self.rec_t_step += 1
     
  def getData(self, starttime):
         
    glActiveTexture(reciever_texture_unit)
    #glBindTexture(GL_TEXTURE_2D, self.recordDataTexId);
    glGetTexImage(GL_TEXTURE_2D,0, GL_RED, GL_FLOAT, self.recieverData)
                   
    sim_strs = []  
    for i in range(0,len(self.rec_name)):    
      
      sim_trs = []
      for t in range(0,3):
        #making stream in obspy format
        sim_tr = obspy.Trace()
        sim_tr.stats.delta = self.sim_params.rec_dt
        sim_tr.stats.npts = self.rec_t_step
        sim_tr.stats.starttime = starttime
        sim_tr.stats.network = "SIM"#self.recieverList[i].network
        sim_tr.stats.station = self.rec_name[i]
        if t == 0:
          sim_tr.stats.channel = "n"
          sim_tr.data = self.recieverData[0:self.rec_t_step,0 + 9*i] #esta en metros
        if t == 1:
          sim_tr.stats.channel = "e" 
          sim_tr.data = self.recieverData[0:self.rec_t_step,1 + 9*i] 
        if t == 2:
          sim_tr.stats.channel = "z"             
          sim_tr.data = -self.recieverData[0:self.rec_t_step,2 + 9*i] 

        sim_trs.append(sim_tr)
        
      sim_strs.append(obspy.Stream(traces=[sim_trs[0],sim_trs[1],sim_trs[2]]))

    return sim_strs
       

