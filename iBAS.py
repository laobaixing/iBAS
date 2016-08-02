import os
import sys
import wx
# import wx.lib.filebrowsebutton as filebrowse

import numpy
import pandas as pd
from scipy import stats
from iFun import *
from iRpy import *
from iBAStable import *
from iBASdialog import *
from iBASfigure import FigurePanel
from iBASnotebook import Notebook
from iBASoutput import OutFrame

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title= "(iBAS) interactive Bioinformatics Analysis System" ,size=(1200, 600))
        
        self.data = []
        # define the Icon will be used by this frame
        ico = wx.Icon('pyramid3.png', wx.BITMAP_TYPE_ANY)
        self.SetIcon(ico)
        
        # status Bar can show the help information on menu etc. 
        self.CreateStatusBar()
        
        # set menuFile and menuBar
        menuFile = wx.Menu()
        menuFile.Append(1, "&Input files")
        menuFile.Append(2, "&Save")
        menuFile.Append(3, "&Save As")
        menuFile.AppendSeparator()
        menuFile.Append(4, "E&xit")
        
        menuAbout = wx.Menu()
        menuAbout.Append(10, "&About...")
        
        menuPretreat = wx.Menu()
        menuPretreat.Append(21, "&Batch effects", "Examine batch effects with PCA")
        menuPretreat.Append(24, "&Summary")   
        menuPretreat.Append(25, "&Log Transformation")
        
        menuStat = wx.Menu()
        menuStat.Append(31, "&T-test")
        menuStat.Append(32, "&Fisher-test")
        menuStat.Append(33, "&Correlation") 
        menuStat.Append(34, "&ANONA") 
        menuStat.Append(35, "&Logistic regression")   
        menuStat.Append(36, "&Linear Regression")          
        menuStat.Append(37, "&KM Curve")           
        menuStat.Append(38, "&Cox")                       
        
        menuML = wx.Menu()
        menuML.Append(41, "&Naive Bayes")    
        menuML.Append(42, "&Hierarchical Model")     
        menuML.Append(43, "&SVM")                            
        menuML.Append(44, "&Lasso and Elastic net")            
        menuML.Append(45, "&Coxnet")   
        
        # Bioinformatics menu include method to treat high dimension data, the method may come from statistics or machine learning    
        menuBioinfo = wx.Menu()
        menuBioinfo.Append(51, "&Heatmap")
        menuBioinfo.Append(52, "&Consensus Clustering")
        menuBioinfo.Append(53, "&NMF")    
        menuBioinfo.Append(54, "&FDR_ttest")   
        menuBioinfo.Append(55, "&FDR_Cox")  
        menuBioinfo.Append(56, "&Gaussian Graphical Model")                     

        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        menuBar.Append(menuPretreat, "&Pretreatment")
        menuBar.Append(menuStat, "&Statistics")        
        menuBar.Append(menuML, "&Machine-Learning")
        menuBar.Append(menuBioinfo, "&Bioinformatics-Tools")
        menuBar.Append(menuAbout, "&About")

        # add tool bars if there are suitable icon
        # self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
        # self.m_tool1 = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"name Format", wx.Bitmap( u"../../Icon/style_edit.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        # self.m_toolBar1.Realize() 
        
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnInputFile, id=1)
        self.Bind(wx.EVT_MENU, self.OnSave, id=2)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id=3)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=4)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=10)
        self.Bind(wx.EVT_MENU, self.OnT_test, id=31)
        self.Bind(wx.EVT_MENU, self.OnCor, id=33)
        self.Bind(wx.EVT_MENU, self.OnANOVA, id=34)
        self.Bind(wx.EVT_MENU, self.OnCox, id=38)
        self.Bind(wx.EVT_MENU, self.OnPCA, id=21)
        self.Bind(wx.EVT_MENU, self.OnCoxnet, id=45)
        self.Bind(wx.EVT_MENU, self.OnHeatmap, id=51)
        self.Bind(wx.EVT_MENU, self.OnFDR_ttest, id=54)
        self.Bind(wx.EVT_MENU, self.OnFDR_Cox, id=55)
                
        # make sizers of windows
        self.sizerMainFrame = wx.BoxSizer(wx.VERTICAL)

        # make 3 buttons on the top of the frame
        self.sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerMainFrame.Add(self.sizerBtns)

        btn1 = wx.Button(self, wx.ID_ANY, label="&Summary")
        btn2 = wx.Button(self, wx.ID_ANY, label="&Histogram")
        btnScatplot = wx.Button(self, wx.ID_ANY, label="&ScatterPlot")
        btn3 = wx.Button(self, wx.ID_ANY, label="&Layout")
        btnWorkFlow = wx.Button(self, wx.ID_ANY, label="&WorkFlow")
        btnGenCode = wx.Button(self, wx.ID_ANY, label="&GenCode")        
        
        self.sizerBtns.Add(btn1, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)
        self.sizerBtns.Add(btn2, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)
        self.sizerBtns.Add(btnScatplot, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5) 
        self.sizerBtns.Add(btn3, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)
        self.sizerBtns.Add(btnWorkFlow, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)        
        self.sizerBtns.Add(btnGenCode, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)    
        btnWorkFlow.Disable()
        btnGenCode.Disable()           

        self.Bind(wx.EVT_BUTTON, self.OnSummary, btn1)
        self.Bind(wx.EVT_BUTTON, self.OnHistogram, btn2)
        self.Bind(wx.EVT_BUTTON, self.OnScatplot, btnScatplot)
        self.Bind(wx.EVT_BUTTON, self.OnLayout, btn3)

        # make frame with notebook and figure (case 1)
        self.splitterTop1 = wx.SplitterWindow(self)
        self.sizerMainFrame.Add(self.splitterTop1, 1, wx.EXPAND)

        self.notebook = Notebook(self.splitterTop1, [])
        self.fgr = FigurePanel(self.splitterTop1, [])

        self.splitterTop1.SplitVertically(self.notebook, self.fgr, sashPosition=800)  # set the sash position explicitly, otherwise in windows, the left panel will not show
        # however with this method, the left panel size will not change, this is a problem of environment.
        self.splitterTop1.Show()

