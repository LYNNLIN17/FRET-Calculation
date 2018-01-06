import Tkinter as tk
import tkFileDialog
import os.path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector


class Module_FRETanalysis(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        modulenameLabel = tk.Label(self, text="Module 3: FRET Calculation for Embryo")
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


        step2Button = tk.Button(self,text=u"Step2: Select Background in Acceptor", command=self.step2Button_Click)
        step2Button.grid(row=2, column=0, columnspan=150, sticky='W')
        self.abkgdrect = tk.StringVar()
        abkgdrectLabel = tk.Label(self, textvariable=self.abkgdrect)
        abkgdrectLabel.grid(row=2, column=151, columnspan=100, sticky='W')
        self.abkgdrect.set(u"")

        
        step3Button = tk.Button(self,text=u"Step3: Select ROI in Acceptor", command=self.step3Button_Click)
        step3Button.grid(row=3, column=0, columnspan=150, sticky='W')
        self.aroirect = tk.StringVar()
        aroirectLabel = tk.Label(self, textvariable=self.aroirect)
        aroirectLabel.grid(row=3, column=151, columnspan=100, sticky='W')
        self.aroirect.set(u"")

        
        step4Button = tk.Button(self,text=u"Step4: Background Substraction", command=self.step4Button_Click)
        step4Button.grid(row=4, column=0, columnspan=150, sticky='W')

        step5Button = tk.Button(self,text=u"Step4: FRET Efficiency and Uncertainty Calculation", command=self.step5Button_Click)
        step5Button.grid(row=5, column=0, columnspan=150, sticky='W')
        

        self.testStr1 = tk.StringVar()
        testLabel1 = tk.Label(self, textvariable=self.testStr1, fg="red")
        testLabel1.grid(row=6, column=0, sticky='W')
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
        self.step5Button_Checked = False
        self.haveFinished = np.array([0,0])

                
    def pathEntry_Enter(self, event):
        self.imgpath = self.pathStr.get()
        self.pathEntry.focus_set()
        self.pathEntry.selection_range(0, tk.END)
    
    def getpathButton_Click(self):
        imgfullpath = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",
            filetypes = (("tif files","*.tif"),("all files","*.*")))
        self.imgpath = os.path.dirname(imgfullpath)
        self.pathStr.set(self.imgpath)

    def getrect_Callback(self, eclick, erelease):
        self.x1, self.y1 = np.rint(eclick.xdata), np.rint(eclick.ydata)
        self.x2, self.y2 = np.rint(erelease.xdata), np.rint(erelease.ydata)

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
                
                self.imgfig1,self.axes1 = plt.subplots(1,3)
                self.imgfig1.canvas.set_window_title('Original Images')
                
               
                im1 = self.axes1[0].imshow(self.donorArray, cmap = 'nipy_spectral')
                cbar1 = self.imgfig1.colorbar(im1, ax=self.axes1[0],orientation='horizontal')
                cbar1.ax.set_xticklabels(cbar1.ax.get_xticklabels(),rotation=90)
                self.axes1[0].set_title('Donor Channel')
                self.axes1[0].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                
                im2 = self.axes1[1].imshow(self.acceptorArray, cmap = 'nipy_spectral')
                cbar2 = self.imgfig1.colorbar(im2, ax=self.axes1[1],orientation='horizontal')
                cbar2.ax.set_xticklabels(cbar2.ax.get_xticklabels(),rotation=90)
                self.axes1[1].set_title('Acceptor Channel')
                self.axes1[1].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                im3 = self.axes1[2].imshow(self.fretArray, cmap = 'nipy_spectral')
                cbar3 = self.imgfig1.colorbar(im3, ax=self.axes1[2],orientation='horizontal')
                cbar3.ax.set_xticklabels(cbar3.ax.get_xticklabels(),rotation=90)
                self.axes1[2].set_title('FRET Channel')
                self.axes1[2].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                        
                plt.show()
                        
    def step2Button_Click(self):
        if self.step2Button_Checked:
            self.step2Button_Checked = False
            self.haveFinished[0] = 1
            self.abkgdrect.set(u"(%3d, %3d, %3d, %3d)" % (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            self.abkgdrectArray = np.array([self.x1, self.y1, self.x2, self.y2])
            self.r1.set_active(False)
        else:
            self.step2Button_Checked = True
            self.r1 = RectangleSelector(self.axes1[1], self.getrect_Callback, drawtype='box', useblit=True,
                                       button=[1, 3], minspanx=5, minspany=5, spancoords='pixels',
                                       interactive=True)
            plt.show()
    
    def step3Button_Click(self):
        if self.step3Button_Checked:
            self.step3Button_Checked = False
            self.haveFinished[1] = 1
            self.aroirect.set(u"(%3d, %3d, %3d, %3d)" % (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            self.aroirectArray = np.array([self.x1, self.y1, self.x2, self.y2])
            self.r2.set_active(False)
        else:
            self.step3Button_Checked = True
            self.r2 = RectangleSelector(self.axes1[1], self.getrect_Callback, drawtype='box', useblit=True,
                                       button=[1, 3], minspanx=5, minspany=5, spancoords='pixels',
                                       interactive=True)
            plt.show()

    def step4Button_Click(self):
        if (np.all(self.haveFinished) == True) & (self.step2Button_Checked==False) & (self.step3Button_Checked==False):         
            abkgdrectArray = np.int_(self.abkgdrectArray)
            aroirectArray = np.int_(self.aroirectArray)
            
            aimgMat = np.int_(self.acceptorArray[abkgdrectArray[1]:abkgdrectArray[3],abkgdrectArray[0]:abkgdrectArray[2]])
            bkgdVal = np.int_(np.median(aimgMat))

            dimgMat = np.int_(self.donorArray[abkgdrectArray[1]:abkgdrectArray[3],abkgdrectArray[0]:abkgdrectArray[2]])
            bkgdVal_donor = np.int_(np.median(dimgMat))

            fimgMat = np.int_(self.fretArray[abkgdrectArray[1]:abkgdrectArray[3],abkgdrectArray[0]:abkgdrectArray[2]])
            bkgdVal_fret = np.int_(np.median(fimgMat))


            cropacceptorArray = self.acceptorArray[aroirectArray[1]:aroirectArray[3],aroirectArray[0]:aroirectArray[2]]-bkgdVal
            cropdonorArray = self.donorArray[aroirectArray[1]:aroirectArray[3],aroirectArray[0]:aroirectArray[2]]-bkgdVal_donor
            cropfretArray = self.fretArray[aroirectArray[1]:aroirectArray[3],aroirectArray[0]:aroirectArray[2]]-bkgdVal_fret

            for i in range(0,cropacceptorArray.shape[0]):
                for j in range(0,cropacceptorArray.shape[1]):
                    if cropacceptorArray[i,j]<0:
                        cropacceptorArray[i,j]=0
                    if cropdonorArray[i,j]<0:
                        cropdonorArray[i,j]=0
                    if cropfretArray[i,j]<0:
                        cropfretArray[i,j]=0

            self.cropacceptorArray = np.uint16(cropacceptorArray)
            self.cropdonorArray = np.uint16(cropdonorArray)
            self.cropfretArray = np.uint16(cropfretArray)
                
            imgfig2,axes2 = plt.subplots(1,3)
            imgfig2.canvas.set_window_title('Images after background substraction')
                    
            im4 = axes2[0].imshow(self.cropdonorArray, cmap = 'nipy_spectral')
            cbar4 = imgfig2.colorbar(im4, ax=axes2[0],orientation='horizontal')
            cbar4.ax.set_xticklabels(cbar4.ax.get_xticklabels(),rotation=90)
            axes2[0].set_title('Donor Channel')
            axes2[0].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

                
            im5 = axes2[1].imshow(self.cropacceptorArray, cmap = 'nipy_spectral')
            cbar5 = imgfig2.colorbar(im5, ax=axes2[1],orientation='horizontal')
            cbar5.ax.set_xticklabels(cbar5.ax.get_xticklabels(),rotation=90)
            axes2[1].set_title('Acceptor Channel')
            axes2[1].tick_params(axis='both', which='both',
                        bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

                    
            im6 = axes2[2].imshow(self.cropfretArray, cmap = 'nipy_spectral')
            cbar6 = imgfig2.colorbar(im6, ax=axes2[2],orientation='horizontal')
            cbar6.ax.set_xticklabels(cbar6.ax.get_xticklabels(),rotation=90)
            axes2[2].set_title('FRET Channel')
            axes2[2].tick_params(axis='both', which='both',
                                bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')

                
            self.step4Button_Clicked = True
                
            plt.show() 
                
    def step5Button_Click(self):
        if (self.step4Button_Clicked == True):
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
                    if cF[i,j] < 0:
                        cF[i,j] = 0

            E = np.zeros((cF.shape[0],cF.shape[1]), np.float_)
            qD = cropdonorArrayVal
            Q_D = 0.85
            gainDARatio = 1.15
            for i in range(0,cF.shape[0]):
                for j in range(0,cF.shape[1]):
                    if (qD[i,j] != 0) & (cF[i,j] != 0):
                        E[i,j] = 100*(cF[i,j]*Q_D*gainDARatio)/(qD[i,j]+cF[i,j]*Q_D*gainDARatio)

            donorSigma = np.float_(np.std(cropdonorArrayVal))
            acceptorSigma = np.float_(np.std(cropacceptorArrayVal))
            fretSigma = np.float_(np.std(cropfretArrayVal))

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
            
            self.step5Button_Clicked = True
            plt.show()

    
    
if __name__ == "__main__":
    FRETapp = Module_FRETanalysis(None)
    FRETapp.title('Modules for FRET analysis')
    FRETapp.mainloop()
    
