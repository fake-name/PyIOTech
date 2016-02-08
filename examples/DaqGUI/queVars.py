#!C:/Python26


import numpy as np
import Queue
import time


class Box:				# Box class permits passing by reference. Any function passed queVars.tempsAbs will always be able to reference the most recent version of the boxed matrix by calling Box.unbox()
	def __init__(self, item):
		self.item = item

	def update(self, item):
		self.item = item

	def unbox(self):

		return self.item


class RingBuffer(list):
	"""
	inherits deque, pops the oldest data to make room
	for the newest data when size is reached
	"""
	def __init__(self, size):
		list.__init__(self)
		self.size = size

	def append(self, item):
		if len(self) >= self.size:
			self.pop(0)

		list.append(self, item)

	def get(self):
		"""returns a list of size items (newest items)"""
		return list(self)

	def getAsArray(self):
		arr = np.asarray(self)
		return arr

class ConfigObj:

	serThread	=	None

	openOnStart	=	False

	noRedir		=	False

	Shutdown	=	False


	logEn		=	False
	logName		=	"IIC Temp Log %s, %s.txt" % (time.time(), time.strftime("%Y-%m-%d %H;%M;%S;", time.gmtime()))

	visualization	=	True

	scaled = True

	Qin		=	Queue.Queue()
	Qout		=	Queue.Queue()

	arSz = (1, 1)

	def __init__(self):

		self.regenArayVars((14, 8))


	def regenArayVars(self, arSz):


		self.tmpRawAr = Box(None)		# delta temp array scaled to 0-1 for display





cnf	=	ConfigObj()
