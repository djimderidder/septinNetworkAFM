# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 11:18:24 2023

@author: djimd
"""

'''
@Djim de Ridder

Runs a pipeline to get orientation information
'''

###---Import functions---
import functions as f

''''------------------------------------------------------------------------'''
'''LOADING DATA'''
indexConfig = 15
config = f.loadingMod.LoadConfigFile() #f.loadingMod.LoadConfigFile(fileFolder = folderAFM, nameConfig = fileNameConfig)
#load AFM image from config file
imAFM = f.loadingMod.LoadTxtFileFromConfig(config,
                                           iConfig = indexConfig
                                           ) #imAFM = f.loadingMod.LoadTxtFileFromConfig(config,fileFolder = folderAFM,iConfig = indexConfig)

#load simulated image'
imSim = f.loadingMod.LoadPngFile() #f.loadingMod.LoadPngFile(simImName,folderSim)
''''------------------------------------------------------------------------'''
'''PREPROCESSING'''
#For the orientation information we need uses 8 bit downscaled figure where low intenisty correlates with the background
#This step might not be necessary however it removes computational time and allows any 8 bit image (or tool)
imAFMp = f.preprocessingMod.FloatImgTo8Bit(im = imAFM,
                                           size = (768,768),
                                           config=config,
                                           iConfig = indexConfig
                                           )
imAFMp = imAFMp/512
imSimp = f.preprocessingMod.FloatImgTo8Bit(im = imSim,
                                           size = (768,768),
                                           invert = True
                                           )
imSimp = imSimp/512



''''------------------------------------------------------------------------'''
'''ANALYSING - window acf'''
#calculate autocorrelation image (code speed might be improved if we use the wiener-khinchin theorem)
#http://doi.org/10.1117/1.JBO.17.8.080801
#I also would probably look at the following paper: http://doi.org/10.1016/0098-3004(93)90053-8
#and consider to un this on the orientation information
import numpy as np
PImAFM = np.fft.fft2(imAFMp)*np.fft.fft2(imAFMp).conj()
acfImAFM = np.fft.ifft(PImAFM)/(np.mean(imAFMp)**2*PImAFM.shape[0]*PImAFM.shape[1]) #normalization seems to be off by factor of N with im=NxN

PImSim = np.fft.fft2(imSimp)*np.fft.fft2(imSimp).conj()
acfImSim = np.fft.ifft(PImSim)/(np.mean(imSimp)**2*PImSim.shape[0]*PImSim.shape[1])

#calculate crosscorrelation of image with window of image
windowSize = int(imAFMp.shape[0]/6)
windowAFM = np.zeros(imAFMp.shape) 
windowAFM[0:windowSize,0:windowSize]=imAFMp[0:windowSize,0:windowSize]
PImAFMw =  np.fft.fft2(imAFMp)*np.fft.fft2(windowAFM).conj()
acfImAFMw = np.fft.ifft(PImAFMw)/(np.mean(imAFMp)*np.mean(windowAFM)*PImAFMw.shape[0]*PImAFMw.shape[1])

windowSim = np.zeros(imSimp.shape) 
windowSim[0:windowSize,0:windowSize]=imSimp[0:windowSize,0:windowSize]
PImSimw =  np.fft.fft2(imSimp)*np.fft.fft2(windowSim).conj()
acfImSimw = np.fft.ifft(PImSimw)/(np.mean(imSimp)*np.mean(windowSim)*PImSimw.shape[0]*PImSimw.shape[1])

import matplotlib.pyplot as plt
fig,gs = f.plottingMod.SettingUpPlot(figGridx = 2,
                  figGridy=2
                  )
fig.add_subplot(gs[0,0]).imshow(np.fft.fftshift(acfImAFM).real) #shift middle of fourier to middle
fig.add_subplot(gs[1,0]).imshow(np.fft.fftshift(acfImAFMw).real) #shift middle of fourier to middle
fig.add_subplot(gs[0,1]).imshow(np.fft.fftshift(acfImSim).real) #shift middle of fourier to middle
fig.add_subplot(gs[1,1]).imshow(np.fft.fftshift(acfImSimw).real) #shift middle of fourier to middle

