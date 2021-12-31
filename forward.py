import time
from matplotlib import pyplot as plt
import numpy as np
import obspy
import time as exec_time
import scipy

import src.elastic_3D_GL as elastic_3D_GL
import src.source as source
import src.reciever as reciever
import src.dataReader as dataReader
import src.invertion_helpers as invertion_helpers

[recievers, sources, veltable, params] = dataReader.getData()

max_vel = 0
min_vel = 100000000000000
for layer in veltable:
  vp_ = layer[3]
  vs_ = layer[4]
  if vp_ > max_vel:
    max_vel = vp_
  if vs_ > max_vel:
    max_vel = vs_
  if vp_ < min_vel:
    min_vel = vp_
  if vs_ < min_vel:
    min_vel = vs_
    
sim_wavefield = elastic_3D_GL.elastic_sim(recievers, sources, max_vel, min_vel, params) 
sim_wavefield.updateVelTable(veltable) 
   
for src in sources:

  sim_wavefield.setSimulationTime(src)
  sim_wavefield.updateSource(src)
  sim_strs = sim_wavefield.simulate()
  
  #print("--- %s seconds ---" % (exec_time.time() - start_time)) 
  
  real_strs = []
  for i in range(len(recievers)):

    sim_str = sim_strs[i]    
    real_str = recievers[i].readStream(src.time, sim_str[0].stats.starttime, sim_str[0].stats.endtime)
    
    for sim_tr in sim_str: 
      sim_tr.write("output/" + sim_tr.id + sim_str[0].stats.starttime.format_arclink() + ".MSEED", format="MSEED") 
    
    #print("real start/end time: ", real_str[0].stats.starttime, " ", real_str[0].stats.endtime)
    #print("sim start/end time: ", sim_str[0].stats.starttime, " ", sim_str[0].stats.endtime)
        
    sim_wavefield.filterStream(real_str, 0)
    sim_wavefield.filterStream(sim_str, 0)
    
    real_strs.append(real_str)
    
    real_t_e = np.linspace(0.0, real_str[0].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[0].stats.npts)
    sim_t_e = np.linspace(0.0, sim_str[0].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, sim_str[0].stats.npts)
    real_t_n = np.linspace(0.0, real_str[1].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[1].stats.npts)
    sim_t_n = np.linspace(0.0, sim_str[1].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, sim_str[1].stats.npts)
    real_t_z = np.linspace(0.0, real_str[2].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[2].stats.npts)
    sim_t_z = np.linspace(0.0, sim_str[2].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, sim_str[2].stats.npts)
    
      
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
    
  error_strs = invertion_helpers.calculateErrorStrs(sim_strs,real_strs)
  MSE = invertion_helpers.calculateMSE(error_strs)  
  print("MSE: ", MSE)
  