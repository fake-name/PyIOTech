from PyIOTech.daq import daqDevice
from PyIOTech.daqh import DgainX1, DafBipolar,DafUnsigned

dev = daqDevice(b'DaqBoard3031USB')
chan = 0
gain = DgainX1
flags = DafBipolar|DafUnsigned

read = dev.AdcRd(chan, gain, flags)
read = (20.0/2**16)*read -10
print read
dev.Close()
