
from PyIOTech import daq
from PyIOTech import daqh
import time
#import sys
import csv
import threading
import numpy as np
#import ringBuffer

import Queue

#print daq.GetDeviceList()



class IOTechConfiguration:


	def __init__(self):

		self.gains = [daqh.DgainX1, daqh.DgainX1]#, daqh.DgainX2, daqh.DgainX2,
				#daqh.DgainX1]#, daqh.DgainX2]#, daqh.DgainX1, daqh.DgainX1]

		self.flags = \
			   [daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential,
				daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential]#,
				#daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential,
				#daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential,
				#daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential]#,
				#daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential]#,
				#daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential,
				#daqh.DafBipolar | daqh.DafSettle1us | daqh.DafDifferential]
				#daqh.DafBipolar|daqh.DafSettle10us,
				#daqh.DafBipolar|daqh.DafSettle10us,
				#daqh.DafBipolar|daqh.DafSettle1us,
				#daqh.DafBipolar|daqh.DafSettle1us,
				#daqh.DafBipolar|daqh.DafSettle1us]

		self.channels = [0, 1]#, 2, 3, 4]#, 5]#, 6, 7]

		disableOversampling = True

		self.clockSource = daqh.DacsAdcClock

		self.transMask = daqh.DatmDriverBuf | daqh.DatmUpdateBlock | daqh.DatmCycleOn


		self.buf = False

		self.triggerEv = daqh.DatsImmediate

		self.rateMode = daqh.DarmFrequency

		self.rateState = daqh.DaasPostTrig

		self.sampleRate = 10000		# 10 Khz datarate

		self.binRatio = 0
		self.dataRate = (self.sampleRate * len(self.channels)) * (self.binRatio + 1)
		while self.dataRate <= 10**6:
			self.binRatio += 1
			self.dataRate = (self.sampleRate * len(self.channels)) * (self.binRatio + 1) # look ahead to the next result, and if it
											# exceeds the possible data rate, break now.

		if disableOversampling:
			self.binRatio = 1

		self.dataRate = (self.sampleRate * len(self.channels)) * (self.binRatio)
		# dataRate is the effective aggretate sample-rate.
		# Basically, it's the frequency the DAQ ADC will actually have to run at.

		print "Datarate, binratio - ", self.dataRate, self.binRatio
		print "Functional sample rate per-channel - ", self.dataRate * self.binRatio

		self.acqRate 	= int(self.dataRate / len(self.channels))
		# Since the IOTech wants the sample rate on a per-channel basis,
		# we divide the total sample rate by the number of channels we're acquiring on,
		# to get the sample rate that will get the IOTech as close as possible.




		self.setSampleFreq(self.acqRate)  # 20kHzs

		self.scans = 2**22
		self.dataPointsPerChunk = 2**16

		devL = daq.GetDeviceList()

		if devL:
			self.deviceNameStr = devL[0]
		else:
			self.deviceNameStr = None

		# PC Side buffering options

		self.logDataRam = False

		#self.circularBuffer = False

	def setSampleFreq(self, freq):

		aggFreq = freq * len(self.channels)  # 1000 Hertz
		if aggFreq > 1000000:

			print aggFreq
			print freq, len(self.channels)  # 1000 Hertz
			raise ValueError("Aggregate Scan Frequency cannot exceed 1 Mhz")

		else:
			self.freq = freq

	def listDevices(self):
		return daq.GetDeviceList()


