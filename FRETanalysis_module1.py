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

        modulenameLabel = tk.Label(self, text="Module 1: Bleedthrough Correction")
        modulenameLabel.grid(row=0, column=0, sticky='W')

        
        getpathButton = tk.Button(self,text=u"Select Image Path", command = self.getpathButton_Click)
        getpathButton.grid(row=1, column=151, columnspan=100, sticky='W')

        
        self.pathStr = tk.StringVar()
        self.pathEntry = tk.Entry(self,textvariable=self.pathStr)
        self.pathEntry.grid(row=1, column=251, columnspan=150, sticky='W')
        self.pathEntry.bind("<Return>", self.pathEntry_Enter)
        self.pathStr.set(u"")
        self.imgpath = ""
        

        step1Button = tk.Button(self,text=u"Step1: Load Bleedthrough Images", command=self.step1Button_Click)
        step1Button.grid(row=1, column=0, columnspan=150, sticky='W')


        step2Button = tk.Button(self,text=u"Step2: Select Bkgd in Donor", command=self.step2Button_Click)
        step2Button.grid(row=2, column=0, columnspan=150, sticky='W')
        self.dbkgdrect = tk.StringVar()
        dbkgdrectLabel = tk.Label(self, textvariable=self.dbkgdrect)
        dbkgdrectLabel.grid(row=2, column=151, columnspan=100, sticky='W')
        self.dbkgdrect.set(u"")


        step3Button = tk.Button(self,text=u"Step3: Select ROI in Donor", command=self.step3Button_Click)
        step3Button.grid(row=3, column=0, columnspan=150, sticky='W')
        self.droirect = tk.StringVar()
        droirectLabel = tk.Label(self, textvariable=self.droirect)
        droirectLabel.grid(row=3, column=151, columnspan=100, sticky='W')
        self.droirect.set(u"")


        step4Button = tk.Button(self,text=u"Step4: Select Bkgd in Acceptor", command=self.step4Button_Click)
        step4Button.grid(row=4, column=0, columnspan=150, sticky='W')
        self.abkgdrect = tk.StringVar()
        abkgdrectLabel = tk.Label(self, textvariable=self.abkgdrect)
        abkgdrectLabel.grid(row=4, column=151, columnspan=100, sticky='W')
        self.abkgdrect.set(u"")


        step5Button = tk.Button(self,text=u"Step5: Select ROI in Acceptor", command=self.step5Button_Click)
        step5Button.grid(row=5, column=0, columnspan=150, sticky='W')
        self.aroirect = tk.StringVar()
        aroirectLabel = tk.Label(self, textvariable=self.aroirect)
        aroirectLabel.grid(row=5, column=151, columnspan=100, sticky='W')
        self.aroirect.set(u"")

        step6Button = tk.Button(self,text=u"Step6: Bleedthrough Correction", command=self.step6Button_Click)
        step6Button.grid(row=6, column=0, columnspan=150, sticky='W')

        step7Button = tk.Button(self,text=u"Step7: Update paramerters", command=self.step7Button_Click)
        step7Button.grid(row=7, column=0, columnspan=150, sticky='W')

        self.testStr = tk.StringVar()
        testLabel = tk.Label(self, textvariable=self.testStr, fg="red")
        testLabel.grid(row=8, column=0, sticky='W')
        self.testStr.set(u"Start the procedure by following the steps!")

        self.deltaStr = tk.StringVar()
        deltaLabel = tk.Label(self, textvariable=self.deltaStr, fg="blue")
        deltaLabel.grid(row=9, column=0, sticky='W')
        self.deltaStr.set(u"delta = ")

        self.alphaStr = tk.StringVar()
        alphaLabel = tk.Label(self, textvariable=self.alphaStr, fg="blue")
        alphaLabel.grid(row=10, column=0, sticky='W')
        self.alphaStr.set(u"alpha = ")

        para1Label = tk.Label(self, text="Q_D")
        para1Label.grid(row=11, column=0, columnspan=50, sticky='W')
        self.paraStr_QD = tk.StringVar()
        self.QDEntry = tk.Entry(self,textvariable=self.paraStr_QD)
        self.QDEntry.grid(row=11, column=51, columnspan=50, sticky='W')
        self.paraStr_QD.set(u"0.85")

        para2Label = tk.Label(self, text="Gain Ratio")
        para2Label.grid(row=12, column=0, columnspan=50, sticky='W')
        self.paraStr_gainratio = tk.StringVar()
        self.gainratioEntry = tk.Entry(self,textvariable=self.paraStr_gainratio)
        self.gainratioEntry.grid(row=12, column=51, columnspan=50, sticky='W')
        self.paraStr_gainratio.set(u"1.15")

        para3Label = tk.Label(self, text="Sigma of donor")
        para3Label.grid(row=13, column=0, columnspan=50, sticky='W')
        self.paraStr_sigmadonor = tk.StringVar()
        self.sigmadonorEntry = tk.Entry(self,textvariable=self.paraStr_sigmadonor)
        self.sigmadonorEntry.grid(row=13, column=51, columnspan=50, sticky='W')
        self.paraStr_sigmadonor.set(u"9")

        para4Label = tk.Label(self, text="Sigma of acceptor")
        para4Label.grid(row=14, column=0, columnspan=50, sticky='W')
        self.paraStr_sigmaacceptor = tk.StringVar()
        self.sigmaacceptorEntry = tk.Entry(self,textvariable=self.paraStr_sigmaacceptor)
        self.sigmaacceptorEntry.grid(row=14, column=51, columnspan=50, sticky='W')
        self.paraStr_sigmaacceptor.set(u"7.2")

        para5Label = tk.Label(self, text="Sigma of fret")
        para5Label.grid(row=15, column=0, columnspan=50, sticky='W')
        self.paraStr_sigmafret = tk.StringVar()
        self.sigmafretEntry = tk.Entry(self,textvariable=self.paraStr_sigmafret)
        self.sigmafretEntry.grid(row=15, column=51, columnspan=50, sticky='W')
        self.paraStr_sigmafret.set(u"7.2")


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
        self.step6Button_Checked = False
        self.haveFinished = np.array([0,0,0,0])
                
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
                self.step1Button_Clicked = True
                
                donorBleedThrou = Image.open(os.path.abspath(self.imgpath) + "/donorBleedThrou.tif")
                self.dbtArray = np.array(donorBleedThrou)
                
                dfretBleedThrou = Image.open(os.path.abspath(self.imgpath) + "/dfretBleedThrou.tif")
                self.dfretbtArray = np.array(dfretBleedThrou)
                
                acceptorBleedThrou = Image.open(os.path.abspath(self.imgpath) + "/acceptorBleedThrou.tif")
                self.abtArray = np.array(acceptorBleedThrou)
                
                afretBleedThrou = Image.open(os.path.abspath(self.imgpath) + "/afretBleedThrou.tif")
                self.afretbtArray = np.array(afretBleedThrou)
        
                self.imgfig, self.axes = plt.subplots(2,2)
                
                
                im1 = self.axes[0,0].imshow(self.dbtArray, cmap='nipy_spectral')
                self.imgfig.colorbar(im1, ax=self.axes[0,0])
                self.axes[0,0].set_title('Donor Channel')
                self.axes[0,0].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                self.axes[0,0].set_ylabel('Donor Bleedthrough')
                
                
                im2 = self.axes[0,1].imshow(self.dfretbtArray, cmap='nipy_spectral')
                self.imgfig.colorbar(im2, ax=self.axes[0,1])
                self.axes[0,1].set_title('FRET Channel')
                self.axes[0,1].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                
                
                im3 = self.axes[1,0].imshow(self.abtArray, cmap = 'nipy_spectral')
                self.imgfig.colorbar(im3, ax=self.axes[1,0])
                self.axes[1,0].set_title('Acceptor Channel')
                self.axes[1,0].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
                self.axes[1,0].set_ylabel('Acceptor Bleedthrough')
            
            	
            	im4 = self.axes[1,1].imshow(self.afretbtArray, cmap = 'nipy_spectral')
            	self.imgfig.colorbar(im4, ax=self.axes[1,1])
                self.axes[1,1].set_title('FRET Channel')
                self.axes[1,1].tick_params(axis='both', which='both',
                            bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
        
                plt.show()
        
    def step2Button_Click(self):
        if self.step2Button_Checked:
            self.step2Button_Checked = False
            self.haveFinished[0] = 1
            self.dbkgdrect.set(u"(%3d, %3d, %3d, %3d)" % (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            self.dbkgdrectArray = np.array([self.x1, self.y1, self.x2, self.y2])
            self.r1.set_active(False)
        else:
            self.step2Button_Checked = True
            self.r1 = RectangleSelector(self.axes[0,0], self.getrect_Callback, drawtype='box', useblit=True,
                                       button=[1, 3], minspanx=5, minspany=5, spancoords='pixels',
                                       interactive=True)
            plt.show()
        

    def step3Button_Click(self):
        if self.step3Button_Checked:
            self.step3Button_Checked = False
            self.haveFinished[1] = 1
            self.droirect.set(u"(%3d, %3d, %3d, %3d)" % (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            self.droirectArray = np.array([self.x1, self.y1, self.x2, self.y2])
            self.r2.set_active(False)
        else:
            self.step3Button_Checked = True
            self.r2 = RectangleSelector(self.axes[0,0], self.getrect_Callback, drawtype='box', useblit=True,
                                       button=[1, 3], minspanx=5, minspany=5, spancoords='pixels',
                                       interactive=True)
            plt.show()

    def step4Button_Click(self):
        if self.step4Button_Checked:
            self.step4Button_Checked = False
            self.haveFinished[2] = 1
            self.abkgdrect.set(u"(%3d, %3d, %3d, %3d)" % (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            self.abkgdrectArray = np.array([self.x1, self.y1, self.x2, self.y2])
            self.r3.set_active(False)
        else:
            self.step4Button_Checked = True
            self.r3 = RectangleSelector(self.axes[1,0], self.getrect_Callback, drawtype='box', useblit=True,
                                       button=[1, 3], minspanx=5, minspany=5, spancoords='pixels',
                                       interactive=True)
            plt.show()

    def step5Button_Click(self):
        if self.step5Button_Checked:
            self.step5Button_Checked = False
            self.haveFinished[3] = 1
            self.aroirect.set(u"(%3d, %3d, %3d, %3d)" % (self.x1, self.y1, self.x2-self.x1, self.y2-self.y1))
            self.aroirectArray = np.array([self.x1, self.y1, self.x2, self.y2])
            self.r4.set_active(False)
        else:
            self.step5Button_Checked = True
            self.r4 = RectangleSelector(self.axes[1,0], self.getrect_Callback, drawtype='box', useblit=True,
                                       button=[1, 3], minspanx=5, minspany=5, spancoords='pixels',
                                       interactive=True)
            plt.show()

    def step6Button_Click(self):
        if (np.all(self.haveFinished) == True) & (self.step2Button_Checked==False) & (self.step3Button_Checked==False) & (self.step4Button_Checked==False) & (self.step5Button_Checked==False):
            
            dbtArray = np.float_(self.dbtArray)
            dfretbtArray = np.float_(self.dfretbtArray)
            abtArray = np.float_(self.abtArray)
            afretbtArray = np.float_(self.afretbtArray)

            dbkgdrectArray = np.int_(self.dbkgdrectArray)
            droirectArray = np.int_(self.droirectArray)
            abkgdrectArray = np.int_(self.abkgdrectArray)
            aroirectArray = np.int_(self.aroirectArray)
            

            dbkgdArray = dbtArray[dbkgdrectArray[1]:dbkgdrectArray[3],dbkgdrectArray[0]:dbkgdrectArray[2]]
            mdBkgd = np.median(dbkgdArray)
            dfretbkgdArray = dfretbtArray[dbkgdrectArray[1]:dbkgdrectArray[3],dbkgdrectArray[0]:dbkgdrectArray[2]]
            mdfretBkgd = np.median(dfretbkgdArray)

            sumdBt = 0
            N = 0
            for i in range(droirectArray[1],droirectArray[3]+1):
                for j in range(droirectArray[0],droirectArray[2]+1):
                    if ((dbtArray[i,j]-mdBkgd) != 0):
                        temp = (dfretbtArray[i,j]-mdfretBkgd)/(dbtArray[i,j]-mdBkgd)
                    else:
                        temp = 0
                    sumdBt = sumdBt + temp
                    N = N + 1
                    
            self.delta = sumdBt/N*100;
            self.deltaStr.set(u"delta = %2.1f" %self.delta)
            
            abkgdArray = abtArray[abkgdrectArray[1]:abkgdrectArray[3],abkgdrectArray[0]:abkgdrectArray[2]]
            maBkgd = np.median(abkgdArray)
            afretbkgdArray = afretbtArray[abkgdrectArray[1]:abkgdrectArray[3],abkgdrectArray[0]:abkgdrectArray[2]]
            mafretBkgd = np.median(afretbkgdArray)

            sumdBt = 0
            N = 0
            for i in range(aroirectArray[1],aroirectArray[3]+1):
                for j in range(aroirectArray[0],aroirectArray[2]+1):
                    if ((abtArray[i,j]-maBkgd) != 0):
                        temp = (afretbtArray[i,j]-mafretBkgd)/(abtArray[i,j]-maBkgd)
                    else:
                        temp = 0
                    sumdBt = sumdBt + temp
                    N = N + 1
                    
            self.alpha = sumdBt/N*100;
            self.alphaStr.set(u"alpha = %2.1f" %self.alpha)

            self.step6Button_Checked = True

    def step7Button_Click(self):
        if (self.step6Button_Checked==True):
            Q_D = np.float_(self.paraStr_QD.get())
            gainDARatio = np.float_(self.paraStr_gainratio.get())
            donorSigma = np.float_(self.paraStr_sigmadonor.get())
            acceptorSigma = np.float_(self.paraStr_sigmaacceptor.get())
            fretSigma = np.float_(self.paraStr_sigmafret.get())
            textFile = open(os.path.abspath(self.imgpath) + "/Parameter.txt", "w")
            textFile.write("delta: %2.1f\n" %self.delta)
            textFile.write("alpha: %2.1f\n" %self.alpha)
            textFile.write("Q_D: %2.2f\n" %Q_D)
            textFile.write("GainRatio: %2.2f\n" %gainDARatio)
            textFile.write("SigmaDonor: %2.2f\n" %donorSigma)
            textFile.write("SigmaAcceptor: %2.2f\n" %acceptorSigma)
            textFile.write("SigmaFRET: %2.2f\n" %fretSigma)
            textFile.close()

    
if __name__ == "__main__":
    FRETapp = Module_FRETanalysis(None)
    FRETapp.title('Modules for FRET analysis')
    FRETapp.mainloop()
    
