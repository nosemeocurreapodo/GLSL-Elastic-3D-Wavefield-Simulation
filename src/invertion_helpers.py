import numpy as np

import obspy
from obspy.core import UTCDateTime

import src.elastic_3D_GL as elastic_3D_GL
import src.source as source
import src.reciever as reciever

import copy
      
def calculateErrorStrs(first_strs, second_strs):
  
  error_strs = copy.deepcopy(first_strs)
  mean_error = 0.0
  mean_n = 0
  for j in range(0,len(first_strs)):
  
    first_str = first_strs[j]
    second_str = second_strs[j]
    error_str = error_strs[j]
    
    steps = min(first_str[0].stats.npts, second_str[0].stats.npts) 
    for k in range(0,3):
      error_str[k].data[0:steps] = first_str[k].data[0:steps] - second_str[k].data[0:steps]
      #mean_error += np.sum(error_str[k].data[0:steps])
      #mean_n += steps
  
  """
  mean_error = mean_error/mean_n
  for j in range(0,len(first_strs)):
    error_str = error_strs[j]
    for k in range(0,3):    
      error_str[k].data = (error_str[k].data/mean_n)/mean_error
  """    
  return error_strs

def calculateMSE(error_strs):
  """
  error_max = 0.0
  for j in range(0,len(error_strs)):
    error_str = error_strs[j]
    for k in range(0,3):
      error = error_str[k].data
      emax = np.amax(error_str[k].data)
      if emax > error_max:
        error_max = emax
  """     
  MSE = 0
  for j in range(0,len(error_strs)):
    error_str = error_strs[j]
    for k in range(0,3):
      error = error_str[k].data
      #error = error/error_max
      MSE += error.dot(error)
      
  return MSE 


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
