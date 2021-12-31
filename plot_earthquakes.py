import time
from matplotlib import pyplot as plt
import numpy as np
import obspy
import time as exec_time
import scipy

import pygmt

import src.source as source
import src.reciever as reciever
import src.dataReader as dataReader
import src.elastic_3D_GL as elastic_3D_GL

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

fig = pygmt.Figure()

#global plot configuration
region_lat_long = [sim_wavefield.sim_params.min_lon, sim_wavefield.sim_params.max_lon, sim_wavefield.sim_params.min_lat, sim_wavefield.sim_params.max_lat]
fig.basemap(region=region_lat_long, projection="M15c", frame=True)
#fig.coast(shorelines=True)
fig.coast(land="#666666", water="skyblue")

for station in recievers:
  fig.plot(x=station.lon, y=station.lat, style="d0.3c", color="white", pen="black")
  fig.text(text=station.name, x=station.lon, y=station.lat+0.01)

for source in sources:
  fig.plot(x=source.lon, y=source.lat, style="d0.3c", color="red", pen="black")

#fig.colorbar(frame='af+l"iteration"')
fig.show()
#fig.savefig("lat-long_plot.png")
