from daq import daqDevice
from daqh import DgainX1, DafBipolar,DafUnsigned

dev = daqDevice('DaqBoard3031USB')
chan = 0
gain = DgainX1
flags = DafBipolar|DafUnsigned

read = dev.AdcRd(chan, gain, flags)
read = (20.0/2**16)*read -10
print read
dev.Close()
