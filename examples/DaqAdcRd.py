"""Read a single ADC sample from a single input channel."""
from __future__ import print_function, division
from PyIOTech import daq, daqh

# Device name as registered with the Windows driver.
device_name = b'DaqBoard3K0'
# Input channel number.
channel = 0
# Programmable amplifier with gain of 1.
gain = daqh.DgainX1
# Bipolar-voltage differential input, unsigned-integer readout.
flags = (
    daqh.DafAnalog | daqh.DafUnsigned  # Default flags.
    | daqh.DafBipolar | daqh.DafDifferential  # Nondefault flags.
    )
# max_voltage and bit_depth are device specific.
# Our device's bipolar voltage range is -10.0 V to +10.0 V.
max_voltage = 10.0
# Our device is a 16 bit ADC.
bit_depth = 16

try:
    # Connect to the device.
    dev = daq.daqDevice(device_name)
    # Read one sample.
    data = dev.AdcRd(channel, gain, flags)
    # Convert sample from unsigned integer value to bipolar voltage.
    data = data*max_voltage*2/(2**bit_depth) - max_voltage
    print(data)
finally:
    # Close the connection to the device even if an exception is raised.
    dev.Close()
