import Tkinter as tk
import tkFileDialog
import os.path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.optimize import curve_fit
from scipy import exp


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
        

        step4Button = tk.Button(self,text=u"Step4: FRET Efficiency and Uncertainty Calculation", command=self.step4Button_Click)
        step4Button.grid(row=4, column=0, columnspan=150, sticky='W')
        

        self.testStr1 = tk.StringVar()
        testLabel1 = tk.Label(self, textvariable=self.testStr1, fg="red")
        testLabel1.grid(row=5, column=0, sticky='W')
        self.testStr1.set(u"Start the procedure by following the steps!")
        
                      
        self.grid_columnconfigure(0, weight=1)
        self.update()
        self.geometry(self.geometry())       
        self.pathEntry.focus_set()
        self.pathEntry.selection_range(0, tk.END)

        self.step1Button_Clicked = False
        self.step2Button_Checked = False
        self.step3Button_Checked = False
        self.step4Button_Checked = False

        self.drawNpt = 0
        self.finishDrawing = False

                
    def pathEntry_Enter(self, event):
        self.imgpath = self.pathStr.get()
        self.pathEntry.focus_set()
        self.pathEntry.selection_range(0, tk.END)
    
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
                
               
                im1 = axes1[0].imshow(self.donorArray, cmap = 'nipy_spectral')
                cbar1 = imgfig1.colorbar(im1, ax=axes1[0],orientation='horizontal')
                cbar1.ax.set_xticklabels(cbar1.ax.get_xticklabels(),rotation=90)
                axes1[0].set_title('Donor Channel')
                axes1[0].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                
                im2 = axes1[1].imshow(self.acceptorArray, cmap = 'nipy_spectral')
                cbar2 = imgfig1.colorbar(im2, ax=axes1[1],orientation='horizontal')
                cbar2.ax.set_xticklabels(cbar2.ax.get_xticklabels(),rotation=90)
                axes1[1].set_title('Acceptor Channel')
                axes1[1].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                im3 = axes1[2].imshow(self.fretArray, cmap = 'nipy_spectral')
                cbar3 = imgfig1.colorbar(im3, ax=axes1[2],orientation='horizontal')
                cbar3.ax.set_xticklabels(cbar3.ax.get_xticklabels(),rotation=90)
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
                cv2.circle(self.img, (ix,iy), 2, (0,65536,0))
                            
            elif (self.drawNpt > 0) & (self.finishDrawing == False):
                ix,iy = x,y
                self.drawNpt = self.drawNpt+1
                self.polylineX = np.append(self.polylineX,[ix],axis=0)
                self.polylineY = np.append(self.polylineY,[iy],axis=0)
                cv2.line(self.img, (self.polylineX[self.drawNpt-2],self.polylineY[self.drawNpt-2]), (ix,iy), (0,65536,0), 1)
                cv2.circle(self.img, (ix,iy), 2, (0,65536,0))

        elif event == cv2.EVENT_RBUTTONDOWN:
            if (self.drawNpt >= 2):
                self.finishDrawing = True
                print(self.polylineX)
                print(self.polylineY)
        
    def step2Button_Click(self):
        if (self.step1Button_Clicked == True):
            self.img = cv2.cvtColor(self.acceptorArray,cv2.COLOR_GRAY2RGB)

            cv2.namedWindow('Acceptor Channel')
            cv2.setMouseCallback('Acceptor Channel',self.drawMultiLineSegments)
            while (self.finishDrawing == False):
                cv2.imshow('Acceptor Channel',self.img)
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

            newacceptorArray = np.zeros((self.acceptorArray.shape[0],self.acceptorArray.shape[1]), np.uint16)
            newdonorArray = np.zeros((self.donorArray.shape[0],self.donorArray.shape[1]), np.uint16)
            newfretArray = np.zeros((self.fretArray.shape[0],self.fretArray.shape[1]), np.uint16)
            ROIArray = np.zeros((self.acceptorArray.shape[0],self.acceptorArray.shape[1]), np.int_)


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
                        gaussWidth = popt[2]
                        bkgdVal = popt[3]
                        self.bmean = centerPt
                        self.csigma = gaussWidth
                    else:
                        centerPt = np.append(centerPt,popt[1])
                        gaussWidth = np.append(gaussWidth,popt[2])
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
	                    	pxlInten = np.int_(self.acceptorArray[ii,xxfit[i]-1])-bkgdVal[i]
	                    	if pxlInten < 0:
	                        	pxlInten = 0
	                    	newacceptorArray[ii,xxfit[i]-1] = np.uint16(pxlInten)

	                    	pxlInten_donor = np.int_(self.donorArray[ii,xxfit[i]-1])-bkgdVal_donor[i]
	                    	if pxlInten_donor < 0:
	                        	pxlInten_donor = 0
	                        newdonorArray[ii,xxfit[i]-1] = np.uint16(pxlInten_donor)

	                        pxlInten_fret = np.int_(self.fretArray[ii,xxfit[i]-1])-bkgdVal_fret[i]
	                        if pxlInten_fret < 0:
	                            pxlInten_fret = 0
	                    	newfretArray[ii,xxfit[i]-1] = np.uint16(pxlInten_fret)
	                    	ROIArray[ii,xxfit[i]-1] = np.int_(1)
                        newacceptorArray[yyfit[i]-gaussWidth[i]-1+shiftCPt-1,xxfit[i]-1] = np.uint16(2000)
                        newacceptorArray[yyfit[i]+gaussWidth[i]+shiftCPt,xxfit[i]-1] = np.uint16(2000)
                        newdonorArray[yyfit[i]-gaussWidth[i]-1+shiftCPt-1,xxfit[i]-1] = np.uint16(2000)
                        newdonorArray[yyfit[i]+gaussWidth[i]+shiftCPt,xxfit[i]-1] = np.uint16(2000)
                        newfretArray[yyfit[i]-gaussWidth[i]-1+shiftCPt-1,xxfit[i]-1] = np.uint16(2000)
                        newfretArray[yyfit[i]+gaussWidth[i]+shiftCPt,xxfit[i]-1] = np.uint16(2000)

                    
                elif (fitMode == 2):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(-gaussWidth[i]-1,gaussWidth[i]+1):
                            pxlInten = np.int_(self.acceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt])-bkgdVal[i]
                            if pxlInten < 0:
                                pxlInten = 0                        
                            newacceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.uint16(pxlInten)

                            pxlInten_donor = np.int_(self.donorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt])-bkgdVal_donor[i]
                            if pxlInten_donor < 0:
                                pxlInten_donor = 0                        
                            newdonorArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.uint16(pxlInten_donor)

                            pxlInten_fret = np.int_(self.fretArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt])-bkgdVal_fret[i]
                            if pxlInten_fret < 0:
                                pxlInten_fret = 0                        
                            newfretArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.uint16(pxlInten_fret)
                            ROIArray[yyfit[i]+ii+shiftCPt,xxfit[i]-ii-shiftCPt] = np.int_(1)
                        newacceptorArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]+gaussWidth[i]+2-shiftCPt] = np.uint16(2000)
                        newacceptorArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]-gaussWidth[i]-1-shiftCPt] = np.uint16(2000)
                        newdonorArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]+gaussWidth[i]+2-shiftCPt] = np.uint16(2000)
                        newdonorArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]-gaussWidth[i]-1-shiftCPt] = np.uint16(2000)
                        newfretArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]+gaussWidth[i]+2-shiftCPt] = np.uint16(2000)
                        newfretArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]-gaussWidth[i]-1-shiftCPt] = np.uint16(2000)

                elif (fitMode == 3):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(-gaussWidth[i]-1,gaussWidth[i]+1):
                            pxlInten = np.int_(self.acceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt])-bkgdVal[i]
                            if pxlInten < 0:
                                pxlInten = 0                        
                            newacceptorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.uint16(pxlInten)

                            pxlInten_donor = np.int_(self.donorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt])-bkgdVal_donor[i]
                            if pxlInten_donor < 0:
                                pxlInten_donor = 0                        
                            newdonorArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.uint16(pxlInten_donor)

                            pxlInten_fret = np.int_(self.fretArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt])-bkgdVal_fret[i]
                            if pxlInten_fret < 0:
                                pxlInten_fret = 0                        
                            newfretArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.uint16(pxlInten_fret)

                            ROIArray[yyfit[i]+ii+shiftCPt,xxfit[i]+ii+shiftCPt] = np.int_(1)
                        newacceptorArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]-gaussWidth[i]-2+shiftCPt] = np.uint16(2000)
                        newacceptorArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]+gaussWidth[i]+1+shiftCPt] = np.uint16(2000)
                        newdonorArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]-gaussWidth[i]-2+shiftCPt] = np.uint16(2000)
                        newdonorArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]+gaussWidth[i]+1+shiftCPt] = np.uint16(2000)
                        newfretArray[yyfit[i]-gaussWidth[i]-2+shiftCPt,xxfit[i]-gaussWidth[i]-2+shiftCPt] = np.uint16(2000)
                        newfretArray[yyfit[i]+gaussWidth[i]+1+shiftCPt,xxfit[i]+gaussWidth[i]+1+shiftCPt] = np.uint16(2000)
                    
                elif (fitMode == 4):
                    for i in range(0,len(xxfit)):
                        shiftCPt = np.int_(centerPt[i]-neuronWidth)
                        for ii in range(xxfit[i]-gaussWidth[i]-1+shiftCPt,xxfit[i]+gaussWidth[i]+shiftCPt):
	                        pxlInten = np.int_(self.acceptorArray[yyfit[i]-1,ii])-bkgdVal[i]
	                        if pxlInten < 0:
	                            pxlInten = 0                        
	                        newacceptorArray[yyfit[i]-1,ii] = np.uint16(pxlInten)

	                        pxlInten_donor = np.int_(self.donorArray[yyfit[i]-1,ii])-bkgdVal_donor[i]
	                        if pxlInten_donor < 0:
	                            pxlInten_donor = 0                        
	                        newdonorArray[yyfit[i]-1,ii] = np.uint16(pxlInten_donor)

	                        pxlInten_fret = np.int_(self.fretArray[yyfit[i]-1,ii])-bkgdVal_fret[i]
	                        if pxlInten_fret < 0:
	                            pxlInten_fret = 0                        
	                        newfretArray[yyfit[i]-1,ii] = np.uint16(pxlInten_fret)
                        	ROIArray[yyfit[i]-1,ii] = np.int_(np.repeat(1,len(ii)))
                        newacceptorArray[yyfit[i]-1,xxfit[i]-gaussWidth[i]-1+shiftCPt-1] = np.uint16(2000)
                        newacceptorArray[yyfit[i]-1,xxfit[i]+gaussWidth[i]+shiftCPt] = np.uint16(2000)
                        newdonorArray[yyfit[i]-1,xxfit[i]-gaussWidth[i]-1+shiftCPt-1] = np.uint16(2000)
                        newdonorArray[yyfit[i]-1,xxfit[i]+gaussWidth[i]+shiftCPt] = np.uint16(2000)
                        newfretArray[yyfit[i]-1,xxfit[i]-gaussWidth[i]-1+shiftCPt-1] = np.uint16(2000)
                        newfretArray[yyfit[i]-1,xxfit[i]+gaussWidth[i]+shiftCPt] = np.uint16(2000)

                
            imgfig2,axes2 = plt.subplots(2,4)
            # imgfig2,axes2 = plt.subplots(2,3)
            imgfig2.canvas.set_window_title('Images after ROI selection and background substraction')

            a1 = np.int_(np.amin(whole_yyfit)-5)
            a2 = np.int_(np.amax(whole_yyfit)+5)
            b1 = np.int_(np.amin(whole_xxfit)-5)
            b2 = np.int_(np.amax(whole_xxfit)+5)
               

            tempcropdonorArray = newdonorArray[range(a1,a2),:]
            self.cropdonorArray = tempcropdonorArray[:,range(b1,b2)]

            
            im4 = axes2[0,0].imshow(self.cropdonorArray, cmap = 'nipy_spectral')
            cbar4 = imgfig2.colorbar(im4, ax=axes2[0,0],orientation='horizontal')
            cbar4.ax.set_xticklabels(cbar4.ax.get_xticklabels(),rotation=90)
            axes2[0,0].set_title('Donor Channel')
            axes2[0,0].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,0].plot(whole_bkgdVal_donor)
            axes2[1,0].set_title('Donor Bkgd Level')
            
            tempcropacceptorArray = newacceptorArray[range(a1,a2),:]
            self.cropacceptorArray = tempcropacceptorArray[:,range(b1,b2)]

            
            im5 = axes2[0,1].imshow(self.cropacceptorArray, cmap = 'nipy_spectral')
            cbar5 = imgfig2.colorbar(im5, ax=axes2[0,1],orientation='horizontal')
            cbar5.ax.set_xticklabels(cbar5.ax.get_xticklabels(),rotation=90)
            axes2[0,1].set_title('Acceptor Channel')
            axes2[0,1].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,1].plot(whole_bkgdVal)
            axes2[1,1].set_title('Acceptor Bkgd Level')

            
            tempcropfretArray = newfretArray[range(a1,a2),:]
            self.cropfretArray = tempcropfretArray[:,range(b1,b2)]

                
            im6 = axes2[0,2].imshow(self.cropfretArray, cmap = 'nipy_spectral')
            cbar6 = imgfig2.colorbar(im6, ax=axes2[0,2],orientation='horizontal')
            cbar6.ax.set_xticklabels(cbar6.ax.get_xticklabels(),rotation=90)
            axes2[0,2].set_title('FRET Channel')
            axes2[0,2].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,2].plot(whole_bkgdVal_fret)
            axes2[1,2].set_title('FRET Bkgd Level')


            tempROIArray = ROIArray[range(a1,a2),:]
            self.cropROIArray = tempROIArray[:,range(b1,b2)]
            cropROIDispArray = np.uint8(self.cropROIArray*255)

            axes2[0,3].imshow(cropROIDispArray, cmap = 'gray')
            axes2[0,3].set_title('ROI')
            axes2[0,3].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            axes2[1,3].plot(whole_gaussWidth)
            axes2[1,3].set_title('ROI Width')
                            
            self.step3Button_Clicked = True
            
            plt.show()
                
                
                
    def step4Button_Click(self):
        if (self.step3Button_Clicked == True):
            textFile = open(os.path.abspath(self.imgpath) + "/Parameter.txt", "r")
            data = textFile.readlines()
            para = np.zeros(2,np.float_)
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
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (cF[i,j] < 0) | (self.cropROIArray[i,j] == 0):
                        cF[i,j] = 0

            E = np.zeros((cF.shape[0],cF.shape[1]), np.float_)
            qD = cropdonorArrayVal
            Q_D = 0.85
            gainDARatio = 1.15
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (qD[i,j] != 0) & (cF[i,j] != 0):
                        E[i,j] = 100*(cF[i,j]*Q_D*gainDARatio)/(qD[i,j]+cF[i,j]*Q_D*gainDARatio)

            listCount = 0
            donorList = np.zeros(self.cropROIArray.sum())
            acceptorList = np.zeros(self.cropROIArray.sum())
            fretList = np.zeros(self.cropROIArray.sum())
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (self.cropROIArray[i,j] == 1):
                        donorList[listCount] = cropdonorArrayVal[i,j]
                        acceptorList[listCount] = cropacceptorArrayVal[i,j]
                        fretList[listCount] = cropfretArrayVal[i,j]
                        listCount = listCount + 1

            donorSigma = np.float_(np.std(donorList))
            acceptorSigma = np.float_(np.std(acceptorList))
            fretSigma = np.float_(np.std(fretList))

            cFSigma = np.float_(np.sqrt(fretSigma**2 + (para[0]*donorSigma)**2 + (para[1]*acceptorSigma)**2))
            ESigma = np.zeros((cF.shape[0],cF.shape[1]), np.float_)
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (cF[i,j] != 0):
                        A = np.square(np.divide(E[i,j]/100,cF[i,j]*Q_D*gainDARatio))
                        B = np.sqrt((cF[i,j]*Q_D*gainDARatio*donorSigma)**2 + (qD[i,j]*Q_D*gainDARatio*cFSigma)**2)
                        ESigma[i,j] = A*B
            print (np.amax(ESigma))


            imgfig3,axes3 = plt.subplots(1,3)
            imgfig3.canvas.set_window_title('FRET Calculation')
                           
            im7 = axes3[0].imshow(np.uint16(cF), cmap = 'nipy_spectral')
            cbar7 = imgfig3.colorbar(im7, ax=axes3[0],orientation='horizontal')
            cbar7.ax.set_xticklabels(cbar7.ax.get_xticklabels(),rotation=90)
            axes3[0].set_title('FRET Signal')
            axes3[0].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            im8 = axes3[1].imshow(np.uint16(E), cmap = 'nipy_spectral')
            cbar8 = imgfig3.colorbar(im8, ax=axes3[1],orientation='horizontal')
            cbar8.ax.set_xticklabels(cbar8.ax.get_xticklabels(),rotation=90)
            axes3[1].set_title('FRET Efficiency')
            axes3[1].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

            im9 = axes3[2].imshow(np.uint16(ESigma), cmap = 'nipy_spectral')
            cbar9 = imgfig3.colorbar(im9, ax=axes3[2],orientation='horizontal')
            cbar9.ax.set_xticklabels(cbar9.ax.get_xticklabels(),rotation=90)
            axes3[2].set_title('Uncertainty')
            axes3[2].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
            
            self.step4Button_Clicked = True
            plt.show()

    
    
if __name__ == "__main__":
    FRETapp = Module_FRETanalysis(None)
    FRETapp.title('Modules for FRET analysis')
    FRETapp.mainloop()
    
