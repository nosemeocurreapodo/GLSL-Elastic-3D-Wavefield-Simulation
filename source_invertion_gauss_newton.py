import time
from matplotlib import pyplot as plt
import numpy as np
import copy

import obspy
from obspy.core import UTCDateTime

import src.elastic_3D_GL as elastic_3D_GL
import src.source as source
import src.reciever as reciever
import src.dataReader as dataReader
import src.invertion_helpers as invertion_helpers

num_iterations = 100

[recievers, sources, veltable, params] = dataReader.getData()

max_vel = 0
min_vel = 10000000000000000
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
for source_init in sources:    

  print("inverting new source")
  
  sim_wavefield.setSimulationTime(source_init)

  real_strs = []    
  for i in range(0,len(recievers)):
    real_str = recievers[i].readStream(source_init.time, sim_wavefield.sim_params.starttime, sim_wavefield.sim_params.endtime) 
    if real_str == None:
      continue    
    real_strs.append(real_str)
  
  if len(real_strs) != len(recievers):
    print("something wrong while reading the streams, skipping this earthquake")
    continue
 
  filename = "output/" + source_init.time.format_arclink() + ".txt"
  #filename = "source_invertion_out_2.txt"
  file = open(filename, "w+")
      
  best_source = copy.deepcopy(source_init)
  
  sim_wavefield.updateSource(best_source)
  best_strs = sim_wavefield.simulate()

  real_filt_strs = []    
  for i in range(0,len(best_strs)):
    best_str = best_strs[i]
    real_filt_str =  copy.deepcopy(real_strs[i])

    sim_wavefield.filterStream(real_filt_str,0)
    sim_wavefield.filterStream(best_str,0)
  
    real_filt_strs.append(real_filt_str)
    
  best_error_strs = invertion_helpers.calculateErrorStrs(best_strs,real_filt_strs)
  best_MSE = invertion_helpers.calculateMSE(best_error_strs)

  it = 0  

  gradient = np.zeros(10)
  hessian = np.zeros((10,10))
    
  while it < num_iterations:
  
    if it > 0:

      gradient.fill(0.0)
      hessian.fill(0.0)

      mt_only = False
      if it == 1: 
        mt_only = True
 
      derivative_strss = sim_wavefield.calculateSourceDerivative(real_filt_strs, best_strs, best_source, mt_only)
    
      #por cada estacion
      for i in range(0,len(best_error_strs)):
        #por cada componente
        for j in range(0,3):
          steps = best_error_strs[i][j].stats.npts 
          #por cada parametro
          for k in range(0,len(derivative_strss)):
            gradient[k] += best_error_strs[i][j].data[0:steps].dot(derivative_strss[k][i][j].data[0:steps])
            #por parametro
            for l in range(0,len(derivative_strss)):
              hessian[k,l] += (derivative_strss[k][i][j].data[0:steps]).dot(derivative_strss[l][i][j].data[0:steps])

      #gradient = gradient/(len(best_error_strs)*3*best_error_strs[0][0].stats.npts)
      #hessian = hessian/(len(best_error_strs)*3*best_error_strs[0][0].stats.npts)
      
      """
      if it > 1:
        hessian_diag = abs(np.diag(hessian[4:10]))
        print("hessian_diag: ", hessian_diag)
        cova = 1.0/hessian_diag
        print("cova: ", cova)
        max_cova = np.amax(cova)
        min_cova = np.amin(cova)
        weight = 0.1*(cova - min_cova)/(max_cova - min_cova)
        print("weigth: ", weight)
        weight = weight*hessian_diag
        print("weight 2: ", weight)
        #gradient[0]  += weight[0]*(best_source.time  - source_init.time)
        #gradient[1]  += weight[1]*(best_source.lat   - source_init.lat) 
        #gradient[2]  += weight[2]*(best_source.lon   - source_init.lon)   
        #gradient[3]  += weight[3]*(best_source.depth - source_init.depth)
        gradient[4]  += weight[0]*(best_source.mxx)
        gradient[5]  += weight[1]*(best_source.myy)  
        gradient[6]  += weight[2]*(best_source.mzz)    
        gradient[7]  += weight[3]*(best_source.mxy)
        gradient[8]  += weight[4]*(best_source.mxz)  
        gradient[9]  += weight[5]*(best_source.myz)    
        #hessian[0,0] += weight[0]
        #hessian[1,1] += weight[1]
        #hessian[2,2] += weight[2]
        #hessian[3,3] += weight[3]     
        hessian[4,4] += weight[0]
        hessian[5,5] += weight[1]
        hessian[6,6] += weight[2]
        hessian[7,7] += weight[3]
        hessian[8,8] += weight[4]
        hessian[9,9] += weight[5]
      """
      
      lam = 0
      n_try = 0
      
      while(True):
        #print("gradient ", gradient)
        #print("lambda ", lam)
        #delta_estimate = -(1000.0*gradient/np.linalg.norm(gradient))/(lam+1.0)
        diag = np.diag(np.diag(hessian))*lam
        [delta_source, residuals, rank, s] = np.linalg.lstsq(hessian + diag, gradient, rcond=None)  
        
        #print("x: ", delta_source) 
        #print("residuals: ", residuals)
        print("hessian rank: ", rank) 
        #print("s: ",s)        
    
        new_source = copy.deepcopy(best_source)
        new_source.time -= delta_source[0]
        new_source.lat -= delta_source[1]
        new_source.lon -= delta_source[2]
        new_source.depth -= delta_source[3]
        new_source.mxx -= delta_source[4]
        new_source.myy -= delta_source[5]
        new_source.mzz -= delta_source[6]
        new_source.mxy -= delta_source[7]
        new_source.mxz -= delta_source[8]
        new_source.myz -= delta_source[9]
        #print("delta estimate ", delta_estimate)
        #print("best estimate ", best_estimate)
        #print("new estimate ", new_estimate)
        
        #force pure dc solution 
        if new_source.isDC == True:        
          if abs(new_source.mxx) > abs(new_source.myy) and abs(new_source.mxx) > abs(new_source.mzz):
            if abs(new_source.myy) > abs(new_source.mzz):
              new_source.myy = -new_source.mxx
              new_source.mzz = 0.0
            else:
              new_source.mzz = -new_source.mxx
              new_source.myy = 0.0
          if abs(new_source.myy) > abs(new_source.mxx) and abs(new_source.myy) > abs(new_source.mzz):
            if abs(new_source.mxx) > abs(new_source.mzz):
              new_source.mxx = -new_source.myy
              new_source.mzz = 0.0
            else:
              new_source.mzz = -new_source.myy
              new_source.mxx = 0.0
          if abs(new_source.mzz) > abs(new_source.myy) and abs(new_source.mzz) > abs(new_source.mxx):
            if abs(new_source.myy) > abs(new_source.mxx):
              new_source.myy = -new_source.mzz
              new_source.mxx = 0.0
            else:
              new_source.mxx = -new_source.mzz
              new_source.myy = 0.0            
          
          
    
        diff_lat = sim_wavefield.sim_params.max_lat - sim_wavefield.sim_params.min_lat
        diff_lon = sim_wavefield.sim_params.max_lon - sim_wavefield.sim_params.min_lon
        diff_depth = sim_wavefield.sim_params.max_depth - sim_wavefield.sim_params.min_depth
        #print("sample ", sample)
        is_valid = True
        
        if new_source.time < sim_wavefield.sim_params.starttime + 1.5/source_init.peak_freq:
          new_source.time = sim_wavefield.sim_params.starttime + 1.5/source_init.peak_freq
        if(new_source.lat < sim_wavefield.sim_params.min_lat + diff_lat*0.1 or new_source.lat > sim_wavefield.sim_params.max_lat - diff_lat*0.1):
          is_valid = False
        if(new_source.lon < sim_wavefield.sim_params.min_lon + diff_lon*0.1 or new_source.lon > sim_wavefield.sim_params.max_lon - diff_lon*0.1):
          is_valid = False
        #if(new_estimate[2] < sim_wavefield.sim_params.ini_corner[2] + diff[2]*0.1 or new_estimate[2] > sim_wavefield.sim_params.fin_corner[2] - diff[2]*0.1):
        #  is_valid = False
        if new_source.depth < 0.0: 
          new_source.depth = 0.0
        if(new_source.depth > sim_wavefield.sim_params.max_depth - diff_depth*0.1):
          is_valid = False
          
        if(is_valid == True):

          sim_wavefield.updateSource(new_source)  
          new_strs = sim_wavefield.simulate()
  
          real_filt_strs = []
          for i in range(0,len(new_strs)):
            real_filt_str =  copy.deepcopy(real_strs[i])
            sim_wavefield.filterStream(real_filt_str,0)
            sim_wavefield.filterStream(new_strs[i],0)
            real_filt_strs.append(real_filt_str)

          new_error_strs = invertion_helpers.calculateErrorStrs(new_strs,real_filt_strs)
          new_MSE = invertion_helpers.calculateMSE(new_error_strs)
        else:
          print("invalid!")
          new_MSE = 1000000000000000000000000000.0    
     
        if(new_MSE < best_MSE):
          print("**************************")
          print("update accepted")
          print("n_try ", n_try, " lambda ", lam)
          print("**************************")

          p = new_MSE/best_MSE

          best_source = copy.deepcopy(new_source)
          best_MSE = new_MSE
          best_strs = copy.deepcopy(new_strs)
          best_error_strs = copy.deepcopy(new_error_strs)

          if lam < 0.2:
            lam = 0.0
          else:
            lam *= 0.5
        
          if p > 0.999:
            print("**************************")
            print("error too small, converged!")
            print("n_try ", n_try, " lambda ", lam)
            print("**************************")
            it = num_iterations+1	
                  
          break

        else:
          print("**************************")
          print("update rejected")
          print("MSE ", new_MSE)
          print("lambda ", lam)
          print("**************************")

          if lam == 0.0:
            lam = 0.2;
          else:
            lam *= 2.0**n_try;
          n_try+=1

      
          if(np.linalg.norm(delta_source) < 1e-32):
            print("**************************")
            print("update too small, converged!")
            print("n_try ", n_try, " lambda ", lam)
            print("**************************")
            it = num_iterations+1
            break
      
        
    print("iteration ", it)
    print("MSE ", best_MSE)
    print("time: ", best_source.time)
    print("loc: ", best_source.lat, " ", best_source.lon, " ", best_source.depth)
    print("peak freq: ", best_source.peak_freq)
    print("isDC: ", best_source.isDC)
    print("mt: ", best_source.mxx*best_source.mt_scale, " ",best_source.myy*best_source.mt_scale, " ", best_source.mzz*best_source.mt_scale, " ", best_source.mxy*best_source.mt_scale, " ", best_source.mxz*best_source.mt_scale, " ", best_source.myz*best_source.mt_scale)
    #print("cova", new_cova)
    
    file.write("iteration %d \n" % it)
    file.write("error(mse) %1.8e \n" % best_MSE)
    #file.write("maxmt %1.8e \n" % mt_exp)
    time_est = best_source.time
    seconds = time_est.second + time_est.microsecond/1000000.0
    #file.write("time: %s \n" % time_est) 
    file.write("time: ")
    file.write(" %d " % time_est.year) 
    file.write(" %d " % time_est.month)
    file.write(" %d " % time_est.day) 
    file.write(" %d " % time_est.hour)
    file.write(" %d " % time_est.minute)
    file.write(" %1.8e " % seconds) 
    file.write("\n")    
    file.write("loc: ")
    #best_estimate[1:4].tofile(file, sep=" ", format='%1.8e')
    file.write(" %1.8e " % best_source.lat)
    file.write(" %1.8e " % best_source.lon)
    depth_est = best_source.depth/1000.0
    file.write(" %1.8e " % depth_est)
    file.write("\n")
    file.write("peak_freq: %1.8e \n" % best_source.peak_freq)
    file.write("mt: ")
    #(best_estimate[4:10]*mt_exp).tofile(file, sep=" ", format='%1.8e')
    file.write(" %1.8e " % float(best_source.mxx*best_source.mt_scale))
    file.write(" %1.8e " % float(best_source.myy*best_source.mt_scale))
    file.write(" %1.8e " % float(best_source.mzz*best_source.mt_scale))
    file.write(" %1.8e " % float(best_source.mxy*best_source.mt_scale))
    file.write(" %1.8e " % float(best_source.mxz*best_source.mt_scale))
    file.write(" %1.8e " % float(best_source.myz*best_source.mt_scale))
    file.write("\n")
    file.write("hessian: ")
    hessian.tofile(file, sep=" ", format='%1.8e')
    file.write("\n")  

    it+=1
  
  if False:
    for i in range(0, len(real_filt_strs)):
      real_str = real_filt_strs[i]
      best_str = best_strs[i]

      real_t_e = np.linspace(0.0, real_str[0].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[0].stats.npts)
      sim_t_e = np.linspace(0.0, best_str[0].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, best_str[0].stats.npts)
      real_t_n = np.linspace(0.0, real_str[1].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[1].stats.npts)
      sim_t_n = np.linspace(0.0, best_str[1].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, best_str[1].stats.npts)
      real_t_z = np.linspace(0.0, real_str[2].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, real_str[2].stats.npts)
      sim_t_z = np.linspace(0.0, best_str[2].stats.endtime.timestamp-real_str[0].stats.starttime.timestamp, best_str[2].stats.npts)  
  
      fig, (ax1, ax2, ax3) = plt.subplots(3, 1, constrained_layout=True, sharey=True)
      ax1.plot(real_t_n, real_str[0].data, 'b', label='real')
      ax1.plot(sim_t_n, best_str[0].data, 'r', label='sim')
      ax1.set_title(real_str[0].stats.channel)
      ax1.set_xlabel('time (s)')
      ax1.set_ylabel('velocity (m/s)')

      ax2.plot(real_t_n, real_str[1].data, 'b', label='real')
      ax2.plot(sim_t_n, best_str[1].data, 'r', label='sim')
      ax2.set_title(real_str[1].stats.channel)
      ax2.set_xlabel('time (s)')
      ax2.set_ylabel('velocity (m/s)')
    
      ax3.plot(real_t_n, real_str[2].data, 'b', label='real')
      ax3.plot(sim_t_n, best_str[2].data, 'r', label='sim')
      ax3.set_title(real_str[2].stats.channel)
      ax3.set_xlabel('time (s)')
      ax3.set_ylabel('velocity (m/s)')

      fig.suptitle(real_str[0].stats.station, fontsize=16)
    plt.legend()
    plt.show()