#         # make splitter window with tables and figure
#         self.splitterTop2 = wx.SplitterWindow(self)
#         self.sizerMainFrame.Add(self.splitterTop2, 1, wx.EXPAND)
# 
#         self.panelTopLeft2 = SplitterPanel(self.splitterTop2, [])
#         self.panelTopRight2 = FigurePanel(self.splitterTop2, [])
# 
#         self.splitterTop2.SplitVertically(self.panelTopLeft2, self.panelTopRight2)
#         self.splitterTop2.Hide()

        # update sizers
        self.SetSizer(self.sizerMainFrame)
        self.Layout()
        
    def ReadingData(self, path):
        data = getDataFromFile(path)
        return data        

    def OnInputFile(self, event):
        # get paths
        inputDlg = InputDataDialog()
        
        # read files
        # self.data store a list of data
        self.data = [self.ReadingData(inputDlg.GetPath()[n]) for n in range(inputDlg.GetInputFilesQuantityShowed())]

        # update notebook
        self.notebook.UpdateNotebook(self.data, [])  

    def OnSave(self, event):
        pass

    def OnSaveAs(self, event):
        pass

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        wx.MessageBox("Bioinformatics Analysis System for:\n \n indepth analysis \n integration of data\n interactive process \n interdisciplinary study \n \nAuthor: Shiyun Ling", "About...", wx.OK | wx.ICON_INFORMATION, self)

    def OnSummary(self, event):
        # output the mean, median, min, max of the data 
        # check the validation of the data
        number = self.notebook.GetCurrentDataId()
        data = self.notebook.data[number][1:]
        minVal, maxVal, meanVal = iBASsummary(data)
        
        output = "Min is " + str(minVal) + "\n" + "Max is " + str(maxVal) + "\n" + "Mean is " + str(meanVal)
        wx.MessageBox(output, "Summary", wx.OK | wx.ICON_INFORMATION, self)
  
    def OnHistogram(self, event):
        """ show the histogram of the data """
        # number = self.notebook.GetCurrentDataId()
        number = self.notebook.GetCurrentDataId()
        histDlg = InputXDialog(title=u"Input for histogram")
        pars = histDlg.GetValue()
        data = self.notebook.data[number]
        self.fgr.Hist(data, pars)
        
    def OnScatplot(self, event):
        """ show the scatter plot of two columns or rows """
        number = self.notebook.GetCurrentDataId()
        ScatplotDlg = InputXYDialog(title=u"Input for Scatter Plot")
        pair = ScatplotDlg.GetValue()
        data = self.notebook.data[number]      
        self.fgr.Scatplot(data, pair)
    
    def OnT_test(self, event):
        """ show the student test of two columns or rows """
        number = self.notebook.GetCurrentDataId()
        t_testDlg = InputXYDialog(title=u"Input for t-test")
        pair = t_testDlg.GetValue()
        data = self.notebook.data[number]
        numData = data[1:]
        direction = pair[0]
        if direction == "Col":
            x = pair[1]
            y = pair[2]
        elif direction == "Row":
            x = pair[1]-1
            y = pair[2]-1
        res = iBAS_ttest(numData, direction, x, y)
        output = "t-statistics is " + str(res[0]) + "\n" + "p-value is "  + str(res[1])     
        wx.MessageBox(output, "t-test result", wx.OK | wx.ICON_INFORMATION, self)
        
    def OnCor(self, event):
        """ Show the correlation between two columns or rows """
        number = self.notebook.GetCurrentDataId()
        corDlg = InputXYDialog(title=u"Input for correlation study")
        pair = corDlg.GetValue()
        data = self.notebook.data[number]      
        numData = data[1:]
        direction = pair[0]
        if direction == "Col":
            x = pair[1]
            y = pair[2]
        elif direction == "Row":
            x = pair[1]-1    # when there is a header row
            y = pair[2]-1  
        res = iBAS_Cor(numData, direction, x, y)      
        output = "The pearson correlation is " +  str(round(res[0], 3)) + "\n" + "p-value is "  +  str( round(res[1], 3) )    
        wx.MessageBox(output, "Correlation result", wx.OK | wx.ICON_INFORMATION, self)
    
    def OnANOVA(self, event):        
        pass

    def OnCox(self, event):
        number = self.notebook.GetCurrentDataId()
        coxDlg = InputSurvDialog(title=u"Input for cox analysis")
        vars = coxDlg.GetValue()
        
        data = self.notebook.data[number]
        summary = coxphPy(data, vars)
        pvalue = summary.rx2("logtest")[2]
        output = "p-value of cox survival analysis is "  + str(pvalue)     
        wx.MessageBox(output, "Cox survival analysis result", wx.CENTER, self)
    
    def OnCoxnet(self, event):
        number = self.notebook.GetCurrentDataId()
        coxnetDlg = DialogCox(title=u"Input for cox-lasso survival analysis")
        vars = coxnetDlg.GetValue()  
        
        data = self.notebook.data[number]
        timeColnum = vars[0]
        censorColnum = vars[1]
        varsColStart = vars[2]
        res = coxnet (data, timeColnum, censorColnum, varsColStart )
        output = OutFrame("notebook", res, "Coxnet")   
        output.Show()   
    
    def OnPCA(self, event):   # this function rely on vegan package
        number = self.notebook.GetCurrentDataId()
        pcaDlg = DialogPCA(title=u"Input for PCA")   
        startColNum, groupColNum = pcaDlg.GetValue()
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        base = importr("base")
        vegan = importr("vegan")
        graphics = importr("graphics")
        stats = importr("stats") 
               
        data = self.notebook.data[number]
        
        # need to transpose if the sample is arranged along with column
        # python array is arranged by row
        # PCA is calculated with row
        numData = numpy.array(data)[1:,startColNum: ].astype(float)
        grp = numpy.array(data)[1:, groupColNum]
        # colsDic = {1:"red", 2:"orange", 3:"blue", 4:"forestgreen"}
        groupColDic = getCategoryColorDic (list(set(grp)), colsDic)
        cols = getMemberColor(grp, groupColDic)        
        # col = [colsDic[x] for x in grp]
        # print col
        from rpy2.robjects import numpy2ri
        numpy2ri.activate()   # transfer the numpy array to matrix in R
        pca = vegan.rda(numData, scale = True)       
        
        col4R = robjects.StrVector(cols) # for vector, need to transfer explicitly, numpy2ri didn't work
        scl = 1 ## scaling
        
        graphics.plot(pca, display = "sites", scaling = scl , type = "n")
        # stats.biplot(pca, main = "biplot")
        graphics.points(pca, display = "sites", scaling = scl, col = col4R, pch = 16)  # color map to the group
        # lev = base.levels(grp)
        lev = list(set(grp))
        # print lev
        # please note the order of group set from python and R is different. next time just try to use one method
        for i in range(len(lev)):
            ## draw ellipse per group
            vegan.ordiellipse(pca, display = "sites", kind = "se", scaling = scl, groups =  robjects.StrVector(grp), col = groupColDic[lev[i]], show_groups = lev[i])
        ## centroids
        scrs = base.as_data_frame(vegan.scores(pca, display = "sites", scaling = scl, choices = robjects.IntVector([1,2])))
        cent = base.do_call(base.rbind, base.lapply(base.split(scrs, robjects.StrVector(grp)), base.colMeans))  # split map scores to group
        centRowname = base.row_names(cent)
        centCols = [groupColDic[x] for x in centRowname]
        graphics.points(cent, col = robjects.StrVector(centCols), pch = 3, cex = 1.1)

    def OnHeatmap(self,event):
        number = self.notebook.GetCurrentDataId()
        heatmapDlg = DialogHeatmap(title=u"Input for heatmap")
        pars = heatmapDlg.GetValue()
        
        print(pars)
        
        matStart = pars[0]-1     
        data = self.notebook.data[number]
        numData = numpy.array(data)[1:,matStart: ].astype(float)
        
        # get numpy data column items
        items = numpy.array(data)[0,matStart: ].astype(str)          
                   
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        base = importr("base")
        from rpy2.robjects import numpy2ri        
        numpy2ri.activate()   # transfer the numpy array to matrix in R 
        
        # transfer numpy data to r matrix
        numDataR = transposeNumpyMat2R(numData)             
        numDataR.rownames = robjects.StrVector(items) # the numData column now is the row names of R matrix, heatmap3 use this format        
        
        # get column side annotation colors
        # get color list for legend
        annoCols = [ x-1 for x in pars[1]]         
        #annoColDicList =[]
        for n, annoCol in enumerate(annoCols):            
            anno = numpy.array(data)[1:, int(annoCol)]
            annoColDic = getCategoryColorDic (list(set(anno)), colsDic)
            cols = getMemberColor(anno, annoColDic)
            if (n==0):
                annoColor1 = robjects.StrVector(cols)  
                annoColDicList =  [annoColDic]    
                ColSideColors = base.cbind(annoColor1) # should use matrix in R instead of dataframe         
            if (n==1):
                annoColor2 = robjects.StrVector(cols)
                ColSideColors = base.cbind(annoColor1 , annoColor2)
                annoColDicList = annoColDicList + [annoColDic]
            if (n>=2):
                annoColorX = robjects.StrVector(cols)              
                ColSideColors = base.cbind(ColSideColors , annoColorX)
                annoColDicList = [annoColDicList, annoColDic]  # for legend
        print base.dim(ColSideColors)
        annoName = robjects.StrVector(numpy.array(data)[0, annoCols])
        ColSideColors.colnames = annoName

        outputDlg = OutputDialog()
        outPath, fileName = outputDlg.GetPath()
        print outPath        
        fileName = fileName + ".pdf"        
       
        heatmap3py(numDataR, ColSideColors, annoColDicList, fileName=fileName, outPath=outPath)
        heatmap3py(numDataR, ColSideColors, annoColDicList)
        
        
    def OnFDR_ttest(self, event):
        # get the active dataset
        number = self.notebook.GetCurrentDataId()
        fdrDlg = DialogFDR(title=u"Input for FDR analysis")
        pars = fdrDlg.GetValue()
        method = pars[3]

        data = self.notebook.data[number]

        y = pars[1]
        independentVars = numpy.delete(range(len(data[0])), [pars[1]]+pars[2])   
  
        numData = numpy.array(data[1:]).astype(float)      
        res = multi_ttest(numData, independentVars, y, method)
        res = getFDR_BH(res, data[0])

        output = OutFrame("notebook", res, "FDR")   
        output.Show()

    def OnFDR_Cox(self, event):
        # get the active dataset
        number = self.notebook.GetCurrentDataId()
        fdrDlg = DialogCox(title=u"Input for FDR of cox survival analysis")
        pars = fdrDlg.GetValue()

        data = self.notebook.data[number]
        survTime = pars[0]
        censor = pars[1]
        factors = range(pars[2], len(data[0]))

        res = numpy.zeros(shape=(len(factors), 3))
        for i in range(len(factors)):
            vars = [survTime, censor, factors[i]]
            # print data[0][factors[i]]
            summary = coxphPy(data, vars)
            pvalue = summary.rx2("logtest")[2]
            # print pvalue
            res[i, 0] = factors[i]
            res[i, 1] = pvalue      
                  
        res = getFDR_BH(res, data[0])
        output = OutFrame("notebook", res, "FDR")   
        output.Show()        
                
    def OnLayout(self, event):
        pass


if __name__ == '__main__':
    app = wx.App()

    frame = MainFrame()
    frame.Show()

    app.MainLoop()
