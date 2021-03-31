"""
CHIV
error  0.0427919417428   0.0948813776284   0.0529307986438
RCC
error  0.0556504932158   0.0646166717912   0.167959643306
LMGC
error  0.18391888841   0.417178442322   0.100290034779
GTBY
error  0.154504026872   0.227230603467   0.0759147786518
MASC
error  0.214617753723   0.0799111886055   0.115626924265
CCCC
error  0.21617905458   0.0817558338567   0.182178466064
MTDJ
error  0.205081570633   0.388936964751   0.259278217253
LGNH
error  0.202588226223   0.157298298806   0.244491747127
"""

"""
import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
IT = [0.0427919417428, 0.0556504932158, 0.18391888841, 0.154504026872, 0.214617753723, 0.21617905458, 0.205081570633, 0.202588226223]
ECE = [0.0948813776284, 0.0646166717912, 0.417178442322, 0.227230603467, 0.0799111886055, 0.0817558338567, 0.388936964751, 0.157298298806]
CSE = [0.0529307986438, 0.167959643306, 0.100290034779, 0.0759147786518, 0.115626924265, 0.182178466064, 0.259278217253, 0.244491747127]
 
# Set position of bar on X axis
br1 = np.arange(len(IT))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
 
# Make the plot
plt.bar(br1, IT, color ='r', width = barWidth,
        edgecolor ='grey', label ='north')
plt.bar(br2, ECE, color ='g', width = barWidth,
        edgecolor ='grey', label ='east')
plt.bar(br3, CSE, color ='b', width = barWidth,
        edgecolor ='grey', label ='down')
 
# Adding Xticks
plt.xlabel('Stations', fontweight ='bold', fontsize = 15)
plt.ylabel('Error (%)', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(IT))],
        ['CHIV', 'RCC', 'LMGC', 'GTBY', 'MASC', 'CCCC', 'MTDJ', 'LGNH'])
 
plt.legend()
plt.show()
"""

"""
CHIV
rms error  1.01456120767e-06
p error  0.063534706005
p error  0.0427919417428   0.0948813776284   0.0529307986438
RCC
rms error  1.32332739356e-06
p error  0.0960756027712
p error  0.0556504932158   0.0646166717912   0.167959643306
LMGC
rms error  1.03550732828e-06
p error  0.233795788503
p error  0.18391888841   0.417178442322   0.100290034779
GTBY
rms error  1.01696285131e-06
p error  0.152549802997
p error  0.154504026872   0.227230603467   0.0759147786518
MASC
rms error  6.91970512322e-07
p error  0.136718622198
p error  0.214617753723   0.0799111886055   0.115626924265
CCCC
rms error  8.93483260084e-07
p error  0.160037784834
p error  0.21617905458   0.0817558338567   0.182178466064
MTDJ
rms error  1.35396907218e-06
p error  0.284432250879
p error  0.205081570633   0.388936964751   0.259278217253
LGNH
rms error  9.76139926156e-07
p error  0.201459424052
p error  0.202588226223   0.157298298806   0.244491747127
"""

import matplotlib.pyplot as plt
fig = plt.figure()
langs = ['CHIV', 'RCC', 'LMGC', 'GTBY', 'MASC', 'CCCC', 'MTDJ', 'LGNH']
students = [1.01456120767e-06,1.32332739356e-06,1.03550732828e-06,1.01696285131e-06,6.91970512322e-07,8.93483260084e-07,1.35396907218e-06,9.76139926156e-07]
plt.bar(langs,students)
plt.xlabel('Stations', fontweight ='bold', fontsize = 15)
plt.ylabel('Error (rms)', fontweight ='bold', fontsize = 15)
plt.legend()
plt.show()

import matplotlib.pyplot as plt
fig = plt.figure()
langs = ['CHIV', 'RCC', 'LMGC', 'GTBY', 'MASC', 'CCCC', 'MTDJ', 'LGNH']
students = [0.063534706005,0.0960756027712,0.233795788503,0.152549802997,0.136718622198,0.160037784834,0.284432250879,0.201459424052]
plt.bar(langs,students)
plt.xlabel('Stations', fontweight ='bold', fontsize = 15)
plt.ylabel('Error (%)', fontweight ='bold', fontsize = 15)
plt.legend()
plt.show()

"""
0 & 0.0060 & 0.0015 & 4.0 \\
\hline
1 & 0.024 & 0.0022 & 10.9 \\
\hline
2 & 0.067 & 0.0041 & 16.34 \\
\hline
3 & 0.13 & 0.011 & 11.81 \\
\hline
4 & 0.25 & 0.036 & 6.94 \\
\hline
5 & 0.49 & 0.040 & 12.25 \\
\hline
6 & 1.03 & 0.087 & 11.83 \\
\hline
7 & 2.13 & 0.17 & 12.52 \\
\hline
8 & 4.35 & 0.30 & 14.5 \\
\hline
9 & 9.31 & 0.85 & 10.95 \\
\hline
10 & 21.91 & 1.75 & 12.52  \\
"""

import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
levels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
cpu_times = np.array([0.0060,0.024,0.067,0.13,0.25,0.49,1.03,2.13,4.35,9.31,21.91])
gpu_times = np.array([0.0015,0.0022,0.0041,0.011,0.036,0.040,0.087,0.17,0.30,0.85,1.75])
#cpu_times = np.log(cpu_times)
#gpu_times = np.log(gpu_times)

# Set position of bar on X axis
barWidth = 0.25
br1 = np.arange(len(cpu_times))
br2 = [x + barWidth for x in br1]

#plt.bar(br1,cpu_times)
#plt.bar(br2,gpu_times)

plt.semilogy(br1, cpu_times, 'x',  label ='CPU')
plt.semilogy(br2, gpu_times, 'o',  label ='GPU')

plt.xlabel('level of detail', fontweight ='bold', fontsize = 15)
plt.ylabel('time (seconds)', fontweight ='bold', fontsize = 15)
plt.legend()
plt.show()

import matplotlib.pyplot as plt
fig = plt.figure()
langs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
students = [4.0,10.9,16.34,11.81,6.94,12.25,11.83,12.52,14.5,10.95,12.52]
plt.bar(langs,students)
plt.xlabel('level of detail', fontweight ='bold', fontsize = 15)
plt.ylabel('Speed up', fontweight ='bold', fontsize = 15)
plt.legend()
plt.show()
