"""Output an analog voltage to a single DAC channel."""
import time
from PyIOTech.daq import daqDevice
from PyIOTech.daqh import DddtLocal

# Device name as registered with the Windows driver.
device_name = b'DaqBoard3K0'
# Output channel number.
channel = 0
# DAC channel location.
deviceType = DddtLocal
# Output 3.3 Volts.
dataVal = 3.3

try:
    # Connect to the device.
    dev = daqDevice(device_name)
    # Set the output voltage.
    dev.DacWt(deviceType, channel, dataVal)
    # Wait for 5 seconds.
    time.sleep(5)
    # Reset the output voltage to zero.
    dev.DacWt(deviceType, channel, 0.0)
finally:
    # Close the connection to the device even if an exception is raised.
    dev.Close()
