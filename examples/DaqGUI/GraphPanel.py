


import wx

import numpy as np
import queVars


import random
import wx




class GraphPanel(wx.Panel):

		#Number of items in the color map LUT
		#I'm pretty sure the actual cm library only uses 256, so settings above 256 have no benefit

	def __init__(self, *args, **kwds):
		#kwds["style"] = wx.RESIZE_BORDER|wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN
		self.channel = kwds.pop('dataChannel')
		self.IOTechConfig = kwds.pop('configItem')
		wx.Panel.__init__(self, *args, **kwds)
		#print self
		#wx.Panel.__init__( self, parent, **kwargs )

		#print "Test"
		#super(GridPanel, self).__init__(None, -1, 'CursorTracker')	# Call inheritor's __init__




		self.mdc = None 		# memory dc to draw off-screen

		self.Bind(wx.EVT_SIZE, self.onSize)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.onErase)
		self.Bind(wx.EVT_PAINT, self.onPaint)

		#print "Size", self.rectDims
		#Blue text on a black->red->orange->yellow->white background


		self.colourBlack	= wx.Colour(0, 0, 0)
		self.colourWhite	= wx.Colour(255, 255, 255)

		self.penBlack		= wx.Pen(self.colourBlack)
		self.penWhite		= wx.Pen(self.colourWhite)

		self.brushBlack = wx.Brush(self.colourBlack)
		self.brushWhite = wx.Brush(self.colourWhite)


		self.onSize(None)
		#self.onTimer()

		self.redraw_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
		self.redraw_timer.Start(1000 / 30)

	def onSize(self, event):
		# re-create memory dc to fill window
		w, h = self.GetClientSize()
		self.mdc = wx.MemoryDC(wx.EmptyBitmap(w, h))
		self.redraw()

	def onErase(self, event):
		pass 		# don't do any erasing to avoid flicker

	def onPaint(self, event):
		# just blit the memory dc
		dc = wx.PaintDC(self)
		if not self.mdc:
			return
		w, h = self.mdc.GetSize()
		dc.Blit(0, 0, w, h, self.mdc, 0, 0)

	def redraw(self):
		# do the actual drawing on the memory dc here
		dc = self.mdc

		self.data = self.IOTechConfig.circularBuffer.getAsArray()

		w, h = dc.GetSize()
		dc.Clear()
		dc.SetPen(self.penBlack)


		dc.SetBrush(self.brushBlack)
		dc.DrawRectangle(0, 0, w, h)

		dc.SetTextForeground(self.colourWhite)
		#print arr
		#print self.rectDims

		if self.data.shape != (0,):
			#print "Meh",  self.data[...,self.channel].shape
			#print self.data.shape
			dataLen = self.data[..., self.channel].shape[0]

			dataMin = self.data[..., self.channel].min() - 1
			dataMax = self.data[..., self.channel].max() + 1

			dataHeight = float(dataMax - dataMin)

			scaleFactor = (h - 2) / dataHeight
			#print scaleFactor, dataMin, dataMax, dataHeight

			dataX = np.linspace(1, w - 1, num=dataLen)

			dataY = ((self.data[..., self.channel].astype(np.float) - dataMin) * scaleFactor) + 1

			pointList = []

			for offset in xrange(dataLen):
				tX = dataX[offset]
				tY = dataY[offset]

				pointList.append((tX, tY))

			dc.DrawPointList(pointList, self.penWhite)


			dc.DrawText("Max: %0.5fV" % self.intToVolts(dataMax), 10, 5)
			dc.DrawText("Min: %0.5fV" % self.intToVolts(dataMin), 10, h - 20)


		self.Refresh()

	def intToVolts(self, intVal):
		val = float(intVal - 2 ** 15)
		val = (val / (2 ** 15)) * 10
		return val

	def draw_plot(self):
		""" Redraws the plot
		"""
		# when xmin is on auto, it "follows" xmax to produce a
		# sliding window effect. therefore, xmin is assigned after
		# xmax.
		#

		# for ymin and ymax, find the minimal and maximal values
		# in the data set and add a mininal margin.
		#
		# note that it's easy to change this scheme to the
		# minimal/maximal value in the current display, and not
		# the whole data set.
		#
		self.redraw()



	def on_redraw_timer(self, event):
		# if paused do not add data, but still redraw the plot
		# (to respond to scale modifications, grid change, etc.)

		#print "Bwuh?", self.channel, self.data.shape, self.data[...,self.channel], np.arange(self.data.shape[0])
		self.draw_plot()

	def on_exit(self, event):
		print "trying to die"
		self.Destroy()


