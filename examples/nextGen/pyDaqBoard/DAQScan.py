
from PyIOTech import daq
from PyIOTech import daqh

import time
import sys
import csv
import threading

import numpy as np
import os
import cPickle

import matplotlib
matplotlib.use("WxAgg")

import matplotlib.pyplot as pplt


#print daq.GetDeviceList()


devName = b'DaqBoard3001USB{321752}'


class IOTechConfiguration:



	def __init__(self):


		self.gainOpts	= {"Gain of 1" : daqh.DgainX1, "Gain of 1" : daqh.DgainX2, "Gain of 1" : daqh.DgainX4, "Gain of 1" : daqh.DgainX8}
		self.bipolarOpts	= {"Bipolar": daqh.DafBipolar, "Unipolar": daqh.DafUnipolar}
		self.settlingOpts	= {"Settling Time = 1 uS": daqh.DafSettle1us, "Settling Time = 5 uS": daqh.DafSettle5us, "Settling Time = 10 uS": daqh.DafSettle10us, "Settling Time = 20 uS": daqh.DafSettle20us, "Settling Time = 1 nS": daqh.DafSettle1ms, }

		self.channelOpts = [self.gainOpts, self.bipolarOpts, self.settlingOpts]





		self.channelSettings	= [	{"channelGain" : daqh.DgainX1, "channelFlags" : [daqh.DafBipolar, daqh.DafSettle1us]},
						{"channelGain" : daqh.DgainX1, "channelFlags" : [daqh.DafBipolar, daqh.DafSettle1us]},
						{"channelGain" : daqh.DgainX1, "channelFlags" : [daqh.DafBipolar, daqh.DafSettle1us]},
						{"channelGain" : daqh.DgainX1, "channelFlags" : [daqh.DafBipolar, daqh.DafSettle1us]} ]
						
		self.scanSettings	= {	"scans"			: 1000,
						"clockSource"		: daqh.DacsAdcClock,
						"transferMask"		: [daqh.DatmDriverBuf, daqh.DatmUpdateBlock, daqh.DatmCycleOn],
						"buffer"		: False,
						"triggerEvent"		: daqh.DatsImmediate,
						"rateMode"		: daqh.DarmFrequency,
						"rateState"		: daqh.DaasPostTrig,
						"acquisitionMode"	: daqh.DaamInfinitePost,
						"frequency"		: 1000.0,
						"iterScans"		: 1000,
						"logDataRam"		: True,
						"circularBuffer"	: False
						}



		self.gains = [daqh.DgainX1, daqh.DgainX1, daqh.DgainX1, daqh.DgainX1]#,
				#daqh.DgainX1, daqh.DgainX1, daqh.DgainX1, daqh.DgainX1]

		self.flags = [daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us]#,

				#daqh.DafBipolar|daqh.DafSettle1us,
				#daqh.DafBipolar|daqh.DafSettle1us,
				#daqh.DafBipolar|daqh.DafSettle1us,
				#daqh.DafBipolar|daqh.DafSettle1us]

		self.channels = [0, 1, 2, 3] 		# , 4, 5, 6, 7]
	

		self.clockSource = daqh.DacsAdcClock

		self.transMask = daqh.DatmDriverBuf | daqh.DatmUpdateBlock | daqh.DatmCycleOn

		self.scans = 1000

		self.buf = False

		self.triggerEv = daqh.DatsImmediate
		
		self.rateMode = daqh.DarmFrequency

		self.rateState = daqh.DaasPostTrig

		self.freq = 1000.0 		# 10000 Hertz

		self.iterScans = 1000

		
		try:
			devL = daq.GetDeviceList()
		except:
			devL = None
		if devL:
			self.deviceNameStr = devL[0]
		else:
			self.deviceNameStr = None

		# PC Side buffering options

		self.logDataRam = True

		self.circularBuffer = False

		self.acqSettings = {"channel" : self.channelSettings, "scan" : self.scanSettings}

		try:
			self.settingsFileName = "acquisitionSettings.pik"
			settingsFile = open(self.settingsFileName, "r")
			self.load(settingsFile)
			settingsFile.close()
			os.unlink(self.settingsFileName)
		except:
			import traceback
			traceback.print_exc()
			print "Failed to load settings file. Is this the first run on this computer?"
			print os.getcwd()
			
	def load(self, fp):
		pickleCont = fp.read()
		unpickled = cPickle.loads(pickleCont)
		self.acqSettings = unpickled


	def saveSettings(self):
		print "Pickling"
		

		settingsFile = open(self.settingsFileName, "w")
		print cPickle.dump(self.acqSettings, settingsFile)
		settingsFile.close()
		print "Done"

	def buildChannelConfigurationArrays(self):
		gains		= []
		flags		= []
		channels	= []
		
		index = 0
		for chan in self.acqSettings["channel"]:
			gains.append(chan["channelGain"])
			flag = 0
			for subFlag in chan["channelFlags"]:
				flag = flag | subFlag
			flags.append(flag)
			channels.append(index)
			index += 1
		return gains, flags, channels
	
	def setSampleFreq(self, freq):

		aggFreq = freq * len(self.channels) 	# 1000 Hertz
		if aggFreq > 1000000:

			print aggFreq
			print freq, len(self.channels) 		# 1000 Hertz
			raise ValueError("Aggregate Scan Frequency cannot exceed 1 Mhz")

		else:
			self.freq = freq

	def listDevices(self):
		return daq.GetDeviceList()

		
