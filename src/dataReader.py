import numpy as np

import obspy
from obspy.core import UTCDateTime

import src.reciever as reciever
import src.source as source

def getData():

  f = open("./input_files.txt", "r")	
  lines = f.readlines()
  
  print("reading input files...")
  
  network_file_name = None
  model_file_name = None
  earthquake_file_name = None
  params_file_name = None
  
  for line in lines:
    words = line.split()
    if len(words) < 1:
      continue
    if words[0] == "network:":
      network_file_name = words[1]
      print("found network file: ", network_file_name)
    if words[0] == "model:":
      model_file_name = words[1]
      print("found model file: ", model_file_name)
    if words[0] == "earthquake:":
      earthquake_file_name = words[1]
      print("found earthquake file: ", earthquake_file_name) 
    if words[0] == "params:":
      params_file_name = words[1]
      print("found params file: ", params_file_name) 
           
  if network_file_name == None:
    print("no network file found!")
    return False
  if model_file_name == None:
    print("no model file found!")
    return False
  if earthquake_file_name == None:
    print("no earthquake file found!")
    return False
  if params_file_name == None:
    print("no params file found!")
    return False

  print("reading params file: ", params_file_name)  
  
  f = open(params_file_name,"r")
  lines = f.readlines()
  
  paramsList = []
  
  for line in lines:
  
    words = line.split()

    if len(words) < 1:
      continue

    if words[0] == "max_freq:":
      max_frec = float(words[1])
      
      paramsList.append(max_frec)

    if words[0] == "med_size:":
      x_length = int(words[1])
      y_length = int(words[2])
      z_length = int(words[3])      

      paramsList.append(np.array([x_length, y_length, z_length]))

  print("max frequency: ", paramsList[0])
  print("set med size to: ", paramsList[1])

             
  print("reading network file: ", network_file_name)  
  
  f = open(network_file_name,"r")
  lines = f.readlines()
  
  stationList = []
  
  name = None
  lat = None
  lon = None
  depth = None
  ntrace = None
  etrace = None
  ztrace = None
  nresp = None
  eresp = None
  zresp = None
  
  
  for line in lines:
  
    words = line.split()
  
    if len(words) < 1:
      continue
  
    if words[0] == "name:":
      if name != None:
        print("found new station name, but previous station data was incomplete, discarding previous station data")
        lat = None
        lon = None
        depth = None
        ntrace = None
        etrace = None
        ztrace = None
        nresp = None
        eresp = None
        zresp = None
      name = words[1]
    if words[0] == "loc:":
      if name == None:
        print("found location data but no station name given, ignoring")
        continue
      if lat != None:
        print("found second lat data in station ", name, " ignoring")
        continue
      lat = float(words[1])
      lon = float(words[2])
      depth = -float(words[3])*1000.0 #km to meters and altitude to depth
    if words[0] == "ntrace:":
      ntrace = words[1]
    if words[0] == "etrace:":
      etrace = words[1]
    if words[0] == "ztrace:":
      ztrace = words[1]
    if words[0] == "nresp:":
      nresp = words[1]
    if words[0] == "eresp:":
      eresp = words[1]
    if words[0] == "zresp:":
      zresp = words[1]
      
    if name != None and lat != None and lon != None and depth != None and ntrace != None and etrace != None and ztrace != None and nresp != None and eresp != None and zresp != None:
                     
      print("station: ", name, " lat: ", lat, " lon: ", lon, " depth: ", depth)
      print("trace files ")
      print(ntrace)
      print(etrace)
      print(ztrace)
      print("instrument responce files")
      print(nresp)
      print(eresp)
      print(zresp)
        
      stationList.append(reciever.reciever("REAL", name, lat, lon, depth, ntrace, etrace, ztrace, nresp, eresp, zresp))
      
      name = None
      lat = None
      lon = None
      depth = None
      ntrace = None
      etrace = None
      ztrace = None
      nresp = None
      eresp = None
      zresp = None
    
  print("done reading network file!")

  print("reading earthquake file: ", earthquake_file_name)
  f = open(earthquake_file_name)
  lines = f.readlines()
  
  sourceList = []
  
  time = UTCDateTime(1, 1, 1, 0, 0, 0.0)
  lat = 0.0
  lon = 0.0
  depth = 0.0
  
  peak_freq = 0.0
  
  mw = 0.0
  
  strike = 0.0
  deep = 0.0
  rake = 0.0
  
  mxx = 0.0
  mxy = 0.0
  mxz = 0.0
  myy = 0.0
  myz = 0.0
  mzz = 0.0
  
  isDC = False
  
  for line in lines:
    
    words = line.split()
  
    if len(words) < 1:
      continue
      
    if words[0] == "earthquake:":
      continue
    
    if words[0] == "time:":
   
      year = int(words[1])
      month = int(words[2])
      day = int(words[3])
      hour = int(words[4])
      minute = int(words[5])
      seconds = float(words[6])
    
      time = UTCDateTime(year, month, day, hour, minute, seconds)
    
    if words[0] == "loc:":
    
      lat = float(words[1])   
      lon = float(words[2]) 
      depth = float(words[3])*1000.0 #km to meters 
 
    if words[0] == "peak_freq:":
      peak_freq = float(words[1]) 
      
    if words[0] == "mt:":
      mxx = float(words[1])
      myy = float(words[2])
      mzz = float(words[3])
      mxy = float(words[4])
      mxz = float(words[5])
      myz = float(words[6])
      
    if words[0] == "isDC:":
      if words[1] == "True":
        isDC = True
      
      sourceList.append(source.source(time,lat,lon,depth,peak_freq,isDC,mxx,myy,mzz,mxy,mxz,myz))
      
      print("earthquake time: ", time, " loc: ", lat, " ", lon, " ", depth, " peak_freq: ", peak_freq, "isDC: ", isDC, " mxx: ", mxx, " myy: ", myy, " mzz: ", mzz, " mxy: ", mxy, " mxz: ", mxz, " myz: ", myz)
    
  print("reading model file: ", model_file_name)
  f = open(model_file_name)
  lines = f.readlines()
  
  velTableList = []
  
  for line in lines:
    
    words = line.split()
  
    if len(words) < 1:
      continue
    
    if words[0] == "layer:": 

      lat = float(words[1])  
      lon = float(words[2])        
      depth = float(words[3])*1000.0 #change km to meters
      vp    = float(words[4])*1000.0
      vs    = float(words[5])*1000.0
      rho   = float(words[6])*1000.0
      qp    = float(words[7])
      qs    = float(words[8])
      
      layer = np.array([lat, lon, depth, vp, vs, rho, qp, qs])
      velTableList.append(layer)
      
      print("layer: ", layer)
           
  return stationList, sourceList, velTableList, paramsList
      
