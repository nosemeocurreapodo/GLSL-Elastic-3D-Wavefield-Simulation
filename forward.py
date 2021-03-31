import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
import obspy
import time as exec_time

import elastic_3D_GL
import source
import reciever
import dataReader
#[real_ini_corner, real_fin_corner, real_vp, real_vs, real_rho, surface, recievers, sources] = dataReader.getCaviahueData()
[recievers, sources, veltable] = dataReader.getCubaData()
mediumParamsSize = np.array([1, 1, 128])

#np.__config__.show()

sim_wavefield = elastic_3D_GL.elastic_sim(recievers, sources, 8000, 2000, mediumParamsSize)

#print("reading data from velocity table")

vp = np.zeros((mediumParamsSize[2],mediumParamsSize[1],mediumParamsSize[0]), dtype='float32')
vs = np.zeros((mediumParamsSize[2],mediumParamsSize[1],mediumParamsSize[0]), dtype='float32')
rho = np.zeros((mediumParamsSize[2],mediumParamsSize[1],mediumParamsSize[0]), dtype='float32')

#print("veltable: ")
#print(veltable)
      
for i in range(0,mediumParamsSize[2]):
    
  depth = sim_wavefield.sim_params.ini_corner[2] + i*(sim_wavefield.sim_params.fin_corner[2] - sim_wavefield.sim_params.ini_corner[2])/mediumParamsSize[2]

  #print("depth: ", depth)
  
  vp_ = veltable[0,1]*1000.0*0.0001
  vs_ = veltable[0,2]*1000.0*0.0001
  rho_ = veltable[0,3]*1000.0*0.1
    
  for j in range(0,veltable.shape[0]):
    depth_veltable = veltable[j,0]*1000.0
    #print("depth veltable: ", depth_veltable)
    if depth >= depth_veltable:
      #print("is less!")
      vp_ = veltable[j,1]*1000.0
      vs_ = veltable[j,2]*1000.0
      rho_ = veltable[j,3]*1000.0
      #break
  
  #print("i: ", i, " depth: ", depth, " vp: ", vp_, " vs: ", vs_, " rho: ", rho_)      
            
  vp[i,:,:] = vp_
  vs[i,:,:] = vs_
  rho[i,:,:] = rho_

#init logaritmic (so they are not just positive numbers) rho, lam and mu from velocity parameters
"""
invRho = np.log(1.0/rho)
lam = np.log(rho*((vp*vp) - 2.0*(vs*vs)))
mu = np.log((vs*vs)*rho)
"""
invRho = 1.0/rho
lam = rho*((vp*vp) - 2.0*(vs*vs))
mu = (vs*vs)*rho
     
#print("done reading data!")

sim_wavefield.setMediumParams(invRho, lam, mu)