class IOTechInterface:

	capRunning = False
	data = []

	def __init__(self, config = IOTechConfiguration()):
		self.iotech = None

		self.running = False

		self.config = config

		self._openDevice()
		self._configureDevice()


	def _openDevice(self):

		self.iotech = daq.daqDevice(self.config.deviceNameStr)


	def _configureDevice(self, ):
		if self.iotech:

	# Configure channels and gains
			self.iotech.AdcSetScan(self.config.channels, self.config.gains, self.config.flags)

	# Set Daq Acquisition mode
			self.iotech.AdcSetAcq(daqh.DaamInfinitePost)

	# Configure ADC Clocksource
			self.iotech.AdcSetClockSource(self.config.clockSource)

	# Configure Triggering
			#self.iotech.SetTriggerEvent(self.config.triggerEv, None, 0, 0, 0, 0, 0, 0, 0)
			self.iotech.AdcSetTrig(self.config.triggerEv, 0, 0, 0, 0)

	# Configure ADC Scanrate
			print "Channels:", self.config.channels

			actualScanRate = self.iotech.AdcSetRate(self.config.rateMode, self.config.rateState, self.config.freq)
			print "Requested ADC Rate = ", self.config.freq, "Set ADC scan rate:", actualScanRate


			return True

		else:
			raise ValueError, "No IO-Tech Found!"

	def startCapture(self, writeFile=False):

		print "Taking Data..."
		print "Configured ADC Freq", self.config.freq
		print "Actual ADC Freq", self.iotech.AdcGetFreq()
		self.writeToLogFile = writeFile

		self.capMonThread = threading.Thread(target = self.runCapture, name = "DAQ Readout Thread")
		self.capRunning = True
		self.capMonThread.start()

	def asyncFileWriter(self, inQueue, gainLUT):
		filename = time.strftime("Data/Datalog - %Y %m %d, %a, %H-%M-%S.csv", time.localtime())
		fp = open(filename, "w")

		headerStr = ""

		headerStr += "# Sample Rate: %i, Actual ADC Rate: %i\r\n" % (self.config.sampleRate, self.config.freq)
		headerStr += "# Bin-Down Ratio = %i\r\n" % (self.config.binRatio)
		for x in range(len(self.config.gains)):
			headerStr += "# Channel %i - Gain: %i \r\n" % (x, gainLUT[self.config.gains[x]])


		fp.write(headerStr)

		writer = csv.writer(fp)

		while self.capRunning or not inQueue.empty():

			#print inQueue.qsize()
			try:
				dat = inQueue.get_nowait()
				#fp.write("%s\r\n" % dat.tolist())
				writer.writerows(dat)
			except Queue.Empty :
				pass
			time.sleep(0.001)

		print "File Queue Exiting"
		fp.close()

	def runCapture(self):

		self.running = True
		self.fileWriterRunning = False

		# Configure Transfer Buffer
		self.iotech.AdcTransferSetBuffer(self.config.transMask, self.config.scans, self.config.buf)

		#begin data acquisition

		self.iotech.AdcArm()
		self.iotech.AdcTransferStart()

		arrShape = (self.config.dataPointsPerChunk, len(self.config.channels))


		#lookup table to make going from DGain*X to the actual gain easier.
		gainLUT       = [1, 			2, 				4, 				8]
		voltsBitLUT   = [10.0/(2**15), 	5.0/(2**15), 	2.0/(2**15), 	1.0/(2**15)]

		if self.writeToLogFile:
			self.fileWriterRunning = True

			fileQueue = Queue.Queue()
			fileWriterThread = threading.Thread(target = self.asyncFileWriter, name = "File Writer Thread", args = (fileQueue, gainLUT))
			fileWriterThread.start()


		bufMask = daqh.DabtmOldest | daqh.DabtmRetAvail


		print "Starting Loop"


		garbage = self.iotech.AdcTransferBufData(self.config.dataPointsPerChunk, bufMask)
		# Flush the transfer buffer
		# May not be needeed

		cumInputData = np.empty((0, len(self.config.channels)))

		print cumInputData, cumInputData.shape

		while self.capRunning:
			stat = self.iotech.AdcTransferGetStat()
			if stat["retCount"]:
				tempDat, retNum = self.iotech.AdcTransferBufData(self.config.dataPointsPerChunk, bufMask)
				tempDat = np.ctypeslib.as_array(tempDat).astype(np.float)

				if stat["retCount"] > (self.config.dataPointsPerChunk * 3):
					print "Cannot keep up with data-rate. Please try turning off the visualization."
					print stat, self.config.dataPointsPerChunk

				if stat["retCount"] > (self.config.dataPointsPerChunk * 10):
					print "Too much data in buffer. Please change aquisition settings, or turn off the visualization"
					raise ValueError
				#print "Array Shape", arrShape
				#print "tempDat", tempDat.shape, retNum

				tempDat = tempDat.reshape(arrShape)
				validDataCount = int(retNum.value)
				if validDataCount != 0:
					tempDat = tempDat[:validDataCount, ...]
					cumInputData = np.vstack((cumInputData, tempDat))
					#print "Data", validDataCount, cumInputData.shape

					arHeight = cumInputData.shape[0]

					chunks = arHeight / self.config.binRatio
					#print "Chunks", chunks, chunks * self.config.binRatio, arHeight - (chunks * self.config.binRatio)
					splitableSection 	= cumInputData[:chunks * self.config.binRatio,...]
					oldShape = splitableSection.shape
					newShape = (oldShape[0]/self.config.binRatio, self.config.binRatio, oldShape[1])
					chunked = splitableSection.reshape(newShape)

					cumInputData 		= cumInputData[chunks * self.config.binRatio:,...]
					#chunked = np.array(np.vsplit(splitableSection, self.config.binRatio))
					#print "chunk shape - ", chunked.shape
					averageChunks = chunked.mean(axis=1)
					#print "Averaged?", averageChunks


					averageChunks = averageChunks - 2**15 		# Scale the input reading down by 1/2 full-scale
													# I'm assuming bipolar ACQ range here.
													# This should probably eventually take the config.flags
													# into account.

					for x in range(arrShape[1]):
						#chanGain = gainLUT[self.config.gains[x]]
						#print chanGain, x
						averageChunks[..., x] *= voltsBitLUT[self.config.gains[x]]


					if self.config.logDataRam:
						self.data = np.append(self.data, averageChunks, axis=0)

					if self.config.circularBuffer != None:
						for row in averageChunks:
							self.config.circularBuffer.append(row)
					if self.writeToLogFile:
						fileQueue.put(averageChunks)



			time.sleep(0.001)

		print "Disarming"

		self.iotech.AdcTransferStop()
		print self.iotech.AdcDisarm()


		if self.writeToLogFile:
			self.fileWriterRunning = False
			fileWriterThread.join()

		self.running = False


	def stopCapture(self):
		if self.running:
			self.capRunning = False
			print "Stopping Capture"
			self.capMonThread.join()

	def closeDevice(self):
		print "closing IOTech Interface"

		self.iotech.Close()

	def __del__(self):
		self.closeDevice()

def run():


	config = IOTechConfiguration()
	config.circularBuffer = None

	#config.dataPointsPerChunk =  4096
	#config.freq = 500000

	#config.deviceNameStr = config.listDevices()[1]


	interface = IOTechInterface(config)

	interface.config.logDataRam = False

	print "Starting"
	interface.startCapture(writeFile=True)
	try:
		raw_input()
	except:
		pass
	interface.stopCapture()
	#interface.plotData()


if __name__ == "__main__":



	import cProfile
	import pstats

	cProfile.run('run()', 'fooprof')

	print "Exiting"

	'''
	p = pstats.Stats('fooprof')
	#p.strip_dirs().sort_stats(-1).print_stats()
	#p.sort_stats('name')
	#p.print_stats()
	p.sort_stats('cumulative').print_stats(20)
	p.sort_stats('time').print_stats(20)
	'''




