import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper

import numpy as np                  # all matrix manipulations & OpenGL args

import src.shaderGeom as shaderGeom
import src.simulation_params as simulation_params
import src.wavefield_memory as wavefield_memory
import src.medium_memory as medium_memory
from src.opengl_helpers import *


class simulation_step:
  def __init__(self, sim_params, wavefield_memory):
  
    self.sim_params = sim_params
    self.wave_memory = wavefield_memory
    
    #init shaders
    self.elasticVelShader = shaderGeom.Shader("shaders/elastic3D.vs","shaders/elastic3D.gs","shaders/elasticVel3D.fs")
    
    glUseProgram(self.elasticVelShader.glid)
    
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "sigmaxxTex"), sigmaxx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "sigmaxyTex"), sigmaxy_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "sigmaxzTex"), sigmaxz_texture_unit_number);   
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "sigmayyTex"), sigmayy_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "sigmayzTex"), sigmayz_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "sigmazzTex"), sigmazz_texture_unit_number);       
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "rhoTex"), rho_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "fxTex"), fx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "fyTex"), fy_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "fzTex"), fz_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "surfaceTex"), surface_texture_unit_number);
    
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "dx"), self.sim_params.dxyz[0]);
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "dy"), self.sim_params.dxyz[1]); 
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "dz"), self.sim_params.dxyz[2]);     
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "dt"), self.sim_params.dt); 
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "ox"), 1.0/self.sim_params.sim_size[0]); 
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "oy"), 1.0/self.sim_params.sim_size[1]); 
    glUniform1f(glGetUniformLocation(self.elasticVelShader.glid, "oz"), 1.0/self.sim_params.sim_size[2]);
    
    glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "layer"), -1); 
    
    
    self.elasticVelTaperShader = shaderGeom.Shader("shaders/elastic3D.vs","shaders/elastic3D.gs","shaders/elasticVelTaper.fs")
    
    glUseProgram(self.elasticVelTaperShader.glid)
    
    glUniform1f(glGetUniformLocation(self.elasticVelTaperShader.glid, "ox"), 1.0/self.sim_params.sim_size[0]); 
    glUniform1f(glGetUniformLocation(self.elasticVelTaperShader.glid, "oy"), 1.0/self.sim_params.sim_size[1]); 
    glUniform1f(glGetUniformLocation(self.elasticVelTaperShader.glid, "oz"), 1.0/self.sim_params.sim_size[2]);
    glUniform1i(glGetUniformLocation(self.elasticVelTaperShader.glid, "layer"), -1);
    
    self.elasticSigmaShader = shaderGeom.Shader("shaders/elastic3D.vs","shaders/elastic3D.gs","shaders/elasticSigma3D.fs")

    glUseProgram(self.elasticSigmaShader.glid)
    
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "velxTex"), velx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "velyTex"), vely_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "velzTex"), velz_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "lamTex"), lam_texture_unit_number);      
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "muTex"), mu_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "surfaceTex"), surface_texture_unit_number);
    
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "dx"), self.sim_params.dxyz[0]);
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "dy"), self.sim_params.dxyz[1]); 
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "dz"), self.sim_params.dxyz[2]);     
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "dt"), self.sim_params.dt); 
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "ox"), 1.0/self.sim_params.sim_size[0]); 
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "oy"), 1.0/self.sim_params.sim_size[1]); 
    glUniform1f(glGetUniformLocation(self.elasticSigmaShader.glid, "oz"), 1.0/self.sim_params.sim_size[2]);
    glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "layer"), -1);   
    
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
    #self.frameRbo = glGenRenderbuffers(1);
    #glBindRenderbuffer(GL_RENDERBUFFER, self.frameRbo);
    #glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.steps[0], self.steps[1]); 
    #glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.frameRbo); 
    #glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, self.steps[0], self.steps[1]); 
    #glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, self.frameRbo); 
   
  def step(self):
    
    glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer);
        
    glEnable(GL_BLEND);  
    glViewport(0,0,self.sim_params.sim_size[0],self.sim_params.sim_size[1])   
    
    #update vel
    glBlendEquation(GL_FUNC_ADD);
    glBlendFunc(GL_ONE, GL_ONE);
       
    #glFramebufferTexture3D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_3D, self.velTexId[dst], 0, 0); 
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.wave_memory.velxTexId, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, self.wave_memory.velyTexId, 0);  
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2, self.wave_memory.velzTexId, 0);      
    drawbuffers=[GL_COLOR_ATTACHMENT0,GL_COLOR_ATTACHMENT1,GL_COLOR_ATTACHMENT2]
    glDrawBuffers(drawbuffers);
    
    glUseProgram(self.elasticVelShader.glid)    
    glBindVertexArray(self.frame_VAO)
    glDrawArraysInstanced(GL_TRIANGLES, 0, 6, self.sim_params.sim_size[2]);  
    #for layer in range(0, self.sim_size[simlvl][2]):
    #  glUniform1i(glGetUniformLocation(self.elasticVelShader.glid, "layer"), layer);
    #  glDrawArrays(GL_TRIANGLES, 0, 6)      
    
    
    #apply tapper
    glBlendEquation(GL_FUNC_ADD);
    glBlendFunc(GL_ZERO, GL_ONE_MINUS_SRC_COLOR);
    
    glUseProgram(self.elasticVelTaperShader.glid)
    glBindVertexArray(self.frame_VAO)
    glDrawArraysInstanced(GL_TRIANGLES, 0, 6, self.sim_params.sim_size[2]);  
    #for layer in range(0, self.sim_size[simlvl][2]):
    #  glUniform1i(glGetUniformLocation(self.elasticVelTaperShader.glid, "layer"), layer);
    #  glDrawArrays(GL_TRIANGLES, 0, 6)  
    
    
    # update sigma
    glBlendEquation(GL_FUNC_ADD);
    glBlendFunc(GL_ONE, GL_ONE); 
    
    
    #glBindFramebuffer(GL_FRAMEBUFFER, self.frameBuffer);    
    #glFramebufferTexture3D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_3D, self.velTexId[dst], 0, 0); 
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, self.wave_memory.sigmaxxTexId, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, self.wave_memory.sigmaxyTexId, 0);  
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2, self.wave_memory.sigmaxzTexId, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT3, self.wave_memory.sigmayyTexId, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT4, self.wave_memory.sigmayzTexId, 0);  
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT5, self.wave_memory.sigmazzTexId, 0);      
    drawbuffers=[GL_COLOR_ATTACHMENT0,GL_COLOR_ATTACHMENT1,GL_COLOR_ATTACHMENT2,GL_COLOR_ATTACHMENT3,GL_COLOR_ATTACHMENT4,GL_COLOR_ATTACHMENT5]
    glDrawBuffers(drawbuffers);
    
    
    glUseProgram(self.elasticSigmaShader.glid) 
    glBindVertexArray(self.frame_VAO)
    glDrawArraysInstanced(GL_TRIANGLES, 0, 6, self.sim_params.sim_size[2]);
    #for layer in range(0, self.sim_size[simlvl][2]):
    #  glUniform1i(glGetUniformLocation(self.elasticSigmaShader.glid, "layer"), layer);
    #  glDrawArrays(GL_TRIANGLES, 0, 6)
    
       
    #remove texture attachments to prevent errors
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, 0, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, 0, 0);  
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2, 0, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT3, 0, 0);
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT4, 0, 0);  
    glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT5, 0, 0); 
    
    glDisable(GL_BLEND);
     
  def step_CPU(self):
    
    c1 = 9.0/8.0
    c2 = -1.0/24.0
    """
    size = 1000
    mean = np.zeros(size)
    cova = np.identity(mean.shape[0])*0.001
    sample = np.random.multivariate_normal(mean, cova)
    """
    
    #self.sim_memory.velx[2:-2,2:-2,2:-2] += c1*(np.subtract(self.sim_memory.sigmaxx[2:-2,2:-2,3:-1],self.sim_memory.sigmaxx[2:-2,2:-2,2:-2]))
    
    
    
    self.sim_memory.velx[:,:,2:-2] += (c1*(self.sim_memory.sigmaxx[:,:,3:-1] - self.sim_memory.sigmaxx[:,:,2:-2]) + c2*(self.sim_memory.sigmaxx[:,:,4:  ] - self.sim_memory.sigmaxx[:,:,1:-3]))/self.sim_params.dxyz[0]   
    self.sim_memory.velx[:,2:-2,:] += (c1*(self.sim_memory.sigmaxy[:,2:-2,:] - self.sim_memory.sigmaxy[:,1:-3,:]) + c2*(self.sim_memory.sigmaxy[:,3:-1,:] - self.sim_memory.sigmaxy[:,0:-4,:]))/self.sim_params.dxyz[1]
    self.sim_memory.velx[2:-2,:,:] += (c1*(self.sim_memory.sigmaxz[2:-2,:,:] - self.sim_memory.sigmaxz[1:-3,:,:]) + c2*(self.sim_memory.sigmaxz[3:-1,:,:] - self.sim_memory.sigmaxz[0:-4,:,:]))/self.sim_params.dxyz[2]
    
    self.sim_memory.vely[:,2:-2,:] += (c1*(self.sim_memory.sigmayy[:,3:-1,:] - self.sim_memory.sigmayy[:,2:-2,:]) + c2*(self.sim_memory.sigmayy[:,4:,:  ] - self.sim_memory.sigmayy[:,1:-3,:]))/self.sim_params.dxyz[1]
    self.sim_memory.vely[:,:,2:-2] += (c1*(self.sim_memory.sigmaxy[:,:,2:-2] - self.sim_memory.sigmaxy[:,:,1:-3]) + c2*(self.sim_memory.sigmaxy[:,:,3:-1] - self.sim_memory.sigmaxy[:,:,0:-4]))/self.sim_params.dxyz[0]
    self.sim_memory.vely[2:-2,:,:] += (c1*(self.sim_memory.sigmayz[2:-2,:,:] - self.sim_memory.sigmayz[1:-3,:,:]) + c2*(self.sim_memory.sigmayz[3:-1,:,:] - self.sim_memory.sigmayz[0:-4,:,:]))/self.sim_params.dxyz[2]
    
    self.sim_memory.velz[2:-2,:,:] += (c1*(self.sim_memory.sigmazz[3:-1,:,:] - self.sim_memory.sigmazz[2:-2,:,:]) + c2*(self.sim_memory.sigmazz[4:,:,:  ] - self.sim_memory.sigmazz[1:-3,:,:]))/self.sim_params.dxyz[2]
    self.sim_memory.velz[:,2:-2,:] += (c1*(self.sim_memory.sigmayz[:,2:-2,:] - self.sim_memory.sigmayz[:,1:-3,:]) + c2*(self.sim_memory.sigmayz[:,3:-1,:] - self.sim_memory.sigmayz[:,0:-4,:]))/self.sim_params.dxyz[1]
    self.sim_memory.velz[:,:,2:-2] += (c1*(self.sim_memory.sigmaxz[:,:,2:-2] - self.sim_memory.sigmaxz[:,:,1:-3]) + c2*(self.sim_memory.sigmaxz[:,:,3:-1] - self.sim_memory.sigmaxz[:,:,0:-4]))/self.sim_params.dxyz[0]
    
    
    d_velx_dx = c1*(self.sim_memory.velx[:,:,2:-2] - self.sim_memory.velx[:,:,1:-3]) + c2*(self.sim_memory.velx[:,:,3:-1] - self.sim_memory.velx[:,:,0:-4])/self.sim_params.dxyz[0]
    d_vely_dy = c1*(self.sim_memory.vely[:,2:-2,:] - self.sim_memory.vely[:,1:-3,:]) + c2*(self.sim_memory.vely[:,3:-1,:] - self.sim_memory.vely[:,0:-4,:])/self.sim_params.dxyz[1]
    d_velz_dz = c1*(self.sim_memory.velz[2:-2,:,:] - self.sim_memory.velz[1:-3,:,:]) + c2*(self.sim_memory.velz[3:-1,:,:] - self.sim_memory.velz[0:-4,:,:])/self.sim_params.dxyz[2]
    
    d_vely_dx = (c1*(self.sim_memory.vely[:,:,3:-1] - self.sim_memory.vely[:,:,2:-2]) + c2*(self.sim_memory.vely[:,:,4:  ] - self.sim_memory.vely[:,:,1:-3]))/self.sim_params.dxyz[0]
    d_velx_dy = (c1*(self.sim_memory.velx[:,3:-1,:] - self.sim_memory.velx[:,2:-2,:]) + c2*(self.sim_memory.velx[:,4:,:  ] - self.sim_memory.velx[:,1:-3,:]))/self.sim_params.dxyz[1]
    
    d_velx_dz = (c1*(self.sim_memory.velx[3:-1,:,:] - self.sim_memory.velx[2:-2,:,:]) + c2*(self.sim_memory.velx[4:,:,:  ] - self.sim_memory.velx[1:-3,:,:]))/self.sim_params.dxyz[2]
    d_velz_dx = (c1*(self.sim_memory.velz[:,:,3:-1] - self.sim_memory.velz[:,:,2:-2]) + c2*(self.sim_memory.velz[:,:,4:  ] - self.sim_memory.velz[:,:,1:-3]))/self.sim_params.dxyz[0]
    
    d_vely_dz =(c1*(self.sim_memory.vely[3:-1,:,:] - self.sim_memory.vely[2:-2,:,:]) + c2*(self.sim_memory.vely[4:,:,:  ] - self.sim_memory.vely[1:-3,:,:]))/self.sim_params.dxyz[2]
    d_velz_dy = (c1*(self.sim_memory.velz[:,3:-1,:] - self.sim_memory.velz[:,2:-2,:]) + c2*(self.sim_memory.velz[:,4:,:  ] - self.sim_memory.velz[:,1:-3,:]))/self.sim_params.dxyz[1]
    
    self.sim_memory.sigmaxx[:,:,2:-2] += d_velx_dx
    self.sim_memory.sigmaxx[:,2:-2,:] += d_vely_dy
    self.sim_memory.sigmaxx[2:-2,:,:] += d_velz_dz
    
    self.sim_memory.sigmayy[:,:,2:-2] += d_velx_dx
    self.sim_memory.sigmayy[:,2:-2,:] += d_vely_dy
    self.sim_memory.sigmaxx[2:-2,:,:] += d_velz_dz
    
    self.sim_memory.sigmazz[:,:,2:-2] += d_velx_dx
    self.sim_memory.sigmazz[:,2:-2,:] += d_vely_dy
    self.sim_memory.sigmazz[2:-2,:,:] += d_velz_dz
    
    self.sim_memory.sigmaxy[:,2:-2,:] += d_velx_dy
    self.sim_memory.sigmaxy[:,:,2:-2] += d_vely_dx
    
    self.sim_memory.sigmaxz[:,:,2:-2] += d_velz_dx
    self.sim_memory.sigmaxz[2:-2,:,:] += d_velx_dz 

    self.sim_memory.sigmayz[:,2:-2,:] += d_velz_dy
    self.sim_memory.sigmayz[2:-2,:,:] += d_vely_dz      
    
