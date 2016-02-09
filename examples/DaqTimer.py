"""
This program will run for 30 seconds on a python-based timer.  Input will be
taken every 0.5 seconds and the output will change every 5 seconds.
Two timer functions will be set up to run at the same time.
"""
from __future__ import print_function, division
import time
from PyIOTech import daq, daqh


# Device name as registered with the Windows driver.
device_name = b'DaqBoard3K0'

# Total time in seconds.
runtime = 30

# Input
inputChan = 0
inputGain = daqh.DgainX1  # No gain
inputFlags = daqh.DafAnalog | daqh.DafUnsigned | daqh.DafBipolar | daqh.DafDifferential
inputFreq = 2  # Twice per second

# Output
outChan = 0  # DAC0 channel
outType = daqh.DddtLocal  # DAC channel location
outData = 3.3  # In Volts
outSwitch = True
outFreq = 0.2  # Once per 5 seconds

# Our device's bipolar voltage range is -10.0 V to +10.0 V with gain of 1.
max_voltage = 10.0
# Our device is a 16 bit ADC.
bit_depth = 16

# Data to read
data = []

# Timer functions
def daqOutput(dev, outSwitch):
    if outSwitch:
        dev.DacWt(outType, outChan, outData)
        outSwitch = False
    else:
        dev.DacWt(outType, outChan, 0.0)
        outSwitch = True
    return outSwitch

def daqInput(dev):
    read = dev.AdcRd(inputChan, inputGain, inputFlags)
    # The data list is a global variable and can be accessed anywhere.
    data.append(read)


try:
    # Setup the device.
    dev = daq.daqDevice(device_name)
    # Timers
    for i in range(int(runtime*outFreq)):
        outSwitch = daqOutput(dev, outSwitch)
        # Execute 10 times, or for 5 seconds then switch the output.
        for v in range(int(inputFreq/outFreq)):
            daqInput(dev)
            time.sleep(1.0/inputFreq)

    for i in data:
        # Convert sample from unsigned integer value to bipolar voltage.
        print(i*max_voltage*2/(2**bit_depth) - max_voltage)
finally:
    dev.Close()