class IOTechInterface:

	capRunning = False

	def __init__(self, config=IOTechConfiguration()):
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
			gains, flags, channels = self.config.buildChannelConfigurationArrays()
			self.iotech.AdcSetScan(gains, flags, channels)

	# Set Daq Acquisition mode
			self.iotech.AdcSetAcq(self.config.acqSettings["scan"]["acquisitionMode"])

	# Configure ADC Clocksource
			self.iotech.AdcSetClockSource(self.config.acqSettings["scan"]["clockSource"])

	# Configure Triggering
			self.iotech.SetTriggerEvent(self.config.acqSettings["scan"]["triggerEvent"], None, 0, 0, 0, 0, 0, 0, 0)

			
	# Configure ADC Scanrate

			self.iotech.AdcSetRate(self.config.rateMode, self.config.rateState, self.config.freq)

			
		
			return True

		else:
			raise ValueError("No IO-Tech Found!")

	def startCapture(self, writeFile=False):

		print "Taking Data..."
		print "Actual ADC Freq", self.iotech.AdcGetFreq()
		self.writeToLogFile = writeFile

		self.capMonThread = threading.Thread(target=self.runCapture, name="DAQ Readout Thread")
		self.capRunning = True
		self.capMonThread.start()

	def runCapture(self):

		self.running = True

		# Configure Transfer Buffer
		self.iotech.AdcTransferSetBuffer(self.config.transMask, self.config.scans, self.config.buf)

		#begin data acquisition

		self.iotech.AdcArm()
		self.iotech.AdcTransferStart()

		arrShape = (self.config.iterScans, len(self.config.channels))
		
		if self.writeToLogFile:
			filename = time.strftime("Datalog - %Y %m %d, %a, %H-%M-%S.csv", time.localtime())
			file = open(filename, "wb")
			writer = csv.writer(file)
		else:
			file = None

		bufMask = daqh.DabtmOldest | daqh.DabtmRetAvail

		
		print "Starting Loop"

		while self.capRunning:
			stat = self.iotech.AdcTransferGetStat()
			#print "Stat", stat

			tempDat, retNum = self.iotech.AdcTransferBufData(self.config.iterScans, bufMask)
			
			tempDat = np.array(tempDat)


			#print "Array Shape", arrShape,
			#print "tempDat", tempDat.shape, retNum
			tempDat = tempDat.reshape(arrShape)
			validData = int(retNum.value)
			if validData != 0:
				tempDat = tempDat[:validData, ...]
				#print "shaped", tempDat.shape, tempDat

				if self.config.logDataRam:
					self.data = np.append(self.data, tempDat, axis=0)

				if self.config.circularBuffer != None:
					for row in tempDat:
						self.config.circularBuffer.append(row)


				if file:
					writer.writerows(tempDat)

		print "Disarming"

		self.iotech.AdcTransferStop()
		print self.iotech.AdcDisarm()


		if file:
			file.close()

		self.running = False


	def stopCapture(self):
		if self.running:
			self.capRunning = False
			print "Stopping Capture"
			self.capMonThread.join()
		
	def plotData(self):
		if not self.config.logDataRam:
			raise ValueError
		mainWin = pplt.figure()
		#mainWin.subplots_adjust(hspace=.4, wspace=.4)
		#Add space between subplots to make them look nicer

		print "Adding Plot"
		plot1 = mainWin.add_subplot(1, 1, 1)
		#plot2 = mainWin.add_subplot(2,1,2)
		print "Step2"
		plot1.plot(self.data[..., 0])
		plot1.plot(self.data[..., 1])
		plot1.plot(self.data[..., 2])
		plot1.plot(self.data[..., 3])
		plot1.plot(self.data[..., 4])
		plot1.plot(self.data[..., 5])
		plot1.plot(self.data[..., 6])
		plot1.plot(self.data[..., 7])
		print "Step3"
		plot1.grid()
		#plot2.grid()
		print "Showing Graph"
		pplt.show()

	def closeDevice(self):
		print "closing IOTech Interface"

		self.iotech.Close()

	def __del__(self):
		self.closeDevice()

if __name__ == "__main__":




	
	config = IOTechConfiguration()


	config.gains = [daqh.DgainX1, daqh.DgainX1, daqh.DgainX1, daqh.DgainX1,
			daqh.DgainX1, daqh.DgainX1, daqh.DgainX1, daqh.DgainX1,
			daqh.DgainX1, daqh.DgainX1, daqh.DgainX1, daqh.DgainX1,
			daqh.DgainX1, daqh.DgainX1, daqh.DgainX1, daqh.DgainX1]

	config.channels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

	config.flags = [daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us,
				daqh.DafBipolar | daqh.DafSettle1us]

	config.iterScans = 1000
	config.freq = 1000

	#config.deviceNameStr = config.listDevices()[1]


	interface = IOTechInterface(config)


	print "Starting"
	interface.startCapture(writeFile=False)
	raw_input()
	interface.stopCapture()
	interface.plotData()


	
