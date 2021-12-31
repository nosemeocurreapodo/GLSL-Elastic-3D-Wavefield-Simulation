# Python built-in modules
import os                           # os function, i.e. checking file status
import ctypes 
import copy

from matplotlib import pyplot as plt

import time as exec_time
import math

import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL

import numpy as np                  # all matrix manipulations & OpenGL args

import obspy
from obspy.core import UTCDateTime

import src.reciever as reciever
import src.source as source
import src.simulation_step as simulation_step
import src.simulation_params as simulation_params
import src.simulation_surface as simulation_surface
import src.wavefield_memory as wavefield_memory
import src.medium_memory as medium_memory
import src.simulation_source as simulation_source
import src.simulation_reciever as simulation_reciever
import src.viewer_2D_GL as viewer_2D_GL
import src.invertion_helpers as invertion_helpers

class elastic_sim:
  def __init__(self, stationList, sourceList, max_medium_vel, min_medium_vel, params, show = True):
    
    self.show_size = np.array([640,480])
    self.stationList = stationList
    self.sourceList = sourceList
    
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
              
    self.sim_params = simulation_params.simulation_params(stationList, sourceList, max_medium_vel, min_medium_vel, params)
    self.sim_viewer = viewer_2D_GL.simulation_viewer_2D(self.sim_params, stationList, sourceList, self.show_size)        
    self.wave_memory = wavefield_memory.wavefield_memory(self.sim_params)
    self.med_memory = medium_memory.medium_memory(self.sim_params)
    self.sim_surface = simulation_surface.simulation_surface(self.sim_params, stationList)    
    self.sim_step = simulation_step.simulation_step(self.sim_params, self.wave_memory)
    self.sim_source = simulation_source.simulation_source(self.sim_params, sourceList)
    self.sim_reciever = simulation_reciever.simulation_reciever(self.sim_params, stationList)

  def updateVelTable(self, veltable):
    self.med_memory.setWithVelTable(veltable)
    
  def updateMediumParams(self, rho, lam, mu):
    self.med_memory.setWithLameParams(rho, lam, mu)
  
  def setSimulationTime(self, sources):
    sourceList = []
    if type(sources) != list:
      sourceList.append(sources)
    else:
      sourceList = sources
  
    self.sourceList = sourceList 
    self.sim_params.setSimulationTime(sourceList)
      
  def updateSource(self, sources):
  
    sourceList = []
    if type(sources) != list:
      sourceList.append(sources)
    else:
      sourceList = sources
  
    self.sourceList = sourceList
    self.sim_source.setSource(sourceList)   
    self.sim_viewer.setSource(sourceList)
      
  def simulate(self):
    
    self.wave_memory.reset() 
    #self.sim_source.reset()  
    self.sim_reciever.reset()    
      
    for t in range(0, self.sim_params.t_steps):
      #start_time = exec_time.time()     
      
      #time = t_ini + t*self.sim_params.dt
      #print("time ", time)

      self.sim_source.stepBodyForceTimeFunction(t)
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
      
    stationStreams = self.sim_reciever.getData(self.sim_params.starttime)
    return stationStreams

  def filterTrace(self, trace, sourceIndex): 
    
    #print("trace:")
    #trace.filter('lowpass', freq = self.sim_params.req_frec, corners=8, zerophase=True)
    #spec, freqs = np.fft.rfft(trace.data), np.fft.rfftfreq(trace.data.shape[0], trace.stats.delta)
    #plt.loglog(freqs, np.abs(spec), label="real", color="blue")
    #plt.magnitude_spectrum(trace.data, Fs=1.0/trace.stats.delta, scale='dB')
    #plt.phase_spectrum(trace.data, Fs=1.0/trace.stats.delta)
    #plt.show()
    
    #phase = np.rad2deg(np.unwrap(np.angle(spec)))
    #phase = phase - phase[0]
    #plt.semilogx(freqs, phase, label="real", color="red")
    
    #plt.phase_spectrum(trace.data, Fs=1.0/trace.stats.delta)
    #plt.show()    

    #if sourceIndex < 0:
    #  return

    #trace.filter('highpass', freq = self.sim_source.source_peak_freq[sourceIndex]*0.25, corners=2, zerophase=True)


    #trace.filter('bandpass', freqmin = self.sim_source.source_peak_freq[sourceIndex]*0.5,freqmax = self.sim_source.source_peak_freq[sourceIndex]*1.5, corners=8, zerophase=True)    
    
    
    #trying adding responce to simulation instead of removing it from real trace
    if trace.stats.network == "SIM":
      #self.stationList[recieverIndex].addResponce(trace)
      return
    #else:
    #  trace.resample(1.0/self.sim_params.rec_dt)
    #  return 
    
    


    #trace.filter('lowpass', freq = self.sim_params.req_frec, corners=8, zerophase=True)
    


    #trace.resample(1.0/self.sim_params.rec_dt)
    #return
    
    #min_frec = 2.0/(self.sim_params.endtime - self.sim_params.starttime)
    #print("minfrec: ", min_frec)
    #trace.filter('lowpass', freq = self.sim_params.req_frec, corners=8, zerophase=True)
    #trace.filter('bandpass', freqmin = min_frec, freqmax = self.sim_params.req_frec, corners=8, zerophase=True)
    #trace.resample(1.0/self.sim_params.rec_dt)

    #spec, freqs = np.fft.rfft(trace.data), np.fft.rfftfreq(trace.data.shape[0], self.sim_params.rec_dt)
  
    #plt.loglog(freqs, np.abs(spec), label="real", color="blue")
    #plt.show()

    #return
    
    t_1 = self.sim_source.source_time[sourceIndex] - 1.5/self.sim_source.source_peak_freq[sourceIndex];
    t_2 = self.sim_source.source_time[sourceIndex] + 1.5/self.sim_source.source_peak_freq[sourceIndex];
    ts_1 = int((t_1 - self.sim_params.starttime)/self.sim_params.dt)
    ts_2 = int((t_2 - self.sim_params.starttime)/self.sim_params.dt)
    
    #print("times: ", t_1, " ", t_2)
    #print("samples: ", ts_1, " ", ts_2)
      
    sourceTimeFunction = self.sim_source.source_vel_time_function[sourceIndex][ts_1:ts_2]
    
    spec, freqs = np.fft.rfft(sourceTimeFunction), np.fft.rfftfreq(sourceTimeFunction.shape[0], self.sim_params.dt)
  
    #print("source function:")
    #plt.plot( self.sim_source.source_acc_time_function[sourceIndex][ts_1:ts_2])
    #plt.loglog(freqs, np.abs(spec), label="real", color="blue")
    #plt.show()
    
    #plt.loglog(freqs, np.abs(spec), label="real", color="blue")
    #plt.magnitude_spectrum(self.sim_source.source_vel_time_function[sourceIndex][ts_1:ts_2], Fs=1.0/self.sim_params.dt, scale='dB')
    #plt.magnitude_spectrum(self.sim_source.source_acc_time_function[sourceIndex][ts_1:ts_2], Fs=1.0/self.sim_params.dt, scale='dB')
    #plt.phase_spectrum(self.sim_source.source_vel_time_function[sourceIndex][ts_1:ts_2], Fs=1.0/self.sim_params.dt)
    #plt.show()
    
    #phase = np.rad2deg(np.unwrap(np.angle(spec)))
    #phase = phase - phase[0]
    #plt.semilogx(freqs, phase, label="real", color="red")
    #plt.phase_spectrum(self.sim_source.source_vel_time_function[sourceIndex][ts_1:ts_2], Fs=1.0/self.sim_params.dt)    
    #plt.show()    
    
    max_gain = np.amax(np.abs(spec))
    #print("max gain ", max_gain)
    #print("mean ", 1.0/np.sum(sourceTimeFunction))
  
    trace.resample(1.0/self.sim_params.dt)
    real_tr_new_data = np.convolve(trace.data, sourceTimeFunction/max_gain, mode='same')
    trace.data = real_tr_new_data
    trace.resample(1.0/self.sim_params.rec_dt)
    
    """
    plt.plot(sourceTimeFunction, 'b', label='time', alpha=0.7)
    plt.ylabel("time function")    
    plt.legend()
    plt.show()
    """

  def filterStream(self, stream, sourceIndex):

    self.filterTrace(stream[0], sourceIndex)
    self.filterTrace(stream[1], sourceIndex)
    self.filterTrace(stream[2], sourceIndex)
  
  def calculateSourceDerivative(self, real_strs, best_strs, sources, mt_only = False): 

    #print("calculateSourceDerivative")
    
    sourceList = []
    if type(sources) != list:
      sourceList.append(copy.deepcopy(sources))
    else:
      sourceList = copy.deepcopy(sources)
    
    derivative_strss = []  

    print("Computing source derivatives")    
    invertion_helpers.printProgressBar(0, 10*len(sourceList), prefix = 'Progress:', suffix = 'Complete', length = 50)
        
    for l in range(len(sourceList)):
      for k in range(0, 10):
        calculate = True
        new_sourceList = copy.deepcopy(sourceList)
        delta = 0
        if k == 0:
          delta = self.sim_params.dt
          new_sourceList[l].time += delta
          if mt_only == True:
            calculate = False
        if k == 1:
          delta = self.sim_params.dlat
          new_sourceList[l].lat += delta
          if mt_only == True:
            calculate = False
        if k == 2:
          delta = self.sim_params.dlon
          new_sourceList[l].lon += delta 
          if mt_only == True:
            calculate = False        
        if k == 3:
          delta = self.sim_params.ddepth
          new_sourceList[l].depth += delta
          if mt_only == True:
            calculate = False
        if k == 4:
          delta = abs(new_sourceList[l].mxx)*0.01
          if delta <= 0.0:
            delta = 0.001          
          new_sourceList[l].mxx += delta 
        if k == 5:
          delta = abs(new_sourceList[l].myy)*0.01 
          if delta <= 0.0:
            delta = 0.001 
          new_sourceList[l].myy += delta
        if k == 6:
          delta = abs(new_sourceList[l].mzz)*0.01 
          if delta <= 0.0:
            delta = 0.001 
          new_sourceList[l].mzz += delta
        if k == 7:
          delta = abs(new_sourceList[l].mxy)*0.01
          if delta <= 0.0:
            delta = 0.001 
          new_sourceList[l].mxy += delta
        if k == 8:
          delta = abs(new_sourceList[l].mxz)*0.01 
          if delta <= 0.0:
            delta = 0.001 
          new_sourceList[l].mxz += delta           
        if k == 9:
          delta = abs(new_sourceList[l].myz)*0.01
          if delta <= 0.0:
            delta = 0.001 
          new_sourceList[l].myz += delta
            
        self.updateSource(new_sourceList)    
      
        if calculate == True:
          sim_strs = self.simulate()
          for i in range(0,len(sim_strs)):
            self.filterStream(sim_strs[i],0)      
        else:            
          sim_strs = copy.deepcopy(best_strs)
      
        #error_strs = calculateErrorStrs(sim_strs,real_strs)
        #MSE = calculateMSE(error_strs)
        #print("MSE ", MSE)
      
        derivative_strs = copy.deepcopy(best_strs)  
        for i in range(0,len(real_strs)):
          best_str = best_strs[i]
          sim_str = sim_strs[i]
          derivative_str = derivative_strs[i]
          steps = min(best_str[0].stats.npts, sim_str[0].stats.npts)
          for j in range(0,3):        
            derivative_str[j].data[0:steps] = (sim_str[j].data[0:steps] - best_str[j].data[0:steps])/delta
      
        derivative_strss.append(derivative_strs)   
        
        invertion_helpers.printProgressBar(k+1+l*10, 10*len(sourceList), prefix = 'Progress:', suffix = 'Complete', length = 50)   
    
    return derivative_strss
  
  
  def calculateMediumDerivative(self, real_strs, best_rho, best_lam, best_mu, best_strs, max_rho, max_lam, max_mu): 
  
    #print("calculateMediumDerivative")
    derivative_strss = []  
  
    total_num = best_rho.size + best_lam.size + best_mu.size
    current_num = 0
  
    print("Computing medium derivatives")
    invertion_helpers.printProgressBar(0, total_num, prefix = 'Progress:', suffix = 'Complete', length = 50)
    #for each param (rho, lam, mu)
    for param_index in range(0,3):  
      calculate = True
      #print("param shape ", param.shape)    
      for x_shape in range(0, best_rho.shape[0]):
        
        """
        if x_shape > 1.0*best_rho.shape[0]:
          calculate = False
          #print("skipping depth ", x_shape)
        else:
          calculate = True
        """
        for y_shape in range(0, best_rho.shape[1]):
          for z_shape in range(0, best_rho.shape[2]):
            
            calculate = True
            rho = (best_rho.copy())
            lam = (best_lam.copy())
            mu = (best_mu.copy())
        
            if param_index == 0:  
              deltaParam = rho[x_shape, y_shape, z_shape]*0.01            
              rho[x_shape,y_shape,z_shape] += deltaParam
              #calculate = False
              #print("invRho ", invRho)
            if param_index == 1:  
              deltaParam = lam[x_shape, y_shape, z_shape]*0.01             
              lam[x_shape,y_shape,z_shape] += deltaParam
              #calculate = False
              #print("lam ", lam)
            if param_index == 2:
              deltaParam = mu[x_shape, y_shape, z_shape]*0.01             
              mu[x_shape,y_shape,z_shape] += deltaParam
              #print("mu ", mu)
              """
              if np.random.random_sample() > 0.75:
                calculate = True
              else:
                calculate = False            
              """

            self.updateMediumParams(rho*max_rho, lam*max_lam, mu*max_mu) 
      
            if calculate == True:
              #self.updateSource(source)
              sim_strs = self.simulate()

              for i in range(0,len(sim_strs)):
                self.filterStream(sim_strs[i],0)
                  
            else:            
              sim_strs = copy.deepcopy(best_strs)
            
            #error_strs = calculateErrorStrs(sim_strs,real_strs)
            #MSE = calculateMSE(error_strs)
            #print("MSE ", MSE)
          
            derivative_strs = copy.deepcopy(best_strs)  
            for i in range(0,len(real_strs)):
              best_str = best_strs[i]
              sim_str = sim_strs[i]
              derivative_str = derivative_strs[i]
      
              steps = min(best_str[0].stats.npts, sim_str[0].stats.npts)
              for j in range(0,3):        
                derivative_str[j].data[0:steps] = (sim_str[j].data[0:steps] - best_str[j].data[0:steps])/deltaParam
          
            derivative_strss.append(derivative_strs)  
            current_num += 1
            invertion_helpers.printProgressBar(current_num, total_num, prefix = 'Progress:', suffix = 'Complete', length = 50)     
      
    return derivative_strss
    
