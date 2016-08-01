import wx
import numpy
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
from iBASdialog import OutputDialog

class FigurePanel(wx.Panel):
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)

        # make sizers of panel
        self.sizerMainFrame = wx.BoxSizer(wx.VERTICAL)

        # make figure
        self.figure = Figure()

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()

        # self.UpdateFigurePanel(data)

        # make save button on the top of the panel
        self.sizerBtn = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerMainFrame.Add(self.sizerBtn)

        btn1 = wx.Button(self, wx.ID_ANY, label="&Save")

        self.sizerBtn.Add(btn1, proportion=0, flag=wx.ALL | wx.ALIGN_LEFT, border=5)

        self.Bind(wx.EVT_BUTTON, self.OnSave, btn1)

        # make panel with btn and figure
        self.sizerMainFrame.Add(self.canvas, 1, wx.EXPAND)

        # update sizers
        self.SetSizer(self.sizerMainFrame)
        self.Layout()

    def Hist(self, data, pars):

        if data != []:
            self.data = numpy.array(data)  # Define the data in the class, can use in the future. 

            ax = self.figure.add_subplot(111)
            ax.hold(False)
            # ax.plot(self.data[1:, 0], self.data[1:, 1], '*-')
            ax.hist(self.data[pars[1]:, pars[0]:].astype(float).reshape(-1), color = 'green', normed=1, histtype="bar",  alpha=0.8)
            self.canvas.draw()
    
    def Scatplot(self, data, pair):
        if data != []:
            self.data = numpy.array(data)

            ax = self.figure.add_subplot(111)
            ax.clear()
            # ax.plot(self.data[1:, 0], self.data[1:, 1], '*-')
            if (pair[0] == "col"):
                ax.scatter(self.data[pair[3]:, pair[1]].astype(float),self.data[pair[3]:, pair[2]].astype(float) )
            else:
                ax.scatter(self.data[pair[1], pair[3]:].astype(float),self.data[pair[2],pair[3]: ].astype(float) )
            self.canvas.draw()        

    def SaveFigure(self, name):
        self.canvas.print_bmp(filename=name+'.bmp')

    def OnSave(self, event):
        outputDlg = OutputDialog()
        outPath, fileName = outputDlg.GetPath()
        print outPath 
        fileName = outPath + "/" + fileName + ".bmp"       
        self.canvas.print_bmp(fileName)

