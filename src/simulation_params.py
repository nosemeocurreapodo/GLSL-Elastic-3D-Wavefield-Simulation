import numpy as np                  # all matrix manipulations & OpenGL args
import obspy
import math

class simulation_params:
  def __init__(self, stationList, sourceList, max_medium_vel, min_medium_vel, input_params):
  
    #select simulation corners analizing the sources and the stations locations

    req_frec = input_params[0]
    print("requested frequency (in hertz) ", req_frec)
    
    med_size = input_params[1]    
    print("size of medium (in steps) ", med_size)
        
    min_lat = stationList[0].lat
    min_lon = stationList[0].lon
    min_depth = stationList[0].depth

    max_lat = stationList[0].lat
    max_lon = stationList[0].lon
    max_depth = stationList[0].depth
      
    for s in stationList:
      
      if s.lat < min_lat:
        min_lat = s.lat
      if s.lon < min_lon:
        min_lon = s.lon  
      if s.depth < min_depth:
        min_depth = s.depth  
        
      if s.lat > max_lat:
        max_lat = s.lat
      if s.lon > max_lon:
        max_lon = s.lon 
      if s.depth > max_depth:
        max_depth = s.depth 

    for s in sourceList:
      
      if s.lat < min_lat:
        min_lat = s.lat
      if s.lon < min_lon:
        min_lon = s.lon  
      if s.depth < min_depth:
        min_depth = s.depth  
        
      if s.lat > max_lat:
        max_lat = s.lat
      if s.lon > max_lon:
        max_lon = s.lon 
      if s.depth > max_depth:
        max_depth = s.depth 
        
    lat_diff = max_lat - min_lat
    lon_diff = max_lon - min_lon
    depth_diff = max_depth - min_depth
    
    min_lat -= lat_diff*0.25
    min_lon -= lon_diff*0.25
    #min_depth -= depth_diff*0.5

    max_lat += lat_diff*0.25
    max_lon += lon_diff*0.25
    #max_depth += depth_diff*4.0
    
    xlen = obspy.geodetics.base.gps2dist_azimuth(min_lat, min_lon, max_lat, min_lon)[0]
    ylen = obspy.geodetics.base.gps2dist_azimuth(min_lat, min_lon, min_lat, max_lon)[0]
    zlen = max(depth_diff*2.0,max(xlen,ylen)/4.0)*1.1
    
    min_depth = min_depth - zlen*0.1
    max_depth = min_depth + zlen
    
    print("simulation initial coordinates: ", min_lat, " ", min_lon, " ", min_depth)
    print("simulation final coordinates: ", max_lat, " ", max_lon, " ", max_depth)     
    print("size of simulation (in m) ", xlen, ylen, zlen)

    print("max medium vel: ", max_medium_vel)
    print("min medium vel: ", min_medium_vel)
    
    max_dxyz = 1.0*min_medium_vel/(5.0*req_frec)
    min_dxyz = min(max_dxyz, 1000.0) #set a (max) minimun dxyz of 1 km in depth
    print("max dxyz ", max_dxyz)     

    min_sim_size = np.array([0.0,0.0,0.0])
    min_sim_size[0] = xlen/max_dxyz
    min_sim_size[1] = ylen/max_dxyz
    min_sim_size[2] = zlen/min_dxyz

    print("min simulation size (in steps): ", min_sim_size)
    
    """
    x_exponent = 0
    y_exponent = 0
    z_exponent = 0
    while True:
      if min_sim_size[0] < 2**x_exponent:
        break
      x_exponent += 1
    while True:    
      if min_sim_size[1] < 2**y_exponent:
        break
      y_exponent += 1
    while True:  
      if min_sim_size[2] < 2**z_exponent:
        break
      z_exponent += 1
    
    if x_exponent < 5:
      x_exponent = 5
    if y_exponent < 5:
      y_exponent = 5
    if z_exponent < 5:
      z_exponent = 5

    sim_size = np.array([0,0,0])
    sim_size[0] = 2**x_exponent
    sim_size[1] = 2**y_exponent
    sim_size[2] = 2**z_exponent
    """

    sim_size = np.around(min_sim_size).astype(int)
        
    print("simulation size (in steps): ", sim_size) 

    dxyz = np.zeros((3))
    dxyz[0] = xlen/sim_size[0]
    dxyz[1] = ylen/sim_size[1]
    dxyz[2] = zlen/sim_size[2]    
    
    print("simulation dxyz (in m): ", dxyz)     
    
    max_frec = 1.0*min_medium_vel/(5.0*np.amax(dxyz))
    print("max frec ", max_frec)   
    
    #re calculate ini_corner and fin_corner
    
    #self.zeroLevel = 0.25
    #min_depth = -dxyz[2]*sim_size[2]*self.zeroLevel
    #max_depth = dxyz[2]*sim_size[2]*(1.0-self.zeroLevel)

    #max_depth = min_depth + zlen
    
    # la superficiel real, usada en la simulacion
    # justo en el medio del pixel de superficie de los parametros de lame
    #self.surface = self.surface + 0.5/mediumParamSize[2]   

    self.min_medium_vel = min_medium_vel
    self.max_medium_vel = max_medium_vel    
    
    self.min_lat = min_lat
    self.min_lon = min_lon
    self.min_depth = min_depth
    
    self.max_lat = max_lat
    self.max_lon = max_lon
    self.max_depth = max_depth
  
    self.sim_size = sim_size
    
    self.med_size = med_size
  
    self.xyzlen = np.array([xlen, ylen, zlen])
      
    self.dxyz = dxyz
    
    self.dlat = (max_lat-min_lat)/sim_size[0]
    self.dlon = (max_lon-min_lon)/sim_size[1]    
    self.ddepth = (max_depth-min_depth)/sim_size[2] 
    
    #print("dlat: ",self.dlat)
    #print("dlon: ",self.dlon)
    #print("ddepth: ",self.ddepth)
        
    max_dt = 0.495*np.amin(dxyz)/max_medium_vel
    #max_dt = 0.577*np.min(dxyz)/max_medium_vel
    print("max dt ", max_dt)
    """
    t_exponent = 5
    while True:
      if (max_dt > 5**t_exponent):
        break
      t_exponent -= 1
    """ 

    t_exponent = 0
    while True:
      if (0 < math.trunc(max_dt*(10.0**t_exponent))):
        break
      t_exponent += 1
      
    #dt = math.trunc(max_dt*aux)/aux)
    #dt = 5**(t_exponent)
    dt = math.trunc(max_dt*(10.0**t_exponent))*10.0**(-t_exponent) 
    print("simulation dt: ", dt)
    
    self.max_frec = max_frec
    self.req_frec = req_frec
    self.dt = dt
        
    self.starttime = None
    self.endtime = None
    self.t_steps = None
    self.max_peak_freq = None
    self.min_peak_freq = None
    
    self.decimation_factor = None
    self.rec_dt = None

    #self.setSimulationTime(sourceList)

  def setSimulationTime(self, sourceList):
    
    self.starttime = None
    self.endtime = None
    self.max_peak_freq = None
    self.min_peak_freq = None
    self.t_steps = None
    
    for source in sourceList:
      sourcetime = source.time #obspy.UTCDateTime(source.time.year, source.time.month, source.time.day, source.time.hour, source.time.minute, int(source.time.second))
      peak_freq = source.peak_freq
      if self.starttime == None:
        self.starttime = sourcetime
        self.endtime = sourcetime
        self.max_peak_freq = peak_freq
        self.min_peak_freq = peak_freq
        continue
      
      if sourcetime < self.starttime:
        self.starttime = sourcetime
      if sourcetime > self.endtime:
        self.endtime = sourcetime
      if peak_freq > self.max_peak_freq:
        self.max_peak_freq = peak_freq
      if peak_freq < self.min_peak_freq:
        self.min_peak_freq = peak_freq      

    self.starttime = self.starttime - 2.0/self.min_peak_freq
    #self.endtime = self.endtime + self.dt*int((15.0/(self.min_source_frec))/self.dt) #self.dt*int(sourceList[0].codatime/self.dt)  
    self.endtime = self.endtime + 0.5*np.amax(self.xyzlen)/self.min_medium_vel + 2.0/self.min_peak_freq
    self.t_steps = round((self.endtime-self.starttime)/self.dt)

    self.decimation_factor = 1
    self.rec_dt = self.dt*self.decimation_factor
    
    print("decimation ", self.decimation_factor)
    print("reciever dt ", self.rec_dt)
    
    print("starttime ", self.starttime)
    print("endtime ", self.endtime)
    print("steps ", self.t_steps)  
    
    
  def latlondepth2simulation(self, lat, lon, depth):
    x = (lat - self.min_lat)/self.dlat
    y = (lon - self.min_lon)/self.dlon
    z = (depth - self.min_depth)/self.ddepth
    return np.array([x,y,z])
    
  def latlondepth2simulation_normalized(self, lat, lon, depth):
    x = (lat - self.min_lat)/(self.max_lat-self.min_lat)
    y = (lon - self.min_lon)/(self.max_lon-self.min_lon)
    z = (depth - self.min_depth)/(self.max_depth-self.min_depth)
    return np.array([x,y,z])

  def latlondepth2meters(self, lat, lon, depth):
    x = self.dxyz[0]*(lat - self.min_lat)/self.dlat
    y = self.dxyz[1]*(lon - self.min_lon)/self.dlon
    z = self.dxyz[2]*(depth - self.min_depth)/self.ddepth
    return np.array([x,y,z])
    
  def simulation2latlondepth(self, sim):
    lat   =  self.dlat*sim[0]   + self.min_lat
    lon   =  self.dlon*sim[1]   + self.min_lon
    depth =  self.ddepth*sim[2] + self.min_depth
    return [lat,lon,depth]
    
  def simulation_normalized2latlondepth(self, sim):
    lat   =  self.dlat*sim[0]*self.sim_size[0]   + self.min_lat
    lon   =  self.dlon*sim[1]*self.sim_size[1]   + self.min_lon
    depth =  self.ddepth*sim[2]*self.sim_size[2] + self.min_depth
    return [lat,lon,depth]    
    