for s1 in sources:

  s2_time = obspy.UTCDateTime(2016, 1, 17, 8, 30, 31.526743) 
  s2 = source.source(np.array([20.04158314,   -76.16285844,  4574.35342365]),s2_time,np.array([-2.37178602e+14,  -2.19391049e+16,   4.33634443e+16,  -3.39245290e+15,  -7.79326575e+14,   4.60586216e+15]))

  source = s1

  t_source = obspy.UTCDateTime(source.time.year, source.time.month, source.time.day, source.time.hour, source.time.minute, source.time.second) 
  #TODO calcular esto a partir de datos del sismo como la coda y otros
  #t_ini = t_source - self.sim_params.dt*int(40.0/self.sim_params.dt)
  t_ini = t_source - sim_wavefield.sim_params.dt*int((2.0/(sim_wavefield.sim_params.max_frec))/sim_wavefield.sim_params.dt)
  t_fin = t_source + sim_wavefield.sim_params.dt*int(240.0/sim_wavefield.sim_params.dt)
        
  t_steps = int((t_fin-t_ini)/sim_wavefield.sim_params.dt)
  
  #start_time = exec_time.time() 
  print("steps ", t_steps)
  sim_strs = sim_wavefield.simulate(source, t_ini, t_steps)
  #print("--- %s seconds ---" % (exec_time.time() - start_time)) 
  """
  plt.plot(timefunct_part, 'b', label='time', alpha=0.7)
  plt.ylabel("time function")    
  plt.legend()
  plt.show()
  
  spec, freqs = np.fft.rfft(timefunct_part), np.fft.rfftfreq(timefunct_part.shape[0], sim_wavefield.sim_params.dt)
  plt.loglog(freqs, np.abs(spec), label="real", color="blue")
  plt.legend()
  plt.show()
  """
  #get real stream
  for sim_str in sim_strs:
      
    real_trs = []   
    
    for t in range(0,3):
      
      real_tr = dataReader.getCubaRealTrace(sim_str[t].stats.station,sim_str[t].stats.channel,sim_str[t].stats.starttime,sim_str[t].stats.endtime)
        
      #print("start time ", sim_str[t].stats.starttime)
      #print("read real stream")
      #print(real_tr)
            
      #real_tr.filter('lowpass', freq=sim_wavefield.sim_params.max_frec*2.0, corners=8, zerophase=True)
      #sim_str[t].filter('lowpass', freq=source_frec*1.0, corners=4, zerophase=True)
      real_tr.filter('bandpass', freqmin = sim_wavefield.sim_params.max_frec*0.5, freqmax = sim_wavefield.sim_params.max_frec*1.5, corners=8, zerophase=True)
      sim_str[t].filter('bandpass', freqmin = sim_wavefield.sim_params.max_frec*0.5, freqmax = sim_wavefield.sim_params.max_frec*1.5, corners=8, zerophase=True)
      #real_tr.filter('bandpass', freqmin = 0.02, freqmax = 0.06, corners=8, zerophase=True)
      #sim_str[t].filter('bandpass', freqmin = 0.02, freqmax = 0.06, corners=8, zerophase=True)
      
      """
      if(real_tr.stats.sampling_rate > sim_str[t].stats.sampling_rate):
        decimate_factor = int(real_tr.stats.sampling_rate/sim_str[t].stats.sampling_rate)
        real_tr.decimate(factor=decimate_factor, no_filter=True)
      if(sim_str[t].stats.sampling_rate > real_tr.stats.sampling_rate):
        decimate_factor = int(sim_str[t].stats.sampling_rate/real_tr.stats.sampling_rate)
        sim_str.decimate(factor=decimate_factor, no_filter=True)
      """
      real_tr.resample(1.0/sim_str[t].stats.delta)
      """
      real_tr_new_data = np.convolve(real_tr.data, timefunct_part, mode='same')
      real_tr.data = real_tr_new_data
      """
          
      real_trs.append(real_tr)
          
    real_str = obspy.Stream(traces=[real_trs[0], real_trs[1], real_trs[2]])


    print("simulated stream")
    print(sim_str)
    #sim_str.write("sim_"+sim_str[0].stats.station,format="SAC")
    #sim_str.plot()
        
    print("real stream")
    print(real_str)
    #real_str.write("real_"+real_str[0].stats.station,format="SAC")
    #real_str += sim_str
    #real_str.plot()
    """
    real_str[0].data = real_str[0].data/np.amax(real_str[0].data)
    sim_str[0].data = sim_str[0].data/np.amax(real_str[0].data)

    real_str[1].data = real_str[1].data/np.amax(real_str[1].data)
    sim_str[1].data = sim_str[1].data/np.amax(real_str[1].data)
    
    real_str[2].data = real_str[2].data/np.amax(real_str[2].data)
    sim_str[2].data = sim_str[2].data/np.amax(real_str[2].data)
    """
    
    p_error = 0.0
    
    p_error_n = 0.0
    p_error_e = 0.0
    p_error_z = 0.0
    
    rms_error = 0
    
    steps = min(sim_str[0].stats.npts, real_str[0].stats.npts)
    for k in range(0, steps):
      
      rms_error += (sim_str[0].data[k] - real_str[0].data[k])*(sim_str[0].data[k] - real_str[0].data[k])
      rms_error += (sim_str[1].data[k] - real_str[1].data[k])*(sim_str[1].data[k] - real_str[1].data[k])
      rms_error += (sim_str[2].data[k] - real_str[2].data[k])*(sim_str[2].data[k] - real_str[2].data[k])
      
      
      error_n = abs((sim_str[0].data[k] - real_str[0].data[k])/np.amax(real_str[0].data))
      error_e = abs((sim_str[1].data[k] - real_str[1].data[k])/np.amax(real_str[1].data))
      error_z = abs((sim_str[2].data[k] - real_str[2].data[k])/np.amax(real_str[2].data))
      
      #print("n ", sim_str[0].data[k]," ", real_str[0].data[k])
      #print("error ", error_n, " ", error_e, " ", error_z)
      
      p_error_n += error_n
      p_error_e += error_e
      p_error_z += error_z
      
      p_error += error_n + error_e + error_z
      
    p_error_n = p_error_n/steps
    p_error_e = p_error_e/steps
    p_error_z = p_error_z/steps
    
    p_error = p_error/(steps*3)
    
    rms_error = np.sqrt(rms_error/(steps*3))
    
    print("rms error ", rms_error)
    print("p error ", p_error)
    print("p error ", p_error_n, " ", p_error_e, " ", p_error_z)   
        
    # Now let's plot the raw and filtered data...
    #real_t = np.arange(0, real_str[0].stats.npts / real_str[0].stats.sampling_rate, real_str[0].stats.delta)
    #sim_t = np.arange(0, (sim_str[0].stats.npts-0.5) / sim_str[0].stats.sampling_rate, sim_str[0].stats.delta)
    """
    real_t_e = np.linspace(real_str[0].stats.starttime.timestamp, real_str[0].stats.endtime.timestamp, real_str[0].stats.npts)
    sim_t_e = np.linspace(sim_str[0].stats.starttime.timestamp, sim_str[0].stats.endtime.timestamp, sim_str[0].stats.npts)
    real_t_n = np.linspace(real_str[1].stats.starttime.timestamp, real_str[1].stats.endtime.timestamp, real_str[1].stats.npts)
    sim_t_n = np.linspace(sim_str[1].stats.starttime.timestamp, sim_str[1].stats.endtime.timestamp, sim_str[1].stats.npts)
    real_t_z = np.linspace(real_str[2].stats.starttime.timestamp, real_str[2].stats.endtime.timestamp, real_str[2].stats.npts)
    sim_t_z = np.linspace(sim_str[2].stats.starttime.timestamp, sim_str[2].stats.endtime.timestamp, sim_str[2].stats.npts)
    """ 
    
    real_t_e = np.linspace(0.0, real_str[0].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[0].stats.npts)
    sim_t_e = np.linspace(0.0, sim_str[0].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, sim_str[0].stats.npts)
    real_t_n = np.linspace(0.0, real_str[1].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[1].stats.npts)
    sim_t_n = np.linspace(0.0, sim_str[1].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, sim_str[1].stats.npts)
    real_t_z = np.linspace(0.0, real_str[2].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[2].stats.npts)
    sim_t_z = np.linspace(0.0, sim_str[2].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, sim_str[2].stats.npts)
    
    #print("sim: ", sim_t.size, " ", sim_str[0].data.size," ", sim_str[0].stats.npts)
    """
    plt.subplot(311)
    plt.plot(real_t_e, real_str[0].data/np.amax(real_str[0].data), 'b', label='real', alpha=0.7)
    plt.plot(sim_t_e, sim_str[0].data/np.amax(sim_str[0].data), 'r', label='sim', alpha=0.7)
    plt.ylabel(real_str[0].stats.channel)
        
    plt.subplot(312)
    plt.plot(real_t_n, real_str[1].data/np.amax(real_str[1].data), 'b', label='real', alpha=0.7)
    plt.plot(sim_t_n, sim_str[1].data/np.amax(sim_str[1].data), 'r', label='sim', alpha=0.7)
    plt.ylabel(real_str[1].stats.channel)
        
    plt.subplot(313)
    plt.plot(real_t_z, real_str[2].data/np.amax(real_str[2].data), 'b', label='real', alpha=0.7)
    plt.plot(sim_t_z, sim_str[2].data/np.amax(sim_str[2].data), 'r', label='sim', alpha=0.7)
    plt.ylabel(real_str[2].stats.channel)  
    """
    
    """
    plt.subplot(311)
    plt.plot(real_t_e, real_str[0].data, 'b', label='real', alpha=0.7)
    plt.plot(sim_t_e, sim_str[0].data, 'r', label='sim', alpha=0.7)
    plt.title(real_str[0].stats.channel, fontweight ='bold', fontsize = 7)
    #plt.xlabel('time (s)', fontweight ='bold', fontsize = 7)
    #plt.ylabel('velocity (m/s)', fontweight ='bold', fontsize = 7)
        
    plt.subplot(312)
    plt.plot(real_t_n, real_str[1].data, 'b', label='real', alpha=0.7)
    plt.plot(sim_t_n, sim_str[1].data, 'r', label='sim', alpha=0.7)
    plt.title(real_str[1].stats.channel, fontweight ='bold', fontsize = 7)
    #plt.xlabel('time (s)', fontweight ='bold', fontsize = 7)
    #plt.ylabel('velocity (m/s)', fontweight ='bold', fontsize = 7)
    
    plt.subplot(313)
    plt.plot(real_t_z, real_str[2].data, 'b', label='real', alpha=0.7)
    plt.plot(sim_t_z, sim_str[2].data, 'r', label='sim', alpha=0.7)
    plt.title(real_str[2].stats.channel, fontweight ='bold', fontsize = 7)
    #plt.xlabel('time (s)', fontweight ='bold', fontsize = 7)
    #plt.ylabel('velocity (m/s)', fontweight ='bold', fontsize = 7)
   
    #plt.xlabel('level of detail', fontweight ='bold', fontsize = 15)
    #plt.ylabel('time (seconds)', fontweight ='bold', fontsize = 15)
   
    #plt.plot(t_new, tr_new.data, 'r', label='Lowpassed/Downsampled', alpha=0.7)
    #plt.xlabel('Time [s]')
    #plt.xlim(82, 83.5)
    plt.suptitle(real_str[0].stats.station, fontweight ='bold', fontsize = 15)
    plt.supxlabel('time (s)', fontweight ='bold', fontsize = 15)
    plt.supylabel('velocity (m/s)', fontweight ='bold', fontsize = 7)
    plt.legend()
    plt.show()
    """
    
    #print("max", np.amax(real_str[0].data), np.amax(real_str[1].data), np.amax(real_str[2].data))
    #print("min", np.amin(real_str[0].data), np.amin(real_str[1].data), np.amin(real_str[2].data))
     
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, constrained_layout=True, sharey=True)
    ax1.plot(real_t_n, real_str[0].data, 'b', label='real')
    ax1.plot(sim_t_n, sim_str[0].data, 'r', label='sim')
    ax1.set_title(real_str[0].stats.channel)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('velocity (m/s)')

    ax2.plot(real_t_n, real_str[1].data, 'b', label='real')
    ax2.plot(sim_t_n, sim_str[1].data, 'r', label='sim')
    ax2.set_title(real_str[1].stats.channel)
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('velocity (m/s)')
    
    ax3.plot(real_t_n, real_str[2].data, 'b', label='real')
    ax3.plot(sim_t_n, sim_str[2].data, 'r', label='sim')
    ax3.set_title(real_str[2].stats.channel)
    ax3.set_xlabel('time (s)')
    ax3.set_ylabel('velocity (m/s)')

    fig.suptitle(real_str[0].stats.station, fontsize=16)
    plt.legend()
    plt.show()
    
    """
    plt.subplot(311)
    
    spec, freqs = np.fft.rfft(real_str[0].data), np.fft.rfftfreq(real_str[0].stats.npts, real_str[0].stats.delta)
    plt.loglog(freqs, np.abs(spec), label="real", color="blue")

    spec, freqs = np.fft.rfft(sim_str[0].data), np.fft.rfftfreq(sim_str[0].stats.npts, sim_str[0].stats.delta)
    plt.loglog(freqs, np.abs(spec), label="sim", color="red")
   
    plt.subplot(312)

    spec, freqs = np.fft.rfft(real_str[1].data), np.fft.rfftfreq(real_str[1].stats.npts, real_str[1].stats.delta)
    plt.loglog(freqs, np.abs(spec), label="real", color="blue")

    spec, freqs = np.fft.rfft(sim_str[1].data), np.fft.rfftfreq(sim_str[1].stats.npts, sim_str[1].stats.delta)
    plt.loglog(freqs, np.abs(spec), label="sim", color="red")

    plt.subplot(313)

    spec, freqs = np.fft.rfft(real_str[2].data), np.fft.rfftfreq(real_str[2].stats.npts, real_str[2].stats.delta)
    plt.loglog(freqs, np.abs(spec), label="real", color="blue")

    spec, freqs = np.fft.rfft(sim_str[2].data), np.fft.rfftfreq(sim_str[2].stats.npts, sim_str[2].stats.delta)
    plt.loglog(freqs, np.abs(spec), label="sim", color="red")
    
    plt.suptitle(real_str[0].stats.station)
    plt.legend()
    plt.show()
    """
  
"""
plt.figure(1)
record = recievers[0].getSubRecord(real_t_ini, real_t_fin, int(real_t_steps*1.0))
plt.plot(recievers[0].record, 'r')
record = recievers[int(num_recievers*0.5)].getSubRecord(real_t_ini, real_t_fin, int(real_t_steps*1.0))
plt.plot(record, 'g')
record = recievers[num_recievers-1].getSubRecord(real_t_ini, real_t_fin, int(real_t_steps*1.0))
plt.plot(record, 'b')
plt.show()
"""
