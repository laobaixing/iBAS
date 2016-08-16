import wx
import os
import wx.lib.filebrowsebutton as filebrowse
from iFun import str2num

class InputDataDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, title="Import files", size=(450, 250))

        
        self.dataFilesQuantityMax = 4  # the max quantity of "Add File" buttons, should be put in the dialogue class
        self.inputFilesQuantityShowed = 1
        self.startDirectory = os.getcwd()

        # make sizers
        sizerMainFrame = wx.BoxSizer(wx.VERTICAL)
        self.listFlBrwssizerBtns = wx.BoxSizer(wx.VERTICAL)
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)

        #  make buttons
        self.listFlBrwsBtn = [filebrowse.FileBrowseButton(self, id=wx.NewId(), labelText="data" + str(flBrwsBtn+1), initialValue="", size=(400, -1), buttonText="Browse...", startDirectory=self.startDirectory) for flBrwsBtn in range(self.dataFilesQuantityMax)]
        btnAddFile = wx.Button(self, wx.NewId(), label="&Add file")
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")

        self.Bind(wx.EVT_BUTTON, self.OnAddFile, btnAddFile)

        #  set sizers of list file browse buttons
        self.listFlBrwssizerBtns.Add(wx.Size(1, 20))

        for flBrwsBtn in range(self.dataFilesQuantityMax):
            self.listFlBrwssizerBtns.Add(self.listFlBrwsBtn[flBrwsBtn], flag=wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, border=5)
            if flBrwsBtn > 0:
                self.listFlBrwsBtn[flBrwsBtn].Hide()

        #  set sizers of Open and Cancel buttons
        sizerBtns.Add(wx.Size(1, 20))
        sizerBtns.Add(btnAddFile, flag=wx.ALL, border=5)
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)

        #  set sizerMainFrame
        sizerMainFrame.Add(self.listFlBrwssizerBtns)
        sizerMainFrame.Add(sizerBtns)

        self.SetSizer(sizerMainFrame)
        self.Fit()
        self.Layout()

        if self.ShowModal() == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()

    def OnAddFile(self, event):
        # inputFilesQuantityShowed start from 1
        currentPath = self.listFlBrwsBtn[self.inputFilesQuantityShowed-1].GetValue()
        # print(currentPath)
        self.listFlBrwsBtn[self.inputFilesQuantityShowed].startDirectory = os.path.dirname(currentPath)
        self.inputFilesQuantityShowed += 1

        for flBrwsBtn in range(self.inputFilesQuantityShowed):
            self.listFlBrwsBtn[flBrwsBtn].Show()

        self.Fit()
        self.Layout()

    def GetPath(self):   # Get Path is called in iBAS
        if self.status:
            return [self.listFlBrwsBtn[FlBrwsBtn].GetValue() for FlBrwsBtn in range(self.dataFilesQuantityMax)]
        else:
            return []

    def GetInputFilesQuantityShowed(self):
        if self.status:
            return self.inputFilesQuantityShowed
        else:
            return 1

#######################################################################################
## Class: input one row or column numbers for several methods such as histogram
#######################################################################################

class InputXDialog ( wx.Dialog ):
    
    def __init__( self, title ):
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input the parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )
           
        self.m_staticText_SkipRow = wx.StaticText( self, wx.ID_ANY, u"The number of headers skipped", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_SkipRow.Wrap( -1 )
        gSizer3.Add( self.m_staticText_SkipRow, 0, wx.ALL, 5 )
        
        self.m_textCtrl_SkipRow = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_SkipRow, 0, wx.ALL, 5 )
        self.m_textCtrl_SkipRow.SetValue(u"1")
        
        self.m_staticText_SkipCol = wx.StaticText( self, wx.ID_ANY, u"The number of Columns skipped", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_SkipCol.Wrap( -1 )
        gSizer3.Add( self.m_staticText_SkipCol, 0, wx.ALL, 5 )
        
        self.m_textCtrl_SkipCol = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_SkipCol, 0, wx.ALL, 5 )
        self.m_textCtrl_SkipCol.SetValue(u"2") 
               
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
        
    def GetValue(self):
        if self.status:
            val_skipCol = int(self.m_textCtrl_SkipCol.GetValue()) 
            val_skipRow= int(self.m_textCtrl_SkipRow.GetValue())   # return the format as python
            return (val_skipCol, val_skipRow)  
        else:
            return []
    
    def __del__( self ):
        pass
    


