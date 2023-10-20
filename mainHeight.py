'''
@Djim de Ridder

Runs a pipeline to get height information of AFM data
'''

###---Import functions---
import functions as f

''''------------------------------------------------------------------------'''
'''LOADING DATA'''
#define the folders and names
#folderAFM = r"D:\AFM_sorted\5PIP2_20DOPS\hexamers\denseNetwork"
#fileNameConfig = "fitHeightDistributionshdn.xlsx"
indexConfig = 15
#load config file
config = f.loadingMod.LoadConfigFile() #f.loadingMod.LoadConfigFile(fileFolder = folderAFM, nameConfig = fileNameConfig)
                                     
#load AFM image from config file
imAFM = f.loadingMod.LoadTxtFileFromConfig(config,
                                           iConfig = indexConfig
                                           ) #imAFM = f.loadingMod.LoadTxtFileFromConfig(config,fileFolder = folderAFM,iConfig = indexConfig)
''''------------------------------------------------------------------------'''
''''check loaded data'''
#define grid of figure
fig1,gs1 = f.plottingMod.SettingUpPlot(figGridx = 1,
                  figGridy=1
                  )
fig1,_ = f.plottingMod.PlotImageHistogram(fig=fig1,
                                        gs=gs1[0,0],
                                        im=imAFM,
                                        colorMap="afmhot"
                                        )
''''------------------------------------------------------------------------'''
''''ANALYSING'''
param = f.analysingMod.FitHeightProfile(im= imAFM,
                                        config=config,
                                        iConfig = indexConfig)
print(param)
''''------------------------------------------------------------------------'''
''''PLOTTING'''
#define grid of figure
fig2,gs2 = f.plottingMod.SettingUpPlot(figGridx = 1,
                  figGridy=1
                  )
import numpy as np
fig1, axHis = f.plottingMod.PlotImageHistogram(fig=fig2,
                                               gs=gs2[0,0],
                                               im=imAFM-np.ones(imAFM.shape)*param[0],
                                               clow=0,
                                               chigh=int(param[3]+3*param[4]-param[0]),
                                               colorMap="afmhot"
                                               )
f.plottingMod.PlotBimodalFit(ax=axHis,
                             params=(0, param[1], param[2], param[3]-param[0], param[4], param[5]),
                             im=imAFM-np.ones(imAFM.shape)*param[0])