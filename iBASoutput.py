import wx
from iBASnotebook import Notebook
from iBAStable import *

# show result in a table
class OutFrame(wx.Frame):
    def __init__(self, type, result, notebookTitle):
        wx.Frame.__init__(self, None, -1, title= "Analysis Result" ,size=(800, 600))

        ico = wx.Icon('egypt200.png', wx.BITMAP_TYPE_ANY)
        self.SetIcon(ico)
        
        # set menuFile and menuBar
        menuFile = wx.Menu()
        menuFile.Append(1, "&Save")
        menuFile.AppendSeparator()
        menuFile.Append(2, "E&xit")
        
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        self.SetMenuBar(menuBar)
        # make sizers of windows
        self.sizerMainFrame = wx.BoxSizer(wx.VERTICAL)
        
        if type == "notebook":        
            self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )     
            self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
            bSizer4 = wx.BoxSizer( wx.VERTICAL )
            
            self.m_grid4 = wx.grid.Grid( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
            
            # Grid
            self.m_grid4.CreateGrid( 5, 5 )
            self.m_grid4.EnableEditing( True )
            self.m_grid4.EnableGridLines( True )
            self.m_grid4.EnableDragGridSize( False )
            self.m_grid4.SetMargins( 0, 0 )
            
            # Columns
            self.m_grid4.EnableDragColMove( False )
            self.m_grid4.EnableDragColSize( True )
            self.m_grid4.SetColLabelSize( 30 )
            self.m_grid4.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
            
            # Rows
            self.m_grid4.EnableDragRowSize( True )
            self.m_grid4.SetRowLabelSize( 80 )
            self.m_grid4.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )       
            
            
            # Label Appearance
            
            # Cell Defaults
            self.m_grid4.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
            
            if result != None:
                table = TableBase(result)       
                self.m_grid4.SetTable(table, True)
            
            bSizer4.Add( self.m_grid4, 0, wx.ALL, 5 )
            
            
            self.m_panel1.SetSizer( bSizer4 )
            self.m_panel1.Layout()
            bSizer4.Fit( self.m_panel1 )
            self.m_notebook1.AddPage( self.m_panel1, notebookTitle, False )                               
               
            self.sizerMainFrame.Add(self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( self.sizerMainFrame )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
