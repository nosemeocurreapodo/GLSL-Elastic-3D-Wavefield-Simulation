import numpy as np

from obspy.core import UTCDateTime


class source:
  def __init__(self, pos, time, mt):

    self.pos = pos   
    self.time = time
    self.mt = mt
    
    #time = UTCDateTime(2012, 9, 7, 12, 15, 0)
    #print(time)
    #time += 0.1
    #print(time)


    
