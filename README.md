# GLSL-Elastic-3D-Wavefield-Simulation

Tu espacio de almacenamiento está casi lleno (92 %). … 
Pronto no podrás subir archivos nuevos a Drive ni enviar ni recibir correos electrónicos en Gmail.Más información

HOW TO INSTALL

#For linux:
The following was tested on a fresh ubuntu 20.04.1 install

#open a terminal and run:
sudo apt install git python3-pip python-is-python3

#get the code running in a terminal:
git clone https://github.com/nosemeocurreapodo/GLSL-Elastic-3D-Wavefield-Simulation.git

#install dependencies
pip install matplotlib obspy pyopengl glfw

#For windows:

get the code from: https://github.com/nosemeocurreapodo/GLSL-Elastic-3D-Wavefield-Simulation.git

install python: https://www.python.org/downloads/windows/
install pip by downloading this script: https://bootstrap.pypa.io/get-pip.py
and running python get-pip.py

#open a command prop and run:
pip install matplotlib obspy pyopengl glfw

HOW TO USE

before first use, the user should modify the file input_files.txt with the paths to the following files:
a params file, with the simulation parameters
a network file, with information of the stations
a model file, with the velocity model to use
a earthquake file, with basic information of the earthquake to invert

each of this files has a specific format, but accompaning the src code there are several examples of how to arrange this files, so should be a fairly simple process.

then:

to run a fordward simulation:

python forward.py 

to invert for the CMT run:

python source_invertion_gauss_newton.py

to invert for the velcity model (still not fully implemented) run:

python velocity_invertion_gauss_newton.py 
