'''
@Djim de Ridder

This is the analysing module of septinNetworkAFM.
    This modules contains the variables:
        -
    This module contains the function:
        -CalculateStructureTensor
        -CalculateOrientations
'''
import numpy as np

from skimage.draw import disk
import orientationpy

from ast import literal_eval
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def CalculateStructureTensor(im,
                             sig =1,
                             mode = "gaussian"
                             ):
    '''
    

    Parameters
    ----------
    im : TYPE
        DESCRIPTION.
    sig : TYPE, optional
        DESCRIPTION. The default is 1.
    mode : TYPE, optional
        DESCRIPTION. The default is "gaussian".

    Returns
    -------
    structureTensor : TYPE
        DESCRIPTION.

    '''
    if mode=="test":
        fig = plt.figure(tight_layout=True)
        fig.set_size_inches(15,10) #height, width
        gs6 = gridspec.GridSpec(3,2)
        for n, modes in enumerate(["finite_difference", "splines", "gaussian"]):
            #estimation gradient
            Gy, Gx = orientationpy.computeGradient(im, mode=modes)
            
            ax = fig.add_subplot(gs6[n,0])
            ax.set_title(f"{mode}-Gy")
            ax.imshow(Gy, cmap="coolwarm", vmin=-64, vmax=64)
    
            ax = fig.add_subplot(gs6[n,1])
            ax.set_title(f"{mode}-Gx")
            ax.imshow(Gx, cmap="coolwarm", vmin=-64, vmax=64)
            
            #structure tensor
            structureTensor = orientationpy.computeStructureTensor([Gy, Gx], sigma=sig)
    else:
        Gy, Gx = orientationpy.computeGradient(im, mode=mode)
        structureTensor = orientationpy.computeStructureTensor([Gy, Gx], sigma=sig)
    return structureTensor

def CalculateOrientations(structureTensor,
                          mask = True
                          ):
    orientations = orientationpy.computeOrientation(structureTensor, computeEnergy=True, computeCoherency=True)
    if mask==True:
        #---to avoid edge artifact make circular mask
        mask = np.zeros(structureTensor.shape[1:3], dtype=np.uint8)
        minAx = np.min(structureTensor.shape[1:3])
        rr, cc = disk((structureTensor.shape[1]/2, structureTensor.shape[2]/2), (minAx/2)-2, shape=structureTensor.shape[1:3])
        mask[rr, cc] = 1
        mask= mask>0
        
        orientations['theta'][~mask]=np.nan
        orientations['coherency'][~mask]=np.nan
        orientations['energy'][~mask]=np.nan
    return orientations

def FitHeightProfile(im,
                     config,
                     iConfig=15
                     ):
    expected = literal_eval(config['params_estimation'][iConfig])
    if isinstance(expected,tuple) and len(expected)==6:
        y,x = np.histogram(im.ravel(),bins=100,density=True)
        x=(x[1:]+x[:-1])/2 # correct hist data
        
        def gauss(x,mu,sigma,A):
            return A*np.exp(-(x-mu)**2/2/sigma**2)

        def bimodal(x,mu1,sigma1,A1,mu2,sigma2,A2):
            return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)
        params,cov=curve_fit(bimodal,x,y,expected)
    else:
        raise ValueError('Inside config file give an estimation of fitted values (muBG,sigmaBG,intenistyBG,muNetwork,sigmaNetwork,intenistyNetwork')
    
    return params