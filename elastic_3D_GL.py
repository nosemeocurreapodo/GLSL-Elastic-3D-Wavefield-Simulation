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

import reciever

import simulation_step
import simulation_params
import medium_params
import simulation_memory
import simulation_source
import simulation_reciever
import viewer_2D_GL

class elastic_sim:
  def __init__(self, stationList, sourceList, max_medium_vel, min_medium_vel, mediumParamsSize, show = True):
    
    self.show_size = np.array([640,480])
    
    glfw.init() 

    # version hints: create GL window with >= OpenGL 3.3 and core profile
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)
    glfw.window_hint(glfw.VISIBLE, show)
    self.win = glfw.create_window(self.show_size[0], self.show_size[1], 'Viewer', None, None)

    # make win's OpenGL context current; no OpenGL calls can happen before
    glfw.make_context_current(self.win)

    # register event handlers
    #glfw.set_key_callback(win, self.on_key)
    #glfwSetMouseButtonCallback(window, mouse_button_callback);
    #glfw.set_cursor_pos_callback(self.win, self.onMousePosition);
    #glfw.set_mouse_button_callback(self.win, self.onMouseButton)
    #glfw.set_key_callback(self.win, self.onKeyboard)
    #glfw.set_window_size_callback(self.win, self.onSize) 

    # useful message to check OpenGL renderer characteristics
    print('OpenGL', glGetString(GL_VERSION).decode() + ', GLSL',
              glGetString(GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', glGetString(GL_RENDERER).decode())

    # initialize GL by setting viewport and default render characteristics

    
    self.stationList = stationList
    self.sourceList = sourceList
    self.mediumParamsSize = mediumParamsSize
    
    self.sim_params = simulation_params.simulation_params(stationList, sourceList, max_medium_vel, min_medium_vel, mediumParamsSize)
    self.med_params = medium_params.medium_params(mediumParamsSize)
    self.sim_memory = simulation_memory.simulation_memory(self.sim_params)
    self.sim_source = simulation_source.simulation_source(self.sim_params)
    self.sim_step = simulation_step.simulation_step(self.sim_params, self.sim_memory, self.med_params)
    self.sim_reciever = simulation_reciever.simulation_reciever(stationList, self.sim_params)
    self.sim_viewer = viewer_2D_GL.simulation_viewer_2D(self.sim_params, self.sim_reciever, self.show_size)

  def setMediumParams(self, invRho, lam, mu):
    self.med_params.setMediumParams(invRho, lam, mu)
       
  def simulate(self, source, t_ini, t_steps):
  
    self.sim_memory.reset() 
    self.sim_source.reset()      
    self.sim_source.setBodyForcesFromSource(source, self.sim_params.max_frec)
    self.sim_viewer.setSource(self.sim_source)
      
    for t in range(0, t_steps):
      #start_time = exec_time.time()     
      
      time = t_ini + t*self.sim_params.dt

      self.sim_source.stepBodyForceTimeFunction(t, time)
      self.sim_step.step()
      #self.sim_step.step_CPU()
      self.sim_reciever.saveData(t)
      self.sim_viewer.draw()
        
      glfw.swap_buffers(self.win)
      glfw.poll_events()
    
      #self.drawScene(self.cameraPose)
     
      #print("--- %s seconds ---" % (exec_time.time() - start_time)) 
      
      #print("simulating source: ", source.time)
      #print("step: ", t, " time: ", time)
      
    stationStreams = self.sim_reciever.getData(t_ini, t_steps)
    
    """
    timefunct = self.sim_source.source_time_function[0:self.t_steps]
      
    t_1 = t_source - self.sim_params.dt*int((2.0/(source_frec))/self.sim_params.dt)
    t_2 = t_source + self.sim_params.dt*int((2.0/(source_frec))/self.sim_params.dt)
    ts_1 = int((t_1 - t_ini)/self.sim_params.dt)
    ts_2 = int((t_2 - t_ini)/self.sim_params.dt)
      
    timefunct_part = self.sim_source.source_time_function[ts_1:ts_2]
    timefunct_part = timefunct_part
    
    return stationSteams, timefunct, timefunct_part, t_steps
    """
    return stationStreams    

    
