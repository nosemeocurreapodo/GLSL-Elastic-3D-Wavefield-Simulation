import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper

velx_texture_unit_number = 0
velx_texture_unit = GL_TEXTURE0
    
vely_texture_unit_number = 1
vely_texture_unit = GL_TEXTURE1
    
velz_texture_unit_number =2
velz_texture_unit = GL_TEXTURE2

sigmaxx_texture_unit_number = 3
sigmaxx_texture_unit = GL_TEXTURE3
    
sigmayy_texture_unit_number = 4
sigmayy_texture_unit = GL_TEXTURE4
    
sigmazz_texture_unit_number = 5
sigmazz_texture_unit = GL_TEXTURE5
    
sigmaxy_texture_unit_number = 6
sigmaxy_texture_unit = GL_TEXTURE6
    
sigmaxz_texture_unit_number = 7
sigmaxz_texture_unit = GL_TEXTURE7
  
sigmayz_texture_unit_number = 8
sigmayz_texture_unit = GL_TEXTURE8
    
rho_texture_unit_number = 9
rho_texture_unit = GL_TEXTURE9
    
lam_texture_unit_number = 10
lam_texture_unit = GL_TEXTURE10
    
mu_texture_unit_number = 11
mu_texture_unit = GL_TEXTURE11

fx_texture_unit_number = 12
fx_texture_unit = GL_TEXTURE12
    
fy_texture_unit_number = 13
fy_texture_unit = GL_TEXTURE13
    
fz_texture_unit_number = 14
fz_texture_unit = GL_TEXTURE14

surface_texture_unit_number = 15
surface_texture_unit = GL_TEXTURE15    

reciever_texture_unit_number = 16
reciever_texture_unit = GL_TEXTURE16 
