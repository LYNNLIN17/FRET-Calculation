import Tkinter as tk
import tkFileDialog
import os.path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
from scipy.optimize import curve_fit
from scipy import exp
from astropy.stats import median_absolute_deviation
from astropy.table import Table, Column


class Module_FRETanalysis(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        modulenameLabel = tk.Label(self, text="Module 2: FRET Calculation for Neuron")
        modulenameLabel.grid(row=0, column=0, sticky='W')
               

        getpathButton = tk.Button(self,text=u"Select Image Path", command = self.getpathButton_Click)
        getpathButton.grid(row=1, column=151, columnspan=100, sticky='W')

        
        self.pathStr = tk.StringVar()
        self.pathEntry = tk.Entry(self,textvariable=self.pathStr)
        self.pathEntry.grid(row=1, column=251, columnspan=150, sticky='W')
        self.pathEntry.bind("<Return>", self.pathEntry_Enter)
        self.pathStr.set(u"")
        self.imgpath = ""


        step1Button = tk.Button(self,text=u"Step1: Load Images", command=self.step1Button_Click)
        step1Button.grid(row=1, column=0, columnspan=150, sticky='W')


        step2Button = tk.Button(self,text=u"Step2: Indicate the Position of the Neuron", command=self.step2Button_Click)
        step2Button.grid(row=2, column=0, columnspan=150, sticky='W')

        neuronwidthLabel = tk.Label(self, text="Width of the Neuron: ")
        neuronwidthLabel.grid(row=2, column=151, columnspan=100, sticky='W')
        
        self.neuronwidthStr = tk.StringVar()
        self.neuronwidthEntry = tk.Entry(self,textvariable=self.neuronwidthStr)
        self.neuronwidthEntry.grid(row=2, column=251, columnspan=150, sticky='W')
        self.neuronwidthStr.set(u"20")
        

        step3Button = tk.Button(self,text=u"Step3: Background Substraction and ROI Selection", command=self.step3Button_Click)
        step3Button.grid(row=3, column=0, columnspan=150, sticky='W')

        neuronnameLabel = tk.Label(self, text="Name of the node: ")
        neuronnameLabel.grid(row=3, column=151, columnspan=100, sticky='W')
        
        self.neuronnameStr = tk.StringVar()
        self.neuronnameEntry = tk.Entry(self,textvariable=self.neuronnameStr)
        self.neuronnameEntry.grid(row=3, column=251, columnspan=150, sticky='W')
        self.neuronnameStr.set(u"neuron")
        

        step4Button = tk.Button(self,text=u"Step4: FRET Efficiency and Uncertainty Calculation", command=self.step4Button_Click)
        step4Button.grid(row=4, column=0, columnspan=150, sticky='W')

        step5Button = tk.Button(self,text=u"Step5: Characterization of FRET", command=self.step5Button_Click)
        step5Button.grid(row=5, column=0, columnspan=150, sticky='W')

        self.testStr1 = tk.StringVar()
        testLabel1 = tk.Label(self, textvariable=self.testStr1, fg="red")
        testLabel1.grid(row=6, column=0, sticky='W')
        self.testStr1.set(u"Start the procedure by following the steps!")


        resulttitleLabel = tk.Label(self, text="Results")
        resulttitleLabel.grid(row=0, column=500, columnspan=100, sticky='W')

        result1ttLabel = tk.Label(self, text="Median of the FRET Efficiency:")
        result1ttLabel.grid(row=1, column=401, columnspan=99, sticky='W')
        self.result1Str = tk.StringVar()
        result1Label = tk.Label(self, textvariable=self.result1Str, fg="blue")
        result1Label.grid(row=1, column=500, columnspan=100, sticky='W')
        self.result1Str.set(u"")

        result2ttLabel = tk.Label(self, text="Average of the FRET Efficiency:")
        result2ttLabel.grid(row=2, column=401, columnspan=99, sticky='W')
        self.result2Str = tk.StringVar()
        result2Label = tk.Label(self, textvariable=self.result2Str, fg="blue")
        result2Label.grid(row=2, column=500, columnspan=100, sticky='W')
        self.result2Str.set(u"")

        result3ttLabel = tk.Label(self, text="/total # of pixel in ROI")
        result3ttLabel.grid(row=3, column=401, columnspan=99, sticky='W')
        self.result3Str = tk.StringVar()
        result3Label = tk.Label(self, textvariable=self.result3Str, fg="blue")
        result3Label.grid(row=3, column=500, columnspan=100, sticky='W')
        self.result3Str.set(u"")

        result4ttLabel = tk.Label(self, text="# of uncertain pixels")
        result4ttLabel.grid(row=4, column=401, columnspan=99, sticky='W')
        self.result4Str = tk.StringVar()
        result4Label = tk.Label(self, textvariable=self.result4Str, fg="blue")
        result4Label.grid(row=4, column=500, columnspan=100, sticky='W')
        self.result4Str.set(u"")

        result5ttLabel = tk.Label(self, text="Average uncertainty:")
        result5ttLabel.grid(row=5, column=401, columnspan=99, sticky='W')
        self.result5Str = tk.StringVar()
        result5Label = tk.Label(self, textvariable=self.result5Str, fg="blue")
        result5Label.grid(row=5, column=500, columnspan=100, sticky='W')
        self.result5Str.set(u"")

        result6ttLabel = tk.Label(self, text="# of pixels in final quantification")
        result6ttLabel.grid(row=6, column=401, columnspan=99, sticky='W')
        self.result6Str = tk.StringVar()
        result6Label = tk.Label(self, textvariable=self.result6Str, fg="blue")
        result6Label.grid(row=6, column=500, columnspan=100, sticky='W')
        self.result6Str.set(u"")

                      
        self.grid_columnconfigure(0, weight=1)
        self.update()
        self.geometry(self.geometry())
        self.neuronname = "neuron"
        self.pathEntry.focus_set()
        self.pathEntry.selection_range(0, tk.END)
        self.neuronnameEntry.focus_set()
        self.neuronnameEntry.selection_range(0, tk.END)

        self.step1Button_Clicked = False
        self.step2Button_Checked = False
        self.step3Button_Checked = False
        self.step4Button_Checked = False
        self.step5Button_Checked = False

        self.drawNpt = 0
        self.finishDrawing = False

                
    def pathEntry_Enter(self, event):
        self.imgpath = self.pathStr.get()
        self.pathEntry.focus_set()
        self.pathEntry.selection_range(0, tk.END)

    def neuronnameEntry_Enter(self, event):
    	self.neuronname = self.neuronnameStr.get()
    	self.neuronnameEntry.focus_set()
    	self.neuronnameEntry.selection_range(9, tk.END)
    
    def getpathButton_Click(self):
        imgfullpath = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",
            filetypes = (("tif files","*.tif"),("all files","*.*")))
        self.imgpath = os.path.dirname(imgfullpath)
        self.pathStr.set(self.imgpath)

    def step1Button_Click(self):
        if self.step1Button_Clicked == False:
            
            if self.imgpath == "":
                print("Please enter the path name of the image files!")
            else:                
                donorImg = Image.open(os.path.abspath(self.imgpath) + "/donor.tif")
                self.donorArray = np.array(donorImg)
                
                acceptorImg = Image.open(os.path.abspath(self.imgpath) + "/acceptor.tif")
                self.acceptorArray = np.array(acceptorImg)
                
                fretImg = Image.open(os.path.abspath(self.imgpath) + "/fret.tif")
                self.fretArray = np.array(fretImg)

                self.step1Button_Clicked = True
                
                imgfig1,axes1 = plt.subplots(1,3)
                imgfig1.canvas.set_window_title('Original Images')
                
               
                im11 = axes1[0].imshow(self.donorArray, cmap = 'nipy_spectral')
                cbar11 = imgfig1.colorbar(im11, ax=axes1[0],orientation='horizontal')
                cbar11.ax.set_xticklabels(cbar11.ax.get_xticklabels(),rotation=90)
                axes1[0].set_title('Donor Channel')
                axes1[0].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                
                im12 = axes1[1].imshow(self.acceptorArray, cmap = 'nipy_spectral')
                cbar12 = imgfig1.colorbar(im12, ax=axes1[1],orientation='horizontal')
                cbar12.ax.set_xticklabels(cbar12.ax.get_xticklabels(),rotation=90)
                axes1[1].set_title('Acceptor Channel')
                axes1[1].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                im13 = axes1[2].imshow(self.fretArray, cmap = 'nipy_spectral')
                cbar13 = imgfig1.colorbar(im13, ax=axes1[2],orientation='horizontal')
                cbar13.ax.set_xticklabels(cbar13.ax.get_xticklabels(),rotation=90)
                axes1[2].set_title('FRET Channel')
                axes1[2].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                        
                plt.show()
                
    def drawMultiLineSegments(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.drawNpt == 0:
                ix,iy = x,y
                self.drawNpt = self.drawNpt+1
                self.polylineX = [ix]
                self.polylineY = [iy]
                cv2.circle(self.img, (ix,iy), 5, (0,30000,0))
                            
            elif (self.drawNpt > 0) & (self.finishDrawing == False):
                ix,iy = x,y
                self.drawNpt = self.drawNpt+1
                self.polylineX = np.append(self.polylineX,[ix],axis=0)
                self.polylineY = np.append(self.polylineY,[iy],axis=0)
                cv2.line(self.img, (self.polylineX[self.drawNpt-2],self.polylineY[self.drawNpt-2]), (ix,iy), (0,30000,0), 3)
                cv2.circle(self.img, (ix,iy), 5, (0,30000,0))

        elif event == cv2.EVENT_RBUTTONDOWN:
            if (self.drawNpt >= 2):
                self.finishDrawing = True
                print(self.polylineX)
                print(self.polylineY)
        
    def step2Button_Click(self):
        if (self.step1Button_Clicked == True):
            self.img = cv2.cvtColor(self.acceptorArray,cv2.COLOR_GRAY2RGB)
            filename = os.path.abspath(self.imgpath) + "/field_of_node_" + self.neuronname + ".png"
            cv2.namedWindow('Acceptor Channel')
            cv2.setMouseCallback('Acceptor Channel',self.drawMultiLineSegments)
            while (self.finishDrawing == False):
                cv2.imshow('Acceptor Channel',self.img)
                cv2.imwrite(filename, self.img) 
                cv2.waitKey(1)
            if (len(self.polylineX) >= 2):
                self.step2Button_Clicked = True
                cv2.destroyAllWindows()

    def gauss1Fit(self,x,a1,b1,c1,d1):
        return a1*exp(-((x-b1)/c1)**2)+d1

    def gauss1Fit_adjust(self,x,a1,d1):
        return a1*exp(-((x-self.bmean)/self.csigma)**2)+d1
    
    def step3Button_Click(self):
        if (self.step2Button_Clicked == True):
            neuronWidth = np.int_(self.neuronwidthStr.get())
            self.polylineX = np.int_(np.ceil(self.polylineX))
            self.polylineY = np.int_(np.ceil(self.polylineY))
            Npts = len(self.polylineX)
            fitMode = 0

            newacceptorArray = np.zeros((self.acceptorArray.shape[0],self.acceptorArray.shape[1]), np.int_)
            newdonorArray = np.zeros((self.donorArray.shape[0],self.donorArray.shape[1]), np.int_)
            newfretArray = np.zeros((self.fretArray.shape[0],self.fretArray.shape[1]), np.int_)
            ROIArray = np.zeros((self.acceptorArray.shape[0],self.acceptorArray.shape[1]), np.int_)

            newacceptorDispArray = np.zeros((self.acceptorArray.shape[0],self.acceptorArray.shape[1]), np.int_)
            newdonorDispArray = np.zeros((self.donorArray.shape[0],self.donorArray.shape[1]), np.int_)
            newfretDispArray = np.zeros((self.fretArray.shape[0],self.fretArray.shape[1]), np.int_)

            whole_xxfit = []
            whole_yyfit = []
            whole_centerPt = []
            whole_gaussWidth = []
            whole_bkgdVal = []
            whole_bkgdVal_donor = []
            whole_bkgdVal_fret = []

            for cLine in range(0,Npts-1):
            	endptX = np.array([self.polylineX[cLine],self.polylineX[cLine+1]])
            	endptY = np.array([self.polylineY[cLine],self.polylineY[cLine+1]])
                if endptX[0]!=endptX[1]:
                    pfit = np.polyfit(endptX-0.5, endptY-0.5, 1)
                    mslope = abs(pfit[0])
                    if mslope<=0.577:
                        fitMode = 1
                    elif (mslope>0.577) & (mslope<=1.73):
                        if pfit[0]>0:
                            fitMode = 2
                        else:
                            fitMode = 3
                    elif mslope>1.73:
                        fitMode = 4

                    xfit = np.linspace(endptX[0], endptX[1], 
                        num=100*np.sqrt((endptX[1]-endptX[0])**2+(endptY[1]-endptY[0])**2))
                    yfit = np.polyval(pfit, xfit)

                    xfit = np.int_(np.ceil(xfit))
                    yfit = np.int_(np.ceil(yfit))

                    xxfit = []
                    yyfit = []

                    for i in range(endptX[0], endptX[1]):
                        xind = np.where(xfit==i)
                        uyind = np.unique(yfit[xind])
                        for j in range(0,len(uyind)):
                            xxfit = np.append(xxfit,i)
                            yyfit = np.append(yyfit,uyind[j])
                    xxfit = np.int_(xxfit)
                    yyfit = np.int_(yyfit)

                else:
                    fitMode = 4
                    xxfit = []
                    yyfit = []
                    for i in range(endptY[0], endptY[1]+1):
                        xxfit = np.append(xxfit,endptX[0])
                        yyfit = np.append(yyfit,i)
                    xxfit = np.int_(xxfit)
                    yyfit = np.int_(yyfit)

                whole_xxfit = np.append(whole_xxfit,xxfit)
                whole_yyfit = np.append(whole_yyfit,yyfit)

                print(fitMode)            
                
                if (fitMode == 1):
                    for i in range(0,len(xxfit)):                    
                        if i==0:
                            aimgMat = [self.acceptorArray[range(yyfit[i]-neuronWidth-1,yyfit[i]+neuronWidth),xxfit[i]-1]]
                            dimgMat = [self.donorArray[range(yyfit[i]-neuronWidth-1,yyfit[i]+neuronWidth),xxfit[i]-1]]
                            fimgMat = [self.fretArray[range(yyfit[i]-neuronWidth-1,yyfit[i]+neuronWidth),xxfit[i]-1]]
                        else:
                            aimgMat = np.append(aimgMat,[self.acceptorArray[range(yyfit[i]-neuronWidth-1,yyfit[i]+neuronWidth),xxfit[i]-1]], axis=0)
                            dimgMat = np.append(dimgMat,[self.donorArray[range(yyfit[i]-neuronWidth-1,yyfit[i]+neuronWidth),xxfit[i]-1]], axis=0)
                            fimgMat = np.append(fimgMat,[self.fretArray[range(yyfit[i]-neuronWidth-1,yyfit[i]+neuronWidth),xxfit[i]-1]], axis=0)
                    
                elif (fitMode == 2):
                    for i in range(0,len(xxfit)):
                        for ii in range(-neuronWidth-1,neuronWidth+1):
                            if ii==-neuronWidth-1:
                                atempMat = [self.acceptorArray[yyfit[i]+ii,xxfit[i]-ii]]
                                dtempMat = [self.donorArray[yyfit[i]+ii,xxfit[i]-ii]]
                                ftempMat = [self.fretArray[yyfit[i]+ii,xxfit[i]-ii]]
                            else:
                                atempMat = np.append(atempMat,[self.acceptorArray[yyfit[i]+ii,xxfit[i]-ii]])
                                dtempMat = np.append(dtempMat,[self.donorArray[yyfit[i]+ii,xxfit[i]-ii]])
                                ftempMat = np.append(ftempMat,[self.fretArray[yyfit[i]+ii,xxfit[i]-ii]])
                        if i==0:
                            aimgMat = [atempMat]
                            dimgMat = [dtempMat]
                            fimgMat = [ftempMat]
                        else:
                            aimgMat = np.append(aimgMat,[atempMat], axis=0)
                            dimgMat = np.append(dimgMat,[dtempMat], axis=0)
                            fimgMat = np.append(fimgMat,[ftempMat], axis=0)

                elif (fitMode == 3):
                    for i in range(0,len(xxfit)):
                        for ii in range(-neuronWidth-1,neuronWidth+1):
                            if ii==-neuronWidth-1:
                                atempMat = [self.acceptorArray[yyfit[i]+ii,xxfit[i]+ii]]
                                dtempMat = [self.donorArray[yyfit[i]+ii,xxfit[i]+ii]]
                                ftempMat = [self.fretArray[yyfit[i]+ii,xxfit[i]+ii]]
                            else:
                                atempMat = np.append(atempMat,[self.acceptorArray[yyfit[i]+ii,xxfit[i]+ii]])
                                dtempMat = np.append(dtempMat,[self.donorArray[yyfit[i]+ii,xxfit[i]+ii]])
                                ftempMat = np.append(ftempMat,[self.fretArray[yyfit[i]+ii,xxfit[i]+ii]])
                        if i==0:
                            aimgMat = [atempMat]
                            dimgMat = [dtempMat]
                            fimgMat = [ftempMat]
                        else:
                            aimgMat = np.append(aimgMat,[atempMat], axis=0)
                            dimgMat = np.append(dimgMat,[dtempMat], axis=0)
                            fimgMat = np.append(fimgMat,[ftempMat], axis=0)
                    
                elif (fitMode == 4):
                    for i in range(0,len(xxfit)):
                        if i==0:
                            aimgMat = [self.acceptorArray[yyfit[i]-1,range(xxfit[i]-neuronWidth-1,xxfit[i]+neuronWidth)]]
                            dimgMat = [self.donorArray[yyfit[i]-1,range(xxfit[i]-neuronWidth-1,xxfit[i]+neuronWidth)]]
                            fimgMat = [self.fretArray[yyfit[i]-1,range(xxfit[i]-neuronWidth-1,xxfit[i]+neuronWidth)]]
                        else:
                            aimgMat = np.append(aimgMat,[self.acceptorArray[yyfit[i]-1,range(xxfit[i]-neuronWidth-1,xxfit[i]+neuronWidth)]], axis=0)
                            dimgMat = np.append(dimgMat,[self.donorArray[yyfit[i]-1,range(xxfit[i]-neuronWidth-1,xxfit[i]+neuronWidth)]], axis=0)
                            fimgMat = np.append(fimgMat,[self.fretArray[yyfit[i]-1,range(xxfit[i]-neuronWidth-1,xxfit[i]+neuronWidth)]], axis=0)
                for i in range(0,len(xxfit)):
                    xgaussfit = np.array(range(len(aimgMat[i,:])))
                    ygaussfit = np.array(aimgMat[i,:])
                    popt,pcov = curve_fit(self.gauss1Fit,xgaussfit,ygaussfit,bounds=([0,neuronWidth/2,1,0],[1000,neuronWidth*3/2,neuronWidth,100]))
                    if i==0:
                        centerPt = popt[1]
                        gaussWidth = popt[2]/2/np.sqrt(2)
                        bkgdVal = popt[3]
                        self.bmean = centerPt
                        self.csigma = gaussWidth
                    else:
                        centerPt = np.append(centerPt,popt[1])
                        gaussWidth = np.append(gaussWidth,popt[2]/2/np.sqrt(2))
                        bkgdVal = np.append(bkgdVal,popt[3])
                        self.bmean = centerPt[i]
                        self.csigma = gaussWidth[i]
                    
                    
                    xgaussfit = np.array(range(len(dimgMat[i,:])))
                    ygaussfit = np.array(dimgMat[i,:])
                    popt,pcov = curve_fit(self.gauss1Fit_adjust,xgaussfit,ygaussfit,bounds=([0,0],[1000,100]))
                    if i==0:
                        bkgdVal_donor = popt[1]
                    else:
                        bkgdVal_donor = np.append(bkgdVal_donor,popt[1])

                    xgaussfit = np.array(range(len(fimgMat[i,:])))
                    ygaussfit = np.array(fimgMat[i,:])
                    popt,pcov = curve_fit(self.gauss1Fit_adjust,xgaussfit,ygaussfit,bounds=([0,0],[1000,100]))
                    if i==0:
                        bkgdVal_fret = popt[1]
                    else:
                        bkgdVal_fret = np.append(bkgdVal_fret,popt[1])
                    

                centerPt = np.int_(np.ceil(centerPt))
                gaussWidth = np.int_(np.ceil(gaussWidth))
                bkgdVal = np.int_(np.ceil(bkgdVal))
                bkgdVal_donor = np.int_(np.ceil(bkgdVal_donor))
                bkgdVal_fret = np.int_(np.ceil(bkgdVal_fret))

                whole_centerPt = np.append(whole_centerPt,centerPt)
                whole_gaussWidth = np.append(whole_gaussWidth,gaussWidth)
                whole_bkgdVal = np.append(whole_bkgdVal,bkgdVal)
                whole_bkgdVal_donor = np.append(whole_bkgdVal_donor,bkgdVal_donor)
                whole_bkgdVal_fret = np.append(whole_bkgdVal_fret,bkgdVal_fret)
                              
                if (fitMode == 1):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(yyfit[i]-gaussWidth[i]-1+shiftCPt,yyfit[i]+gaussWidth[i]+shiftCPt):
                            newacceptorArray[ii,xxfit[i]-1] = np.int_(np.int_(self.acceptorArray[ii,xxfit[i]-1])-bkgdVal[i])
                            newacceptorDispArray[ii,xxfit[i]-1] = np.int_(np.int_(self.acceptorArray[ii,xxfit[i]-1])-bkgdVal[i])

                            newdonorArray[ii,xxfit[i]-1] = np.int_(np.int_(self.donorArray[ii,xxfit[i]-1])-bkgdVal_donor[i])
                            newdonorDispArray[ii,xxfit[i]-1] = np.int_(np.int_(self.donorArray[ii,xxfit[i]-1])-bkgdVal_donor[i])

                            newfretArray[ii,xxfit[i]-1] = np.int_(np.int_(self.fretArray[ii,xxfit[i]-1])-bkgdVal_fret[i])
                            newfretDispArray[ii,xxfit[i]-1] = np.int_(np.int_(self.fretArray[ii,xxfit[i]-1])-bkgdVal_fret[i])

                            ROIArray[ii,xxfit[i]-1] = np.int_(1)                           
                        newacceptorDispArray[yyfit[i]-gaussWidth[i]-1+shiftCPt-1,xxfit[i]-1] = np.int_(-1)
                        newacceptorDispArray[yyfit[i]+gaussWidth[i]+shiftCPt,xxfit[i]-1] = np.int_(-1)
                        newdonorDispArray[yyfit[i]-gaussWidth[i]-1+shiftCPt-1,xxfit[i]-1] = np.int_(-1)
                        newdonorDispArray[yyfit[i]+gaussWidth[i]+shiftCPt,xxfit[i]-1] = np.int_(-1)
                        newfretDispArray[yyfit[i]-gaussWidth[i]-1+shiftCPt-1,xxfit[i]-1] = np.int_(-1)
                        newfretDispArray[yyfit[i]+gaussWidth[i]+shiftCPt,xxfit[i]-1] = np.int_(-1)
                elif (fitMode == 2):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(-gaussWidth[i]-1,gaussWidth[i]+1):
                            pxlInten = np.int_(self.acceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt])-bkgdVal[i]
                            newacceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(pxlInten)
                            newacceptorDispArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(pxlInten)

                            pxlInten_donor = np.int_(self.donorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt])-bkgdVal_donor[i]                       
                            newdonorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(pxlInten_donor)
                            newdonorDispArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(pxlInten_donor)

                            pxlInten_fret = np.int_(self.fretArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt])-bkgdVal_fret[i] 
                            newfretArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(pxlInten_fret)
                            newfretDispArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(pxlInten_fret)

                            ROIArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(1)
                        newacceptorDispArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]+gaussWidth[i]+2-shiftCPt] = np.int_(-1)
                        newacceptorDispArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]-gaussWidth[i]-1-shiftCPt] = np.int_(-1)
                        newdonorDispArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]+gaussWidth[i]+2-shiftCPt] = np.int_(-1)
                        newdonorDispArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]-gaussWidth[i]-1-shiftCPt] = np.int_(-1)
                        newfretDispArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]+gaussWidth[i]+2-shiftCPt] = np.int_(-1)
                        newfretDispArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]-gaussWidth[i]-1-shiftCPt] = np.int_(-1)
                elif (fitMode == 3):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(-gaussWidth[i]-1,gaussWidth[i]+1):
                            pxlInten = np.int_(self.acceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt])-bkgdVal[i]                     
                            newacceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(pxlInten)
                            newacceptorDispArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(pxlInten)

                            pxlInten_donor = np.int_(self.donorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt])-bkgdVal_donor[i]                       
                            newdonorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(pxlInten_donor)
                            newdonorDispArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(pxlInten_donor)

                            pxlInten_fret = np.int_(self.fretArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt])-bkgdVal_fret[i]                       
                            newfretArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(pxlInten_fret)
                            newfretDispArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(pxlInten_fret)

                            ROIArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(1)
                        newacceptorDispArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]-gaussWidth[i]-2+shiftCPt] = np.int_(-1)
                        newacceptorDispArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]+gaussWidth[i]+1+shiftCPt] = np.int_(-1)
                        newdonorDispArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]-gaussWidth[i]-2+shiftCPt] = np.int_(-1)
                        newdonorDispArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]+gaussWidth[i]+1+shiftCPt] = np.int_(-1)
                        newfretDispArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]-gaussWidth[i]-2+shiftCPt] = np.int_(-1)
                        newfretDispArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]+gaussWidth[i]+1+shiftCPt] = np.int_(-1)                
                elif (fitMode == 4):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(xxfit[i]-gaussWidth[i]-1+shiftCPt,xxfit[i]+gaussWidth[i]+shiftCPt):
                            newacceptorArray[yyfit[i]-1,ii] = np.int_(np.int_(self.acceptorArray[yyfit[i]-1,ii])-bkgdVal[i])
                            newacceptorDispArray[yyfit[i]-1,ii] = np.int_(np.int_(self.acceptorArray[yyfit[i]-1,ii])-bkgdVal[i])

                            newdonorArray[yyfit[i]-1,ii] = np.uint16(np.int_(self.donorArray[yyfit[i]-1,ii])-bkgdVal_donor[i])
                            newdonorDispArray[yyfit[i]-1,ii] = np.uint16(np.int_(self.donorArray[yyfit[i]-1,ii])-bkgdVal_donor[i])
                            
                            newfretArray[yyfit[i]-1,ii] = np.uint16(np.int_(self.fretArray[yyfit[i]-1,ii])-bkgdVal_fret[i])
                            newfretDispArray[yyfit[i]-1,ii] = np.uint16(np.int_(self.fretArray[yyfit[i]-1,ii])-bkgdVal_fret[i])

                            ROIArray[yyfit[i]-1,ii] = np.int_(np.repeat(1,len(ii)))
                        newacceptorDispArray[yyfit[i]-1,xxfit[i]-gaussWidth[i]-1+shiftCPt-1] = np.int_(-1)
                        newacceptorDispArray[yyfit[i]-1,xxfit[i]+gaussWidth[i]+shiftCPt] = np.int_(-1)
                        newdonorDispArray[yyfit[i]-1,xxfit[i]-gaussWidth[i]-1+shiftCPt-1] = np.int_(-1)
                        newdonorDispArray[yyfit[i]-1,xxfit[i]+gaussWidth[i]+shiftCPt] = np.int_(-1)
                        newfretDispArray[yyfit[i]-1,xxfit[i]-gaussWidth[i]-1+shiftCPt-1] = np.int_(-1)
                        newfretDispArray[yyfit[i]-1,xxfit[i]+gaussWidth[i]+shiftCPt] = np.int_(-1)

            a1 = np.int_(np.amin(whole_yyfit)-5)
            a2 = np.int_(np.amax(whole_yyfit)+5)
            b1 = np.int_(np.amin(whole_xxfit)-5)
            b2 = np.int_(np.amax(whole_xxfit)+5)
            tempcropdonorArray = newdonorArray[range(a1,a2),:]
            self.cropdonorArray = tempcropdonorArray[:,range(b1,b2)]
            tempcropacceptorArray = newacceptorArray[range(a1,a2),:]
            self.cropacceptorArray = tempcropacceptorArray[:,range(b1,b2)]
            tempcropfretArray = newfretArray[range(a1,a2),:]
            self.cropfretArray = tempcropfretArray[:,range(b1,b2)]

            tempcropdonorDispArray = newdonorDispArray[range(a1,a2),:]
            cropdonorDispArray = tempcropdonorDispArray[:,range(b1,b2)]
            cropdonorDispArray[cropdonorDispArray<0] = np.max(cropdonorDispArray)+(np.max(cropdonorDispArray)-np.min(cropdonorDispArray))/3
            tempcropacceptorDispArray = newacceptorDispArray[range(a1,a2),:]
            cropacceptorDispArray = tempcropacceptorDispArray[:,range(b1,b2)]
            cropacceptorDispArray[cropacceptorDispArray<0] = np.max(cropacceptorDispArray)+(np.max(cropacceptorDispArray)-np.min(cropacceptorDispArray))/3
            tempcropfretDispArray = newfretDispArray[range(a1,a2),:]
            cropfretDispArray = tempcropfretDispArray[:,range(b1,b2)]
            cropfretDispArray[cropfretDispArray<0] = np.max(cropfretDispArray)+(np.max(cropfretDispArray)-np.min(cropfretDispArray))/3
            tempROIArray = ROIArray[range(a1,a2),:]
            self.cropROIArray = tempROIArray[:,range(b1,b2)]
            cropROIDispArray = np.uint8(self.cropROIArray*255)


            imgfig2,axes2 = plt.subplots(2,4)
            imgfig2.canvas.set_window_title('Images after ROI selection and background substraction')           
            
            im21 = axes2[0,0].imshow(np.uint16(cropdonorDispArray), cmap = 'nipy_spectral')
            cbar21 = imgfig2.colorbar(im21, ax=axes2[0,0],orientation='horizontal')
            cbar21.ax.set_xticklabels(cbar21.ax.get_xticklabels(),rotation=90)
            axes2[0,0].set_title('Donor Channel')
            axes2[0,0].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,0].plot(whole_bkgdVal_donor)
            axes2[1,0].set_title('Donor Bkgd Level')
            
            
            im22 = axes2[0,1].imshow(np.uint16(cropacceptorDispArray), cmap = 'nipy_spectral')
            cbar22 = imgfig2.colorbar(im22, ax=axes2[0,1],orientation='horizontal')
            cbar22.ax.set_xticklabels(cbar22.ax.get_xticklabels(),rotation=90)
            axes2[0,1].set_title('Acceptor Channel')
            axes2[0,1].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,1].plot(whole_bkgdVal)
            axes2[1,1].set_title('Acceptor Bkgd Level')
                
            im23 = axes2[0,2].imshow(np.uint16(cropfretDispArray), cmap = 'nipy_spectral')
            cbar23 = imgfig2.colorbar(im23, ax=axes2[0,2],orientation='horizontal')
            cbar23.ax.set_xticklabels(cbar23.ax.get_xticklabels(),rotation=90)
            axes2[0,2].set_title('FRET Channel')
            axes2[0,2].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,2].plot(whole_bkgdVal_fret)
            axes2[1,2].set_title('FRET Bkgd Level')          

            axes2[0,3].imshow(cropROIDispArray, cmap = 'gray')
            axes2[0,3].set_title('ROI')
            axes2[0,3].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,3].plot(whole_gaussWidth)
            axes2[1,3].set_title('ROI Width')
                            
            self.step3Button_Clicked = True
            print("Finished step3")
            plt.show()               
                
    def step4Button_Click(self):
        if (self.step3Button_Clicked == True):
            textFile = open(os.path.abspath(self.imgpath) + "/Parameter.txt", "r")
            data = textFile.readlines()
            para = np.zeros(7,np.float_)
            count = 0
            for line in data:
                words = line.split()
                para[count] = np.float_(words[1])
                count = count+1
            textFile.close()

            cropdonorArrayVal = np.float_(self.cropdonorArray)
            cropacceptorArrayVal = np.float_(self.cropacceptorArray)
            cropfretArrayVal = np.float_(self.cropfretArray)

            cF = cropfretArrayVal - para[0]*cropdonorArrayVal/100 - para[1]*cropacceptorArrayVal/100

            E = np.zeros((cF.shape[0],cF.shape[1]), np.float_)
            qD = cropdonorArrayVal
            Q_D = para[2]
            gainDARatio = para[3]
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (qD[i,j]+cF[i,j]*Q_D*gainDARatio != 0) & (self.cropROIArray[i,j] == 1):
                        E[i,j] = 100*(cF[i,j]*Q_D*gainDARatio)/(qD[i,j]+cF[i,j]*Q_D*gainDARatio)
                    if (qD[i,j]+cF[i,j]*Q_D*gainDARatio == 0) & (self.cropROIArray[i,j] == 1):
                        E[i,j] = np.inf
                        if cF[i,j]<0:
                            E[i,j] = -np.inf

            listCount = 0
            donorList = np.zeros(self.cropROIArray.sum())
            acceptorList = np.zeros(self.cropROIArray.sum())
            fretList = np.zeros(self.cropROIArray.sum())
            EList = np.zeros(self.cropROIArray.sum())
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (self.cropROIArray[i,j] == 1):
                        donorList[listCount] = cropdonorArrayVal[i,j]
                        acceptorList[listCount] = cropacceptorArrayVal[i,j]
                        fretList[listCount] = cropfretArrayVal[i,j]
                        EList[listCount] = E[i,j]
                        listCount = listCount + 1

            donorSigma = para[4]
            acceptorSigma = para[5]
            fretSigma = para[6]

            listCount = 0
            ESigmaList = np.zeros(self.cropROIArray.sum())
            cFSigma = np.float_(np.sqrt((cropfretArrayVal*fretSigma)**2 + (para[0]*cropdonorArrayVal*donorSigma)**2 + (para[1]*cropacceptorArrayVal*acceptorSigma)**2))
            ESigma = np.zeros((cF.shape[0],cF.shape[1]), np.float_)
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (cF[i,j] == 0) | ((cF[i,j] != 0) & (np.isinf(E[i,j])==True)):
                        ESigma[i,j] = np.inf
                    if (cF[i,j] != 0) & (np.isinf(E[i,j])==False):
                        A = np.square(np.divide(E[i,j]/100,cF[i,j]*Q_D*gainDARatio))
                        B = np.sqrt((cF[i,j]*Q_D*gainDARatio*donorSigma)**2 + (qD[i,j]*Q_D*gainDARatio*cFSigma[i,j])**2)
                        ESigma[i,j] = A*B
                    if (self.cropROIArray[i,j] == 1):
                        ESigmaList[listCount] = ESigma[i,j]
                        listCount = listCount + 1

            self.EList = EList
            self.ESigmaList = ESigmaList
            self.acceptorList = acceptorList
            self.cF = cF
            self.E = E
            self.ESigma = ESigma
            
            self.step4Button_Clicked = True
            print("Finished step4")

    def step5Button_Click(self):
        def getKey(item):
            return item[0]
        if (self.step4Button_Clicked == True):
            k = 0
            for i in range(0,len(self.ESigmaList)):
                if self.ESigmaList[i]<1e308:
                    if k==0:
                        newESigmaList = self.ESigmaList[i]
                    else:
                        newESigmaList = np.append(newESigmaList,self.ESigmaList[i])
                    k = k+1
            ESigma_mad = np.float_(median_absolute_deviation(newESigmaList))
            ESigma_median = np.float_(np.median(newESigmaList))
            numCertain = 0
            listcount = 0
            for ii in range(0,self.cropROIArray.sum()):
                if (self.ESigmaList[ii] > ESigma_median-ESigma_mad) & (self.ESigmaList[ii] < ESigma_median+ESigma_mad):
                	numCertain = numCertain + 1
                	if (self.acceptorList[ii] > 50):
	                    if listcount == 0:
	                        newacceptorEList = [[self.acceptorList[ii],self.EList[ii],self.ESigmaList[ii]]]
	                    else:
	                        newacceptorEList = np.append(newacceptorEList,[[self.acceptorList[ii],self.EList[ii],self.ESigmaList[ii]]],axis=0)
	                    listcount = listcount + 1

            sortaEList = np.asarray(sorted(newacceptorEList, key=getKey))
            E_avg = np.mean(sortaEList[:,1])
            E_median = np.median(sortaEList[:,1])
            ESigma_avg = np.mean(sortaEList[:,2])
            aECalArray = []
            windowSize = 30
            windowCount = 0
            while (windowCount+windowSize < listcount):
                if windowCount == 0:
                    aECalArrayBin = (sortaEList[windowCount,0]+sortaEList[windowCount+windowSize,0])/2
                    aECalArray = np.mean(sortaEList[range(windowCount,windowCount+windowSize),1])
                else:
                    windowval_mean = np.mean(sortaEList[range(windowCount,windowCount+windowSize),1])
                    aECalArrayBin = np.append(aECalArrayBin,(sortaEList[windowCount,0]+sortaEList[windowCount+windowSize,0])/2)
                    aECalArray = np.append(aECalArray,windowval_mean)
                windowCount = windowCount + windowSize
            NSig = 3
            cFDispArray = self.cF
            cFDispArray[cFDispArray > 2000] = 2000
            cFDispArray[cFDispArray < 0] = 2000
            EDispArray = self.E
            EDispArray[EDispArray > 100] = 120
            EDispArray[EDispArray < 0] = 120
            ESigmaDispArray = self.ESigma
            ESigmaDispArray[ESigmaDispArray > ESigma_median+NSig*ESigma_mad] = ESigma_median+(NSig+1)*ESigma_mad
            ESigmaDispArray[ESigmaDispArray < 0] = ESigma_median+(NSig+1)*ESigma_mad

            self.result1Str.set(u"%2.1f" %E_median)
            self.result2Str.set(u"%2.1f" %E_avg)
            self.result3Str.set(u"%5.0f" %self.cropROIArray.sum())
            numUncertain = self.cropROIArray.sum()-numCertain
            self.result4Str.set(u"%5.0f" %numUncertain)
            self.result5Str.set(u"%2.1f" %ESigma_avg)
            self.result6Str.set(u"%5.0f" %listcount)


            textFile = open(os.path.abspath(self.imgpath) + "/field_of_node_" + self.neuronname + ".txt", "w")
            textFile.write("Median of FRET efficiency: %2.1f\n" %E_median)
            textFile.write("Mean of FRET efficiency: %2.1f\n" %E_avg)
            textFile.write("Total # of pixels in ROI: %5.0f\n" %self.cropROIArray.sum())
            textFile.write("# of uncertain pixels: %5.0f\n" %numUncertain)
            textFile.write("Average of uncertainty: %2.1f\n" %ESigma_avg)
            textFile.write("# of pixels in final quantification: %5.0f\n" %listcount)
            textFile.close()


            imgfig3,axes3 = plt.subplots(2,3)
            imgfig3.canvas.set_window_title('FRET Characterization')
                                       
            im31 = axes3[0,0].imshow(np.uint16(cFDispArray), cmap = 'nipy_spectral')
            cbar31 = imgfig3.colorbar(im31, ax=axes3[0,0],orientation='horizontal')
            cbar31.ax.set_xticklabels(cbar31.ax.get_xticklabels(),rotation=90)
            axes3[0,0].set_title('FRET Signal')
            axes3[0,0].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            im32 = axes3[0,1].imshow(np.uint16(EDispArray), cmap = 'nipy_spectral')
            cbar32 = imgfig3.colorbar(im32, ax=axes3[0,1],orientation='horizontal')
            cbar32.ax.set_xticklabels(cbar32.ax.get_xticklabels(),rotation=90)
            axes3[0,1].set_title('FRET Efficiency')
            axes3[0,1].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            im33 = axes3[0,2].imshow(np.uint16(ESigmaDispArray), cmap = 'nipy_spectral')
            cbar33 = imgfig3.colorbar(im33, ax=axes3[0,2],orientation='horizontal')
            cbar33.ax.set_xticklabels(cbar33.ax.get_xticklabels(),rotation=90)
            axes3[0,2].set_title('Uncertainty')
            axes3[0,2].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            aplot = sortaEList[:,0]
            eplot = sortaEList[:,1]
            uplot = sortaEList[:,2]

            axes3[1,0].scatter(np.float_(uplot),np.float_(eplot), s = 5)
            axes3[1,0].set_title('FRET Efficiency V.S Uncertainty')
            axes3[1,0].set_xlabel('Uncertainty')
            axes3[1,0].set_ylabel('FRET Efficiency')
            axes3[1,0].set_xlim(0, 1000)
            axes3[1,0].set_ylim(0, 100)
            
            # colorList = (np.float_(self.ESigmaList)-(np.float_(ESigma_median)-NSig*ESigma_mad))/(ESigma_mad*NSig)
            # colorList[colorList>1] = 2
            # colorList[colorList<0] = 2

            # axes3[1,1].scatter(np.float_(self.acceptorList),np.float_(self.EList), c = colorList, s = 5, cmap=cm.jet)
            axes3[1,1].scatter(np.float_(aplot),np.float_(eplot), c = np.int_(uplot), s = 5, cmap=cm.jet)
            axes3[1,1].plot(aECalArrayBin,aECalArray, 'k-')
            axes3[1,1].set_title('FRET Efficiency V.S Acceptor')
            axes3[1,1].set_xlabel('Acceptor')
            axes3[1,1].set_ylabel('FRET Efficiency')
            axes3[1,1].set_xlim(0, 1350)
            axes3[1,1].set_ylim(0, 100)

            
            axes3[1,2].scatter(np.float_(aplot),np.float_(uplot), s = 5)
            axes3[1,2].set_title('Uncertainty V.S Acceptor')
            axes3[1,2].set_xlabel('Acceptor')
            axes3[1,2].set_ylabel('Uncertainty')
            axes3[1,2].set_ylim(0, 1000)

            self.step5Button_Clicked = True
            plt.show()
            
    
if __name__ == "__main__":
    FRETapp = Module_FRETanalysis(None)
    FRETapp.title('Modules for FRET analysis')
    FRETapp.mainloop()
    
