import OpenGL
#OpenGL.ERROR_CHECKING = False
#OpenGL.ERROR_LOGGING = False
#OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args

class medium_params:
  def __init__(self, mediumParamsSize):
  
    self.mediumParamsSize = mediumParamsSize
    
    self.invRho = np.zeros((mediumParamsSize[2],mediumParamsSize[1],mediumParamsSize[0]), dtype='float32')
    self.lam = np.zeros((mediumParamsSize[2],mediumParamsSize[1],mediumParamsSize[0]), dtype='float32')
    self.mu = np.zeros((mediumParamsSize[2],mediumParamsSize[1],mediumParamsSize[0]), dtype='float32')
    
    self.invRhoTexId = glGenTextures(1);
    glActiveTexture(GL_TEXTURE9)
    glBindTexture(GL_TEXTURE_3D, self.invRhoTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    #print(invRho.shape)
    #print(invRho.shape[0])
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, mediumParamsSize[0], mediumParamsSize[1], mediumParamsSize[2], 0, GL_RED, GL_FLOAT, self.invRho);
    #glGenerateMipmap(GL_TEXTURE_3D);

    self.lamTexId = glGenTextures(1);
    glActiveTexture(GL_TEXTURE10)
    glBindTexture(GL_TEXTURE_3D, self.lamTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, mediumParamsSize[0], mediumParamsSize[1], mediumParamsSize[2], 0, GL_RED, GL_FLOAT, self.lam);
    #glGenerateMipmap(GL_TEXTURE_3D);

    self.muTexId = glGenTextures(1);
    glActiveTexture(GL_TEXTURE11)
    glBindTexture(GL_TEXTURE_3D, self.muTexId);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); 
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
    glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_MIRRORED_REPEAT);
    glTexImage3D(GL_TEXTURE_3D, 0, GL_R32F, mediumParamsSize[0], mediumParamsSize[1], mediumParamsSize[2], 0, GL_RED, GL_FLOAT, self.mu);
    #glGenerateMipmap(GL_TEXTURE_3D);
      
  def setMediumParams(self, invRho, lam, mu):
  
    self.invRho = invRho
    self.lam = lam
    self.mu = mu
  
    glActiveTexture(GL_TEXTURE9)
    glBindTexture(GL_TEXTURE_3D, self.invRhoTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.mediumParamsSize[0], self.mediumParamsSize[1], self.mediumParamsSize[2], GL_RED, GL_FLOAT, invRho) 
    
    glActiveTexture(GL_TEXTURE10)
    glBindTexture(GL_TEXTURE_3D, self.lamTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.mediumParamsSize[0], self.mediumParamsSize[1], self.mediumParamsSize[2], GL_RED, GL_FLOAT, lam) 

    glActiveTexture(GL_TEXTURE11)
    glBindTexture(GL_TEXTURE_3D, self.muTexId);
    glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, 0, self.mediumParamsSize[0], self.mediumParamsSize[1], self.mediumParamsSize[2], GL_RED, GL_FLOAT, lam) 
