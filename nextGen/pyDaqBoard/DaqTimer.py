from daq import daqDevice
from daqh import DgainX1, DafBipolar, DddtLocal
import time

"""
This function will run for 30 seconds on a python based timer.  Input will be
taken every 0.5 seconds and the output will change every 5 seconds.
Two timer functions will be set up to run at the same time
"""

#Setup the devices
dev = daqDevice('DaqBoard2K0')

#Runtime
runtime = 10

#Input
inputChan = 0
inputGain = DgainX1 #No gain
inputFlags = DafBipolar # -10.0 to 10.0 with no gain
inputFreq = 2 #Twice per second

#Output
outChan = 0
outType = DddtLocal #Always use, default
outData = 3.3 #In Volts
outSwitch = True
outFreq = 0.5 

#Data to read
data = [] 

#Timer functions
def daqOutput(outSwitch):

    if outSwitch:
        dev.DacWt(outType, outChan, outData)
        outSwitch = False
    else:
        dev.DacWt(outType, outChan, 0.0)
        outSwitch = True

    return outSwitch

def daqInput():

    read = dev.AdcRd(inputChan, inputGain, inputFlags)
    data.append(read) #the Data list is a global variable and can be accesed anywhere

#Timers
for i in range(int(runtime*outFreq)): #Execute for ten seconds, 2*outInterval
    outSwitch = daqOutput(outSwitch)
    for v in range(int(inputFreq/outFreq)): #Execute 10 times, or for 5 seconds then switches the output
        daqInput()
        time.sleep(1.0/inputFreq)

for i in data:
    print dev.ADConvert(i)

dev.Close()


