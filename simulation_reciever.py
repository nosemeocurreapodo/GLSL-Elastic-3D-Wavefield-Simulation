import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper
import numpy as np
import obspy

import shader
import simulation_params

class simulation_reciever:
  def __init__(self, recieverList, sim_params):
  
    self.sim_params = sim_params
    
    self.recieverList = recieverList
    
    self.max_records_num = 20
    self.max_t_steps = 10000
    
    self.rec_pos = np.zeros((self.max_records_num,3))
    for i in range(0,len(recieverList)):
      self.rec_pos[i,:] = (recieverList[i].pos - self.sim_params.ini_corner)/(self.sim_params.fin_corner-self.sim_params.ini_corner)
      self.rec_pos[i,2] = self.sim_params.surface + 0.5/self.sim_params.sim_size[2]#en el medio del pixel
    
    self.recieverRead = np.zeros((self.max_t_steps, 9*self.max_records_num)).astype(np.float32)
    
    self.recieverShader = shader.Shader("shaders/2D.vs","shaders/reciever.fs")
    
    glUseProgram(self.recieverShader.glid)
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "velxTex"), 0); 
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "velyTex"), 1);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "velzTex"), 2);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmaxxTex"), 3); 
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmaxyTex"), 4);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmaxzTex"), 5);   
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmayyTex"), 6); 
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmayzTex"), 7);
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "sigmazzTex"), 8); 
     
    glUniform1f(glGetUniformLocation(self.recieverShader.glid, "ox"), 1.0/self.sim_params.sim_size[0]); 
    glUniform1f(glGetUniformLocation(self.recieverShader.glid, "oy"), 1.0/self.sim_params.sim_size[1]); 
    glUniform1f(glGetUniformLocation(self.recieverShader.glid, "oz"), 1.0/self.sim_params.sim_size[2]);
    
    glUniform3fv(glGetUniformLocation(self.recieverShader.glid, "recieverLoc"), self.max_records_num, self.rec_pos); 
    
    zeroRecord = np.zeros((self.max_t_steps, 9*self.max_records_num)).astype(np.float32)
    
    self.recordDataTexId = glGenTextures(1)
    glActiveTexture(GL_TEXTURE17)
    glBindTexture(GL_TEXTURE_2D, self.recordDataTexId);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    #si inicializo con un buffer de diferente tamaño, la cosa no anda,no se porque
    glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, 9*self.max_records_num, self.max_t_steps, 0, GL_RED, GL_FLOAT, zeroRecord);
    #glGenerateMipmap(GL_TEXTURE_2D);
    
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
    
  def saveData(self, t_step):
  
    if(t_step > self.max_t_steps):
      print("trying to save too data num")
      print(t_step)
      print("not saving")
      return
  
    glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer);
      
    glViewport(0,0,9*self.max_records_num,self.max_t_steps)
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.recordDataTexId, 0);       
    drawbuffers=[GL_COLOR_ATTACHMENT0]
    glDrawBuffers(drawbuffers);
    
    glUseProgram(self.recieverShader.glid)
    glUniform1i(glGetUniformLocation(self.recieverShader.glid, "t_step"), t_step);
        
    glBindVertexArray(self.frame_VAO)
    glDrawArrays(GL_TRIANGLES, 0, 6)
     
  def getData(self, t_ini, t_steps):
  
    sim_str = []
         
    glActiveTexture(GL_TEXTURE17)
    glBindTexture(GL_TEXTURE_2D, self.recordDataTexId);
    glGetTexImage(GL_TEXTURE_2D,0, GL_RED, GL_FLOAT, self.recieverRead)
    
    for i in range(0,len(self.recieverList)):    
      sim_trs = []
      
      for t in range(0,3):
        #making stream in obspy format
        sim_tr = obspy.Trace()
        sim_tr.stats.delta = self.sim_params.dt
        sim_tr.stats.npts = t_steps
        sim_tr.stats.starttime = t_ini
        sim_tr.stats.network = self.recieverList[i].network
        sim_tr.stats.station = self.recieverList[i].name
        if t == 0:
          sim_tr.stats.channel = "n"
          sim_tr.data = -self.recieverRead[0:t_steps,0 + 9*i] #esta en metros
        if t == 1:
          sim_tr.stats.channel = "e" 
          sim_tr.data = -self.recieverRead[0:t_steps,1 + 9*i] #esta en metros
        if t == 2:
          sim_tr.stats.channel = "z"             
          sim_tr.data = self.recieverRead[0:t_steps,2 + 9*i] #esta en metros

          
        #print("trace: ", t, " last data: ", tracesData[r,t_steps-1,t])
        
        #tr.plot()
        sim_trs.append(sim_tr)
        
      sim_str.append(obspy.Stream(traces=[sim_trs[0],sim_trs[1],sim_trs[2]]))
        
    return sim_str
       

