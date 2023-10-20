'''
@Djim de Ridder

Runs a pipeline to make figures for the paper
'''

###---Import functions---
import functions as f

''''------------------------------------------------------------------------'''
'''LOADING DATA'''
#define the folders and names
nameConfig = "fitHeightDistributionshdn.xlsx"
nameConfig2 = "fitHeightDistributionsocn.xlsx"
drive = "D:\AFM_sorted"
folder1 = "5PIP2_20DOPS\hexamers\denseNetwork"
folder2 = "5PIP2_20DOPS\octamers\coveredNetwork"

#load config file
import os
config = f.loadingMod.LoadConfigFile(fileFolder = os.path.join(drive,folder1),
                                     nameConfig = nameConfig
                                     )
config2 = f.loadingMod.LoadConfigFile(fileFolder = os.path.join(drive,folder2),
                                     nameConfig = nameConfig2
                                     )

#load high denisty network image
iconfigIMh1 = 36
IMh1 = f.loadingMod.LoadTxtFileFromConfig(config,
                                          fileFolder = os.path.join(drive,folder1),
                                          iConfig = iconfigIMh1
                                          )
coord1=[0,75,256,448] #ymin,ymax,xmin,xmax
IMh1 = IMh1[coord1[0]:coord1[1],coord1[2]:coord1[3]]-config['x1'][iconfigIMh1]
#load lower denisty network
iconfigIMh2 = 26
IMh2 = f.loadingMod.LoadTxtFileFromConfig(config,
                                          fileFolder = os.path.join(drive,folder1),
                                          iConfig = iconfigIMh2
                                          )
coord2=[52,127,25,217] #ymin,ymax,xmin,xmax
IMh2 = IMh2[coord2[0]:coord2[1],coord2[2]:coord2[3]]-config['x1'][iconfigIMh2]
#load octamer networks
iconfigIMo1 =4
IMo1 = f.loadingMod.LoadTxtFileFromConfig(config2,
                                          fileFolder = os.path.join(drive,folder2),
                                          iConfig = iconfigIMo1
                                          )
coord3=[0,188,350,830]
IMo1 = IMo1[coord3[0]:coord3[1],coord3[2]:coord3[3]]-config2['x1'][iconfigIMo1]
#load second octamer network
iconfigIMo2 = 7 #0,34
IMo2 = f.loadingMod.LoadTxtFileFromConfig(config2,
                                          fileFolder = os.path.join(drive,folder2),
                                          iConfig = iconfigIMo2
                                          )
coord4= [0,150,0,384]#[30,130,100,356],[350,600,400,1040]
IMo2 = IMo2[coord4[0]:coord4[1],coord4[2]:coord4[3]]-config2['x1'][iconfigIMo2]
#load image for profile plot
iconfigIMp = 12
IMp = f.loadingMod.LoadTxtFileFromConfig(config,
                                         fileFolder = os.path.join(drive,folder1),
                                         iConfig = iconfigIMp
                                         )

''''------------------------------------------------------------------------'''
''''PLOTTING'''
fig1,gs1 = f.plottingMod.SettingUpPlot(figGridx = 1,
                  figGridy=2,
                  figSize =(7,8)
                  )
fig1,_ = f.plottingMod.PlotImageHistogram(fig=fig1,
                                        gs=gs1[0,0],
                                        im=IMh2,
                                        clow=0,
                                        chigh=15,
                                        colorMap="afmhot"
                                        )
fig1,_ = f.plottingMod.PlotImageHistogram(fig=fig1,
                                        gs=gs1[1,0],
                                        im=IMh1,
                                        clow=0,
                                        chigh=15,
                                        colorMap="afmhot"
                                        )
fig2,gs2 = f.plottingMod.SettingUpPlot(figGridx = 1,
                  figGridy=2,
                  figSize =(7,8)
                  )
fig2,_ = f.plottingMod.PlotImageHistogram(fig=fig2,
                                        gs=gs2[0,0],
                                        im=IMo1,
                                        clow=0,
                                        chigh=15,
                                        colorMap="afmhot",
                                        coordInlet=[240,240+60,110,110+50]
                                        )
fig2,_ = f.plottingMod.PlotImageHistogram(fig=fig2,
                                        gs=gs2[1,0],
                                        im=IMo2,
                                        clow=0,
                                        chigh=15,
                                        colorMap="afmhot"
                                        )

fig3,gs3 = f.plottingMod.SettingUpPlot(figGridx = 1,
                                       figGridy=1,
                                       figSize =(12,4)
                                       )
import re
widthPX = float(re.sub("[^0-9.\-]","",re.findall(r'\d+px',config['name'][iconfigIMp][-20:])[0]))
widthNM = float(re.sub("[^0-9.\-]","",re.findall(r'\d+um',config['name'][iconfigIMp][-20:])[0]))*1000
f.plottingMod.PlotAfmProfilePlot(fig=fig3,
                                 gs=gs3[0,0],
                                 im=IMp,
                                 shift=(200,300),
                                 delta=200,
                                 start=(90,40),
                                 end=(150,135),
                                 widthpx=widthPX,
                                 widthnm=widthNM
                                 )