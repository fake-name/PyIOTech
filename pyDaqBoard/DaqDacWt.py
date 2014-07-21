from daq import daqDevice
from daqh import DddtLocal

#Open the device named DaqBoard2KO
dev = daqDevice('DaqBoard2K0')

#Configure our Output data
channel = 0
deviceType = DddtLocal #DddtLocal is the best to use, channels are indexed 0 and 1 in this case
dataVal = 3.3 #Output 3.3V

dev.DacWt(deviceType, channel, dataVal)

dev.Close() #Make sure to close the device afterword to avoid any later issues
