# Python built-in modules
import os                           # os function, i.e. checking file status
import ctypes 

import time as exec_time
import math

import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL

import numpy as np                  # all matrix manipulations & OpenGL args
import cv2

import obspy
from obspy.core import UTCDateTime

from liegroups.numpy import SE3

import shader
import shaderGeom
import reciever

class simulation_viewer_3D:
  def __init__(self, sim_params, stationList, sourceList, show_size):
    
    
    self.scene3D_size = np.array([32,32,32])
    self.scene3D_vertices = np.zeros((self.scene3D_size[2], self.scene3D_size[1], self.scene3D_size[0],4)).astype(np.float32)
    self.scene3D_indices = np.zeros((self.scene3D_size[2]-1, self.scene3D_size[1]-1, self.scene3D_size[0]-1,18)).astype(np.uint32) #6 triangulos por cada vertice, osea 18 vertices
    
    vertexIndex = 0
    for z in range(0,self.scene3D_size[2]):
      for y in range(0,self.scene3D_size[1]):
        for x in range(0,self.scene3D_size[0]):
        
          xi = float(x)/float(self.scene3D_size[0]-1.0)*2.0-1.0
          yi = float(y)/float(self.scene3D_size[1]-1.0)*2.0-1.0
          zi = float(z)/float(self.scene3D_size[2]-1.0)*2.0-1.0
          id = vertexIndex
            
          #print("vertice: ", xi, " ", yi, " ", zi)

          self.scene3D_vertices[z,y,x,0] = xi
          self.scene3D_vertices[z,y,x,1] = yi
          self.scene3D_vertices[z,y,x,2] = zi
          self.scene3D_vertices[z,y,x,3] = id
          
          vertexIndex += 1

    for z in range(0,self.scene3D_size[2]-1):
      for y in range(0,self.scene3D_size[1]-1):
        for x in range(0,self.scene3D_size[0]-1):
          
          self.scene3D_indices[z,y,x,0] = self.scene3D_vertices[  z,  y,  x,3]
          self.scene3D_indices[z,y,x,1] = self.scene3D_vertices[  z,  y,x+1,3]
          self.scene3D_indices[z,y,x,2] = self.scene3D_vertices[  z,y+1,x+1,3]
                
          #print("indices: ", self.scene3D_indices[z,y,x,0], " ", self.scene3D_indices[z,y,x,1], " ", self.scene3D_indices[z,y,x,2])                
              
          self.scene3D_indices[z,y,x,3] = self.scene3D_vertices[  z,  y,  x,3]
          self.scene3D_indices[z,y,x,4] = self.scene3D_vertices[  z,y+1,  x,3]
          self.scene3D_indices[z,y,x,5] = self.scene3D_vertices[  z,y+1,x+1,3]
                
          #print("indices: ", self.scene2D_indices[y-1,x-1,3], " ", self.scene2D_indices[y-1,x-1,4], " ", self.scene2D_indices[y-1,x-1,5])
            
          self.scene3D_indices[z,y,x,6] = self.scene3D_vertices[  z,  y,  x,3]
          self.scene3D_indices[z,y,x,7] = self.scene3D_vertices[  z,  y,x+1,3]
          self.scene3D_indices[z,y,x,8] = self.scene3D_vertices[z+1,  y,x+1,3]
                
          #print("indices: ", self.scene2D_indices[y-1,x-1,0], " ", self.scene2D_indices[y-1,x-1,1], " ", self.scene2D_indices[y-1,x-1,2])                
                
          self.scene3D_indices[z,y,x, 9] = self.scene3D_vertices[  z,  y,  x,3]
          self.scene3D_indices[z,y,x,10] = self.scene3D_vertices[z+1,  y,  x,3]
          self.scene3D_indices[z,y,x,11] = self.scene3D_vertices[z+1,  y,x+1,3]
                
          #print("indices: ", self.scene2D_indices[y-1,x-1,3], " ", self.scene2D_indices[y-1,x-1,4], " ", self.scene2D_indices[y-1,x-1,5])
            
          self.scene3D_indices[z,y,x,12] = self.scene3D_vertices[  z,  y,  x,3]
          self.scene3D_indices[z,y,x,13] = self.scene3D_vertices[  z,y+1,  x,3]
          self.scene3D_indices[z,y,x,14] = self.scene3D_vertices[z+1,y+1,  x,3]
                
          #print("indices: ", self.scene2D_indices[y-1,x-1,0], " ", self.scene2D_indices[y-1,x-1,1], " ", self.scene2D_indices[y-1,x-1,2])                
                
          self.scene3D_indices[z,y,x,15] = self.scene3D_vertices[  z,  y,  x,3]
          self.scene3D_indices[z,y,x,16] = self.scene3D_vertices[z+1,  y,  x,3]
          self.scene3D_indices[z,y,x,17] = self.scene3D_vertices[z+1,y+1,  x,3]
                
          #print("indices: ", self.scene2D_indices[y-1,x-1,3], " ", self.scene2D_indices[y-1,x-1,4], " ", self.scene2D_indices[y-1,x-1,5])
                
    #print(self.scene2D_vertices)
    #print(self.scene2D_indices)
                
    
    self.scene_VAO = glGenVertexArrays(1)  # create OpenGL vertex array id
    self.scene_VBO = glGenBuffers(1)  # create buffer for position attrib
    self.scene_EBO = glGenBuffers(1)
    
    glBindVertexArray(self.scene_VAO)      # activate to receive state below
    glBindBuffer(GL_ARRAY_BUFFER, self.scene_VBO)
    glBufferData(GL_ARRAY_BUFFER, self.scene3D_vertices, GL_STATIC_DRAW)
    
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.scene_EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.scene3D_indices, GL_STATIC_DRAW)
        
    #position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0*ctypes.sizeof(ctypes.c_float)));


    # cleanup and unbind so no accidental subsequent state update
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    self.scene3DShader = shaderGeom.Shader("shaders/scene3D.vs","shaders/scene3D.gs","shaders/scene3D.fs")
                
    glUseProgram(self.scene3DShader.glid)
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velxTex"), velx_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velyTex"), vely_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "velzTex"), velz_texture_unit_number);     
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "rhoTex"), rho_texture_unit_number);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "lamTex"), lam_texture_unit_number);      
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "muTex"), mu_texture_unit_number); 
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "surfaceTex"), surface_texture_unit_number);
       
    self.projmat = self.create_glm_prj_matrix(self.show_size[0]/3, self.show_size[1]/3, self.show_size[0]/2, self.show_size[1]/2, self.show_size[0], self.show_size[1], 0.00001, 100000.0)
    
    T = np.array([[1, 0, 0, 0.0],
                  [0, 1, 0, 0.0],
                  [0, 0, 1, -2.0],
                  [0, 0, 0, 1]])
                  
    self.cameraPose = SE3.identity()
    self.cameraPose = SE3.from_matrix(T)
    
    self.left_mouse_pressed = False
    self.pos_mouse = np.array([0,0])
    self.vel_mouse = np.array([0,0])

    self.setStation(stationList)
    self.setSource(sourceList)    

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
      
  def draw(self, source, recieverList, time, t_ini, simlvl):
      
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
      
    glViewport(0,0,self.show_size[0],self.show_size[1])
    
    glUseProgram(self.frame3DShader.glid)
    
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "width"), self.sim_size[simlvl][0]); 
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "height"), self.sim_size[simlvl][1]); 
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "depth"), self.sim_size[simlvl][2]);
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "dx"), self.dxyz_cart[simlvl][0]);
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "dy"), self.dxyz_cart[simlvl][1]); 
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "dz"), self.dxyz_cart[simlvl][2]);     
    glUniform1f(glGetUniformLocation(self.frame3DShader.glid, "dt"), self.dt[simlvl]); 
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "lvl"), 0);
    glUniform1i(glGetUniformLocation(self.frame3DShader.glid, "layer"), int(self.sim_size[simlvl][2]*0.5));  
    
    source_s = (source.pos - self.ini_corner)/(self.fin_corner-self.ini_corner)

    glUniform1fv(glGetUniformLocation(self.frame3DShader.glid, "source"), 3, source_s); 
    #glUniform1fv(glGetUniformLocation(self.frame3DShader.glid, "recieverLoc"),45, self.recieverLoc); 
    
    glBindVertexArray(self.frame_VAO)
    glDrawArrays(GL_TRIANGLES, 0, 6)
        
    #usuario: jdondo@gmail.com
    #password:larry1413  
    
  def create_glm_prj_matrix(self, fx, fy, cx, cy, w, h, znear, zfar):

    projmat = np.zeros((4,4))

    projmat[0,0] = 2.0*fx/w;
    projmat[1,1] = 2.0*fy/h;
    projmat[2,0] = 1.0 - 2.0*cx/w;
    projmat[2,1] = -1.0 + 2.0*cy/h;
    projmat[2,2] = -(zfar + znear) / (zfar - znear);
    projmat[2,3] = -1.0;
    projmat[3,2] = -2.0 * zfar * znear / (zfar - znear);

    return projmat
    
  def drawScene(self, pose):
  
    glEnable(GL_BLEND);
    glBlendEquation(GL_FUNC_ADD);
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE);
    
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
      
    glViewport(0,0,self.show_size[0],self.show_size[1])
  
    glDisable(GL_CULL_FACE);
    glDisable(GL_DEPTH_TEST);  
    glClearColor(0.5, 0.5, 0.5, 0.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
    
    glUseProgram(self.scene3DShader.glid)
    
    #glUniform1fv(glGetUniformLocation(self.scene3DShader.glid, "cameraPose"), 3, source_s); 
    #glUniform1fv(glGetUniformLocation(self.scene3DShader.glid, "projection"),45, self.recieverLoc); 
    
    #print(pose.as_matrix())
    
    glUniformMatrix4fv(glGetUniformLocation(self.scene3DShader.glid, "cameraPose"), 1, GL_TRUE, pose.as_matrix())  #no se porque, pero la tengo que transponer, usando ese "GL_TRUE"
    glUniformMatrix4fv(glGetUniformLocation(self.scene3DShader.glid, "projection"), 1, GL_FALSE, self.projmat)
    
    glBindVertexArray(self.scene_VAO);
    glDrawElements(GL_TRIANGLES, self.scene3D_indices.size, GL_UNSIGNED_INT, None);
    
    glDisable(GL_BLEND);
    
  def onMousePosition(self, win, xpos, ypos):
    self.vel_mouse = self.pos_mouse - np.array([xpos, ypos])
    self.pos_mouse = np.array([xpos, ypos])
    if self.left_mouse_pressed == True:
      self.cameraPose = self.cameraPose.dot(SE3.exp([0.0, 0.0, 0.0, -self.vel_mouse[0]*0.01, self.vel_mouse[1]*0.01, 0.0]))
    
    #pass
    
  def onMouseButton(self, win, button, action, mods):
    #print 'mouse button: ', win, button, action, mods
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
      self.left_mouse_pressed = True
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
      self.left_mouse_pressed = False
      #[xpos,ypos] = glfw.get_cursor_pos(win) 
      #print("mouse pos", xpos, ypos)
    #pass

  def onKeyboard(self, win, key, scancode, action, mods):
    #print 'keyboard: ', win, key, scancode, action, mods
    """
    if action == glfw.PRESS:
      # ESC to quit
      if key == glfw.KEY_ESCAPE: 
        self.exitNow = True
      else:
        # toggle cut
        self.scene.showCircle = not self.scene.showCircle 
    """
    pass

  def onSize(self, win, width, height):
    #print 'onsize: ', win, width, height
    #self.width = width
    #self.height = height
    #self.aspect = width/float(height)
    #glViewport(0, 0, self.width, self.height)
    pass
    
