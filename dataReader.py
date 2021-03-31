import numpy as np
import cv2

from matplotlib import pyplot as plt

import obspy
from obspy import read
from obspy.core import UTCDateTime
from obspy.clients.fdsn import Client

from obspy.signal.invsim import corn_freq_2_paz

import reciever
import source

def getCubaData():

  f = open("./data/Cuba/network_caribe.stn", "r")	
  
  flines = f.readlines()
  print("reading station file...")
  
  stationList = []
  
  for line in flines[:]:
  
    words = line.split()
  
    lat = float(words[1])
    lon = float(words[2])
    depth = -float(words[3]) #metros
    name = words[0]
    network = ""
    
    print("Station: ", name, " lon: ", lon, " lat: ", lat, " depth: ", depth)
        
    stationList.append(reciever.reciever(network, name, np.array([lat, lon, depth])))
  print("done reading station file!")

  sourceList = []
  
  print("reading moment tensor data...")
  
  year = 2016
  month = 1
  day = 17
  hour = 8
  minute = 30
  seconds = 23+2.08 #centroid time
    
  time = UTCDateTime(year, month, day, hour, minute, seconds)
       
  lon = -76.09
  lat = 19.749
  depth = 7000.0 #a metros
  
  mt = np.zeros(6).astype(np.float32)
  #nn ee dd ne nd ed
  #[-237175357293957.12, -4.3148834231687064e+16, 4.338600958898102e+16, -3393454996110781.0, -779314042168291.0, 4607153448370924.0]
  
  #xx yy zz xy xz yz
  
  mt[0] = -2.3717535729395712e+14  #supuestamente, el tensor momento esta en kg*m^2/s^2, osea N*m
  mt[1] = -4.3148834231687064e+16
  mt[2] = 4.338600958898102e+16
  mt[3] = -3.393454996110781e+15
  mt[4] = -7.79314042168291e+14
  mt[5] = 4.607153448370924e+15
  
  #print("sismo ")
  #print("time: ", time)
  #print("lon: ", lon, " lat: ", lat, " depth: ", depth)
  #print("mt: ", mt)
      
  sourceList.append(source.source(np.array([lat,lon,depth]),time,mt))
    
  sourceList[len(sourceList)-1].mt = mt.copy()
      
  #print("lon: ", lon, " lat: ", lat, " depth: ", depth, " time: ", time )
  print("done reading moment tensor data!") 
  
  
      #depth of layer top(km)   Vp(km/s)    Vs(km/s)    Rho(g/cm**3)    Qp     Qs
    #  0.0                 4.90       2.816        2.500         176     64
    #  3.0                 5.40       3.103        2.600         176     64
    #  5.0                 6.00       3.448        2.700         176     64
    #  7.0                 6.90       3.966        2.800         450    220
    # 20.0                 7.60       4.368        3.100         500    250
    # 26.0                 7.80       4.483        3.260         550    270
    # 34.0                 8.00       4.598        3.300         600    300


  veltable = np.zeros((7, 6))
  veltable[0,:] = np.array([0.0, 4.9, 2.816, 2.5, 176, 64]) 
  veltable[1,:] = np.array([3.0, 5.4, 3.103, 2.6, 176, 64])
  veltable[2,:] = np.array([5.0, 6.0, 3.448, 2.7, 176, 64])
  veltable[3,:] = np.array([7.0, 6.9, 3.966, 2.8, 450, 220])
  veltable[4,:] = np.array([20.0, 7.6, 4.368, 3.1, 500, 250])
  veltable[5,:] = np.array([26.0, 7.8, 4.483, 3.26, 550, 270])
  veltable[6,:] = np.array([34.0, 8.0, 4.598, 3.3, 600, 300])         
  
  return stationList, sourceList, veltable
 
def getCubaRealTrace(station,channel,starttime,endtime):

  #print("getting real trace")
  #print(station)
  #print(channel)
  
  file = "./data/Cuba/data_SAC/"+station+channel+".sac"
  #file = "E:\msnoise\data\A2014\WA\FRACK\HHE.D\WA.FRACK.HHE_20141219_103000.miniseed"
  st = read(file,starttime=starttime,endtime=endtime, nearest_sample=True)
 
  pzfile = "./data/Cuba/pzfiles/"+station+channel+".pz"
  f = open(pzfile, "r")	
  
  flines = f.readlines()
  #print("reading station file...")
  
  A0 = float(flines[1])
  sens = 1.0/float(flines[3])
  #print("A0 ", A0)
  #print("sens ", sens)
  numzeros = int(flines[5])
  #print("zeros ", numzeros)
  zeros = []
  pos = 5+1
  for i in range(0, numzeros):
    words = flines[pos+i].split()
    zero = float(words[0])+float(words[1])*1j
    #zero = float(words[0])*2*np.pi+float(words[1])*1j*2*np.pi #de radianes a frec   
    #zero = float(words[0])/(2*np.pi)+float(words[1])*1j/(2*np.pi)    
    zeros.append(zero)
  #print(zeros)

  pos = pos + numzeros + 1
  numpoles = int(flines[pos])
  #print("poles ", numpoles)
  poles = []
  pos = pos + 1
  for i in range(0, numpoles):
    words = flines[pos+i].split()
    pole = float(words[0])+float(words[1])*1j
    #pole = float(words[0])*2*np.pi+float(words[1])*1j*2*np.pi
    #pole = float(words[0])/(2*np.pi)+float(words[1])*1j/(2*np.pi)
    poles.append(pole)
  #print(poles)
  
  
  paz_sts2 = {
    'poles' : poles,
    'zeros': zeros,
    'gain': A0,
    'sensitivity': sens}
    
  """
  paz_sts2 = {
    'poles': [],
    'zeros': zeros,
    'gain': 60077000.0,
    'sensitivity': 2516778400.0}
  """  
  #print(paz_sts2)
  
  st_rf = st.copy()
  
  #pre_filt = (0.005, 0.006, 0.1, 0.2)
  pre_filt = (0.005, 0.006, 30.0, 35.0)
  #pre_filt = (0.005, 0.006, max_frec, max_frec*1.5)
  
  st_rf.simulate(paz_remove=paz_sts2,  pre_filt=pre_filt)
  
  #invert east component of GTBY
  if station == "GTBY" and channel == "e":
    st_rf[0].data = -st_rf[0].data
 

  #complete trace with zeros
  zero_tr = st_rf.copy()
  zero_tr[0].stats.starttime = starttime
  zero_tr[0].stats.npts = 10
  zero_tr[0].data = np.zeros(zero_tr[0].stats.npts)
  
  zero_tr_2 = st_rf.copy()
  zero_tr_2[0].stats.starttime = endtime
  zero_tr_2[0].stats.npts = 1
  zero_tr_2[0].data = np.zeros(zero_tr[0].stats.npts)
  
  new_str = obspy.Stream()
  
  new_str += zero_tr
  new_str += zero_tr_2
  new_str += st_rf
  
  new_str.merge(method=1, fill_value='interpolate')
 
  return new_str[0]
  
 
