import wx
from iBAStable import *

class Notebook(wx.Notebook):
    """
    Notebook class
    """
    def __init__(self, parent, data):  # data type is pandas dataframe
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        self.tabDataIdDic = {}
        self.data = []

    def OnPageChanged(self, event):
        self.currentTabId = event.EventObject.GetChildren()[event.Selection].Id
        print "the updated tab Id of notebook is"
        print self.currentTabId
        event.Skip()

    def GetListTabId(self):
        return self.listTabId

    def GetCurrentTabId(self):
        return self.currentTabId
    
    def GetCurrentDataId(self):
        currentDataId = self.tabDataIdDic[self.currentTabId]
        return currentDataId

    def UpdateNotebook(self, data, number):
        if data != []:
            if number == []:
                # generate the tab based on the number of data

                self.listTabPanel = [Table(self, data[n]) for n in range(len(data))]
                listTabId = [self.listTabPanel[n].Id for n in range(len(data))]
                currentDataNum = len(self.data)
                for i in range(len(data)):
                    self.tabDataIdDic [listTabId[i]] = i + currentDataNum
                # print self.listTabPanel[0].GetColLabelValue(2)
                # print self.listTabPanel[0].Table.colLabels[2]   try to show whether the colname is set as we wanted
                # set the page Id to the first tab of notebook             
                self.currentTabId = self.listTabPanel[0].Id
                self.data = self.data + data  
                print "the Ids of the notebook are"
                print self.tabDataIdDic

                self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged) # This bind the event to function, Changed for the tab after change, Changing for the tab before the change

                [self.AddPage(self.listTabPanel[n], "data" + str(n+currentDataNum+1), select=True) for n in range(len(data))]
                # self.listTabPanel[0].SetColLabelValue(2, "first")   
                # self.listTabPanel[0].Refresh()
                self.listTabPanel[0].Update() 
                # print self.listTabPanel[0].GetColLabelValue(2)                

            if number != []:  # update current data
                self.listTabPanel[number].UpdateTable(data)