#######################################################################################
## Class: input two row or column numbers for several methods such as scatter plot
#######################################################################################

class InputXYDialog ( wx.Dialog ):
    
    def __init__( self, title ):
        # wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Input for Scatter Plot", pos = wx.DefaultPosition, size = wx.Size(606,375 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input row/column and the number", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )
        
        self.m_staticText_Direction = wx.StaticText( self, wx.ID_ANY, u"By Row or Column", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_Direction.Wrap( -1 )
        gSizer3.Add( self.m_staticText_Direction, 0, wx.ALL, 5 )
        
        m_choiceDirection = [ u"Col", u"Row" ]
        self.m_choice_Direction = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceDirection, 0 )
        self.m_choice_Direction.SetSelection( 0 )
        gSizer3.Add( self.m_choice_Direction, 0, wx.ALL, 5 )
        
        self.m_staticText_Skip = wx.StaticText( self, wx.ID_ANY, u"The number of headers/columns skipped", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_Skip.Wrap( -1 )
        gSizer3.Add( self.m_staticText_Skip, 0, wx.ALL, 5 )
        
        self.m_textCtrl_Skip = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_Skip, 0, wx.ALL, 5 )
        self.m_textCtrl_Skip.SetValue(u"1")
        
        self.m_staticText_X = wx.StaticText( self, wx.ID_ANY, u"Number 1", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_X.Wrap( -1 )
        gSizer3.Add( self.m_staticText_X, 0, wx.ALL, 5 )
        
        self.m_textCtrl_X = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_X, 0, wx.ALL, 5 )
        
        self.m_staticText_Y = wx.StaticText( self, wx.ID_ANY, u"Number 2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_Y.Wrap( -1 )
        gSizer3.Add( self.m_staticText_Y, 0, wx.ALL, 5 )
        
        self.m_textCtrl_Y = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_Y, 0, wx.ALL, 5 )           
        
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
        
    def GetValue(self):
        if self.status:
            direction = str(self.m_choice_Direction.GetStringSelection())
            val_skip = int(self.m_textCtrl_X.GetValue()) 
            val1= int(self.m_textCtrl_X.GetValue())-1   # return the format as python
            val2= int(self.m_textCtrl_Y.GetValue())-1
            return (direction, val1, val2, val_skip)  
        else:
            return []
    
    def __del__( self ):
        pass
    

#######################################################################################
## Class for FDR
#######################################################################################

class DialogFDR ( wx.Dialog ):
    
    def __init__( self, title, methods):
        # wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Input for Scatter Plot", pos = wx.DefaultPosition, size = wx.Size(606,375 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input row/column and the number", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )  # list control in two columns
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"By Row or Column", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        gSizer3.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        m_choice1Choices = [ u"Col", u"Row" ]
        self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( 0 )
        gSizer3.Add( self.m_choice1, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Name or Number of dependent variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        self.m_textCtrl6 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl6, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Name or Number of excluded independent variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        gSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_textCtrl7 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl7, 0, wx.ALL, 5 )     
        
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Method", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        gSizer3.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        m_choice2Choices = methods
        self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
        self.m_choice2.SetSelection( 0 )
        gSizer3.Add( self.m_choice2, 0, wx.ALL, 5 )      
        
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
        
    def GetValue(self):
        if self.status:
            direction = str(self.m_choice1.GetStringSelection())
            val1= int(self.m_textCtrl6.GetValue())-1
            valstr2= self.m_textCtrl7.GetValue() 
            val2 = str2num(valstr2)  # return a list
            val2 = [x-1 for x in val2]
            method = str(self.m_choice2.GetStringSelection())
            return (direction, val1, val2, method)  
        else:
            return []
    
    def __del__( self ):
        pass

    
#######################################################################################
## Class: input column number for the factors of survival analysis: 
## including survival time, censor and independent variables
#######################################################################################

