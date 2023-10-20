'''
@Djim de Ridder

Runs a pipeline to get orientation information
'''

###---Import functions---
import functions as f

''''------------------------------------------------------------------------'''
'''LOADING DATA'''
#define the folders and names
#folderAFM = r"D:\AFM_sorted\5PIP2_20DOPS\hexamers\denseNetwork"
#fileNameConfig = "fitHeightDistributionshdn.xlsx"
indexConfig = 15
#folderSim = r"D:\AFM_sorted\simulated"
#simImName = "simulatedSeptinNetwork.png"
#load config file
config = f.loadingMod.LoadConfigFile() #f.loadingMod.LoadConfigFile(fileFolder = folderAFM, nameConfig = fileNameConfig)
#load AFM image from config file
imAFM = f.loadingMod.LoadTxtFileFromConfig(config,
                                           iConfig = indexConfig
                                           ) #imAFM = f.loadingMod.LoadTxtFileFromConfig(config,fileFolder = folderAFM,iConfig = indexConfig)

#load simulated image'
imSim = f.loadingMod.LoadPngFile() #f.loadingMod.LoadPngFile(simImName,folderSim)
''''------------------------------------------------------------------------'''
''''check loaded data'''
#define grid of figure
fig,gs = f.plottingMod.SettingUpPlot(figGridx = 2,
                  figGridy=1
                  )
#for scalebar we need to know a pixel distance in nanometer
import re
widthPX = float(re.sub("[^0-9.\-]","",re.findall(r'\d+px',config['name'][indexConfig][-20:])[0]))
widthNM = float(re.sub("[^0-9.\-]","",re.findall(r'\d+um',config['name'][indexConfig][-20:])[0]))*1000
#plotting AFM image
fig,_ = f.plottingMod.PlotAfmImage(fig,
                                   gs = gs[0,0],
                                   AFMimage = imAFM,
                                   clow=round(config['x1'][indexConfig]),
                                   chigh=round(config['x4'][indexConfig]+3*config['x5'][indexConfig]),
                                   widthpx=widthPX,
                                   widthnm=widthNM
                                   )
#plotting simulated image
fix,_ = f.plottingMod.PlotGrayImage(fig,
                                  gs = gs[0,1],
                                  image = imSim
                                  )
''''------------------------------------------------------------------------'''
'''PREPROCESSING'''
#For the orientation information we need uses 8 bit downscaled figure where low intenisty correlates with the background
#This step might not be necessary however it removes computational time and allows any 8 bit image (or tool)
imAFMp = f.preprocessingMod.FloatImgTo8Bit(im = imAFM,
                                           size = (768,768),
                                           config=config,
                                           iConfig = indexConfig
                                           )
imSimp = f.preprocessingMod.FloatImgTo8Bit(im = imSim,
                                           size = (768,768),
                                           invert = True
                                           )
''''------------------------------------------------------------------------'''
''''check loaded data'''
#define grid of figure
fig2,gs2 = f.plottingMod.SettingUpPlot(figGridx = 2,
                  figGridy=1
                  )
fig2,_ = f.plottingMod.PlotGrayImage(fig2,
                                   gs = gs2[0,0],
                                   image = imAFMp
                                     )
fig2,_ = f.plottingMod.PlotGrayImage(fig2,
                                   gs = gs2[0,1],
                                   image = imSimp
                                   )

''''------------------------------------------------------------------------'''
''''ANALYSING'''
#calculate structure tensor with orientationpy (you can install orientationpy with "pip install orientationpy")
#if you set mode = "test" or leave empty you will plot the gradient images for the different methods
sigma = 2
imAFMT = f.analysingMod.CalculateStructureTensor(imAFMp,
                                              sig = sigma,
                                              mode = "gaussian",
                                              )
imSimT = f.analysingMod.CalculateStructureTensor(imSimp,
                                              sig = sigma,
                                              mode = "gaussian",
                                              )
#calculate orientations with orientationpy
#if you set mask = True you can also set orientation information outside the circular mask to nan
orientationsAFM = f.analysingMod.CalculateOrientations(imAFMT,
                                                       mask = True
                                                       )
orientationsSim = f.analysingMod.CalculateOrientations(imSimT,
                                                       mask = True
                                                       )

''''------------------------------------------------------------------------'''
''''PLOTTING'''
#plot image with orientation=Hue, coherency=Saturation, original image=brightness (Rezakhaniha 2012)
fig3,gs3 = f.plottingMod.SettingUpPlot(figGridx = 2,
                  figGridy=1
                  )
fig3,_ = f.plottingMod.PlotHSB(fig = fig3,
                             gs = gs3[0,0],
                             orientations = orientationsAFM,
                             im = imAFMp
                             )
fig3,_ = f.plottingMod.PlotHSB(fig = fig3,
                             gs = gs3[0,1],
                             orientations = orientationsSim,
                             im = imSimp
                             )
#PlotOrientationHistogram()
fig4,gs4 = f.plottingMod.SettingUpPlot(figGridx = 2,
                  figGridy=1
                  )
fig4,_ = f.plottingMod.PlotOrientationHistogram(fig = fig4,
                                              gs = gs4[0,0],
                                              orientations = orientationsAFM
                                                   )
fig4,_ = f.plottingMod.PlotOrientationHistogram(fig=fig4,
                                              gs=gs4[0,1],
                                              orientations = orientationsSim
                                              )