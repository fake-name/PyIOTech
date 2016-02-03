# To change this template, choose Tools | Templates
# and open the template in the editor.

import wx
import wx.lib.scrolledpanel


class SettingsWindow(wx.Frame):
	def __init__(self, parent, *args, **kwds):

		self.parent = parent
		
		
		kwds["title"] = "pyDAQ Settings"
		kwds["style"] = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP

		wx.Frame.__init__(self, parent, *args, **kwds)

		self.scrolledPanel = wx.lib.scrolledpanel.ScrolledPanel(self, style = wx.BORDER_SUNKEN)



		self.scrolledPanel.Bind(wx.EVT_SET_FOCUS, self.onFocus)
		self.Bind(wx.EVT_CLOSE, self.quitApp)

		self.scrolledPanel.SetFocus()



		
		self.scrolledSizer = wx.BoxSizer(wx.VERTICAL)




		text = "Ooga booga\n" * 100
		static_text=wx.StaticText(self.scrolledPanel, -1, text)

		self.scrolledSizer.Add(static_text, wx.EXPAND, 0)


		self.scrolledPanel.SetSizer(self.scrolledSizer)

		size = (600, 500)
		self.SetSize(size)
		self.SetMinSize(size)

		
		self.scrolledPanel.SetInitialSize(size)
		#self.mainWindowSizer.SetSizeHints(self.scrolledPanel.GetParent())
		self.scrolledPanel.SetupScrolling()



		self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE))


		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		headerStaticText = wx.StaticText(self, -1, "IOTech Channel Configuration")

		self.mainSizer.Add(headerStaticText, 0, wx.EXPAND|wx.ALL, 5)

		self.mainSizer.Add(self.scrolledPanel, 1, wx.EXPAND, 0)


		self.mainSizer.Add(self.__footerSizer(), 0, wx.EXPAND|wx.ALL, 5)


		self.SetSizerAndFit(self.mainSizer)

		self.Layout()

	def __footerSizer(self):
		footerSizer = wx.BoxSizer(wx.HORIZONTAL)

		footerButtonOK		=  wx.Button(self, -1, "Ok")
		footerButtonAddChannel	=  wx.Button(self, -1, "Add Channel")
		footerSizer.Add(footerButtonOK)

		footerSizer.Add((10,10), 1, wx.EXPAND)

		footerSizer.Add(footerButtonAddChannel)

		return footerSizer
	
	def addItem(self, item):
		#Magic
		self.scrolledSizer.FitInside()

	def onFocus(self, event):
		self.scrolledPanel.SetFocus()




	def quitApp(self,event):
		self.Destroy()
		self.parent.Enable()

def start(parent):
	
	parent.Disable()
	
	my_frame = SettingsWindow(parent)
	my_frame.Show()
	
	parent.Enable()



class EmptyParent:

	
	def Disable(self):
		pass
	def Enable(self):
		pass

	def hasattr(self, key):
		return key == "empty"


class MyApp(wx.App):

	def OnInit(self):
		wx.InitAllImageHandlers()
		TemperatureFrame = SettingsWindow(None, -1)
		self.SetTopWindow(TemperatureFrame)
		TemperatureFrame.Show()
		return 1


if __name__ == "__main__":

	mainWin = MyApp(0)
	mainWin.MainLoop()