class InputSurvDialog ( wx.Dialog ):
    
    def __init__( self, title ):
        # wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Input for Scatter Plot", pos = wx.DefaultPosition, size = wx.Size(606,375 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input column number of variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )        
       
        self.m_staticText_time = wx.StaticText( self, wx.ID_ANY, u"Column number for survival time", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_time.Wrap( -1 )
        gSizer3.Add( self.m_staticText_time, 0, wx.ALL, 5 )
        
        self.m_textCtrl_time = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_time, 0, wx.ALL, 5 )
        
        self.m_staticText_censor = wx.StaticText( self, wx.ID_ANY, u"Column number for censor", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_censor.Wrap( -1 )
        gSizer3.Add( self.m_staticText_censor, 0, wx.ALL, 5 )
        
        self.m_textCtrl_censor = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_censor, 0, wx.ALL, 5 )  
        
        # the content of variables should be flexible
        self.m_staticText_factor = wx.StaticText( self, wx.ID_ANY, u"Column number for independent variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_factor.Wrap( -1 )
        gSizer3.Add( self.m_staticText_factor, 0, wx.ALL, 5 )
        
        self.m_textCtrl_factor = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_factor, 0, wx.ALL, 5 )                   
        
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
        
    def GetValue(self):
        if self.status:
            val1= int(self.m_textCtrl_time.GetValue())-1
            val2= int(self.m_textCtrl_censor.GetValue())-1
            val3= int(self.m_textCtrl_factor.GetValue())-1
            return ([val1, val2, val3])  
        else:
            return []
    
    def __del__( self ):
        pass

#######################################################################################
## Class for FDR for Cox survival analysis
#######################################################################################

class DialogCox ( wx.Dialog ):
    
    def __init__( self, title ):
        # wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Input for Scatter Plot", pos = wx.DefaultPosition, size = wx.Size(606,375 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input column number of variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )  # list control in two columns        
     
        self.m_staticText_time = wx.StaticText( self, wx.ID_ANY, u"Column number for survival time", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_time.Wrap( -1 )
        gSizer3.Add( self.m_staticText_time, 0, wx.ALL, 5 )
        
        self.m_textCtrl_time = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_time, 0, wx.ALL, 5 )
        
        self.m_staticText_censor = wx.StaticText( self, wx.ID_ANY, u"Column number for censor", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_censor.Wrap( -1 )
        gSizer3.Add( self.m_staticText_censor, 0, wx.ALL, 5 )
        
        self.m_textCtrl_censor = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_censor, 0, wx.ALL, 5 )  
        
        self.m_staticText_factorStart = wx.StaticText( self, wx.ID_ANY, u"Number of start column of independent variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_factorStart.Wrap( -1 )
        gSizer3.Add( self.m_staticText_factorStart, 0, wx.ALL, 5 )
        
        self.m_textCtrl_factorStart = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_factorStart, 0, wx.ALL, 5 )          
      
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
        
    def GetValue(self):
        if self.status:
            val1= int(self.m_textCtrl_time.GetValue())-1
            val2= int(self.m_textCtrl_censor.GetValue())-1
            val3= int(self.m_textCtrl_factorStart.GetValue())-1
            return ([val1, val2, val3])  
        else:
            return []
    
    def __del__( self ):
        pass

#######################################################################################
## Dialog class for heatmap
#######################################################################################

class DialogHeatmap ( wx.Dialog ):
    
    def __init__( self, title ):
        # wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Input for Scatter Plot", pos = wx.DefaultPosition, size = wx.Size(606,375 ), style = wx.DEFAULT_DIALOG_STYLE )
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input for heatmap", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )  # list control in two columns
              
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Data for heatmap start from column", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        self.m_textCtrl6 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl6, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Column number of annotation variables", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        gSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_textCtrl7 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl7, 0, wx.ALL, 5 )     
        
#         self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Method", wx.DefaultPosition, wx.DefaultSize, 0 )
#         self.m_staticText5.Wrap( -1 )
#         gSizer3.Add( self.m_staticText5, 0, wx.ALL, 5 )
#         
#         m_choice2Choices = [ u"ward.D", u"Spearman" ]
#         self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
#         self.m_choice2.SetSelection( 0 )
#         gSizer3.Add( self.m_choice2, 0, wx.ALL, 5 )      
        
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()               
    
    def GetValue(self):
        if self.status:
            # direction = str(self.m_choice1.GetStringSelection())
            val1= int(self.m_textCtrl6.GetValue())
            valstr2 = self.m_textCtrl7.GetValue()
            valnum2 = str2num(valstr2)
            #  method = str(self.m_choice2.GetStringSelection())
            return (val1, valnum2)  
        else:
            return []
                    
    def __del__( self ):
        pass

