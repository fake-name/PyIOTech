# Simple ring buffer implementation using deque
# written by vegaseat, originally acquired from:
# http://www.daniweb.com/forums/post202523-3.html
#
# I have no idea what licensing terms this would be distributed under,
# though I figure they're fairly liberal since the code was posted
# on a public forum.

import numpy as np

from collections import deque

class RingBuffer(deque):
	"""
	inherits deque, pops the oldest data to make room
	for the newest data when size is reached
	"""
	def __init__(self, size):
		deque.__init__(self)
		self.size = size

	def full_append(self, item):
		deque.append(self, item)
		# full, pop the oldest item, left most item
		self.popleft()

	def append(self, item):
		# max size reached, append becomes full_append
		if len(self) == self.size:

			self.popleft()
			deque.append(self, item)
		
	def get(self):
		"""returns a list of size items (newest items)"""
		return list(self)

	def getAsArray(self):
		firstRun = True
		for item in list(self):
			if firstRun:
				firstRun = False
				outData = item
			else:
				outData = np.append(outData, item, axis=0)

		if not firstRun:
			return outData
		else:
			return np.zeros((1))