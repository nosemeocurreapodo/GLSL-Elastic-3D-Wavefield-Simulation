import os

import numpy as np

import obspy

class reciever:
  def __init__(self, network, name, lat, lon, depth, ntrace, etrace, ztrace, nresp, eresp, zresp):
    
    self.network = network
    self.name = name
    self.lat = lat
    self.lon = lon
    self.depth = depth
    self.ntrace = ntrace
    self.etrace = etrace
    self.ztrace = ztrace
    self.nresp = nresp
    self.eresp = eresp
    self.zresp = zresp
    
  def readStream(self,sourcetime,starttime,endtime):
    
    trn = self.readTrace(self.ntrace, self.nresp, sourcetime, starttime, endtime)    
    tre = self.readTrace(self.etrace, self.eresp, sourcetime, starttime, endtime)   
    trz = self.readTrace(self.ztrace, self.zresp, sourcetime, starttime, endtime)

    if trn == None or tre == None or trz == None:
      print("something wrong while reading stream!")
      return None      
    
    return obspy.Stream(traces=[trn, tre, trz])
    
    
  def readTrace(self, traceFile, respFile, sourcetime, starttime, endtime):
  
    st = None
    if os.path.isfile(traceFile) == False:
      for f in os.listdir(traceFile):
        tfile = os.path.join(traceFile,f)
        #print("trying string: ", tfile)
        if os.path.isfile(tfile):
          st_2 = obspy.read(tfile)
          #print("trying file: ", tfile)
          #print("with starttime: ", st_2[0].stats.starttime)
          #print("and endtime: ", st_2[0].stats.endtime)
          if st_2[0].stats.starttime < sourcetime and st_2[0].stats.endtime > sourcetime:
            #print("found stream!")
            #print("requested start/end time")
            #print(starttime)
            #print(endtime)
            #print("stream start/ent time")
            #print(st[0].stats.starttime)
            #print(st[0].stats.endtime)
            st = obspy.read(tfile, starttime=starttime, endtime=endtime,nearest_sample=True, fill_value=0.0, pad=True)
            break
          
    else: 
      #st_2 = obspy.read(traceFile)
      #print("trace starttime entime ",st_2[0].stats.starttime," ",st_2[0].stats.endtime)
      #if st_2[0].stats.starttime < starttime and st_2[0].stats.endtime > endtime:
      st = obspy.read(traceFile,starttime=starttime,endtime=endtime,nearest_sample=True, fill_value=0.0, pad=True)
    
    if st == None:
      print("readTrace fail!")
      if os.path.isfile(traceFile): 
        print("could not find a trace file")
      else:
        print("could not find a trace in folder")
      print(traceFile)
      print("with sourcetime/starttime/endtime")
      print(sourcetime)
      print(starttime)
      print(endtime)
      return st

    #detrend (make 0 mean data)
    st[0].data = st[0].data - np.mean(st[0].data)    
    
    #pre_filt = (0.005, 0.006, 30.0, 35.0)
    
    if respFile[-5:] == ".resp":  
      #print("found .resp file!")
      #print(respFile)
      seedresp = {'filename':respFile,'units':'VEL'}
      #st.simulate(paz_remove=None, pre_filt=pre_filt, seedresp=seedresp)
      st.simulate(paz_remove=None, seedresp=seedresp)
    
    if respFile[-3:] == ".pz":
      #print("resp file: ", respFile)
      paz = self.pzfileReader(respFile)
      #st.simulate(paz_remove=paz,  pre_filt=pre_filt)
      st.simulate(paz_remove=paz)
    

       
    #complete trace with zeros
    zero_tr = st[0].copy()
    #zero_tr[] = obspy.Trace()
    zero_tr.stats.starttime = starttime
    zero_tr.stats.npts = 10
    zero_tr.data = np.zeros(zero_tr.stats.npts,dtype=st[0].data.dtype)

    #print("st stats ", st[0].stats)
    #print("z stats ", zero_tr[0].stats)    
      
    zero_tr_2 = st[0].copy()
    #zero_tr_2 = obspy.Trace()
    zero_tr_2.stats.starttime = endtime
    zero_tr_2.stats.npts = 1
    zero_tr_2.data = np.zeros(zero_tr.stats.npts,dtype=st[0].data.dtype)
    
    new_str = obspy.Stream()
  
    new_str += zero_tr
    new_str += zero_tr_2
    
    new_str += st
  
    new_str.merge(method=1, fill_value='interpolate')
    
    #print("readTrace starttime and endtime:")
    #print(new_str[0].stats.starttime)
    #print(new_str[0].stats.endtime)
    
    return new_str[0]
    #return st[0]
      
  def pzfileReader(self, pzfile):  
 
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
  
  
    paz_sts = {
      'poles' : poles,
      'zeros': zeros,
      'gain': A0*sens,
      'sensitivity': 1.0}
    
    #print(paz_sts)
    
    return paz_sts    


  def addResponce(self, trace):
        
    paz = self.pzfileReader(self.nresp)
    stream = obspy.Stream(traces=[trace])
    stream.simulate(paz_remove=None,  paz_simulate=paz)