#######################################################################################
## Class for getting output path
#######################################################################################
    
class OutputDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, title="Output results", size=(450, 250))
    
        self.startDirectory = os.getcwd()

        # make sizers
        sizerMainFrame = wx.BoxSizer(wx.VERTICAL)
        self.FlBrwsBtnsSizer = wx.BoxSizer(wx.VERTICAL)
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)

        #  make buttons
        self.FlBrwsBtn = filebrowse.DirBrowseButton(self, id=wx.NewId(), labelText="Output path", size=(400, -1), buttonText="Browse...", startDirectory=self.startDirectory) 
        btnOK = wx.Button(self, wx.ID_OK, label="&OK")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        
        self.FlBrwsBtnsSizer.Add(wx.Size(1, 20))
        self.FlBrwsBtnsSizer.Add(self.FlBrwsBtn, flag=wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, border=5)

        gSizerFilename = wx.GridSizer( 0, 2, 0, 0 )        
       
        self.m_staticText_filename = wx.StaticText( self, wx.ID_ANY, u"File Name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_filename.Wrap( -1 )
        gSizerFilename.Add( self.m_staticText_filename, 0, wx.ALL, 5 )
        
        self.m_textCtrl_filename = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizerFilename.Add( self.m_textCtrl_filename, 0, wx.ALL, 5 )

        #  set sizers of OK and Cancel buttons
        sizerBtns.Add(wx.Size(1, 20))
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOK, flag=wx.ALL, border=5)

        #  set sizerMainFrame
        sizerMainFrame.Add(self.FlBrwsBtnsSizer)
        sizerMainFrame.Add(gSizerFilename)
        sizerMainFrame.Add(sizerBtns)

        self.SetSizer(sizerMainFrame)
        self.Fit()
        self.Layout()

        if self.ShowModal() == wx.ID_OK:
            print "OK"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.status = False
            self.Destroy()

    def GetPath(self):
        if self.status:
            path = self.FlBrwsBtn.GetValue() 
            filename = self.m_textCtrl_filename.GetValue()
            return path, filename
        else:
            return None

#######################################################################################
## Class for PCA analysis
#######################################################################################

class DialogPCA ( wx.Dialog ):
    
    def __init__( self, title ):
        wx.Dialog.__init__(self, None, -1, title= title, size=(450, 250))
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Please input for principle component analysis", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        gSizer3 = wx.GridSizer( 0, 2, 0, 0 )  # list control in two columns
              
        self.m_staticText_start = wx.StaticText( self, wx.ID_ANY, u"Numerical Data for PCA start from column", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_start.Wrap( -1 )
        gSizer3.Add( self.m_staticText_start, 0, wx.ALL, 5 )
        
        self.m_textCtrl_start = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_start, 0, wx.ALL, 5 )
        
        self.m_staticText_group = wx.StaticText( self, wx.ID_ANY, u"Column number of group", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_group.Wrap( -1 )
        gSizer3.Add( self.m_staticText_group, 0, wx.ALL, 5 )
        
        self.m_textCtrl_group = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_textCtrl_group, 0, wx.ALL, 5 )     
              
        bSizer1.Add( gSizer3, 1, wx.EXPAND, 5 )
        
        sizerBtns = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(self, wx.ID_OK, label="&Open")
        btnCancel = wx.Button(self, wx.ID_CANCEL, label="&Cancel")
        sizerBtns.Add(btnCancel, flag=wx.ALL, border=5)
        sizerBtns.Add(btnOpen, flag=wx.ALL, border=5)
        bSizer1.Add(sizerBtns)#  , 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        
        result = self.ShowModal()   # Show the dialog and wait for the input
        if result == wx.ID_OK:
            print "Open"
            self.status = True
            self.Destroy()
        else:
            print "Cancel"
            self.Destroy()        
             
    def GetValue(self):
        if self.status:
            # direction = str(self.m_choice1.GetStringSelection())
            val1= int(self.m_textCtrl_start.GetValue())-1
            val2 = int(self.m_textCtrl_group.GetValue())-1
            return (val1, val2)  
        else:
            return []
                    
    def __del__( self ):
        pass 
