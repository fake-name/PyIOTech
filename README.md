PyIOTech
========

Python wrapper for IOTech/Measurement-Computing data-acquisition devices.

Keywords: DaqBoard, DaqBook, DaqLab, DaqScan, Personal Daq, TempBook, WaveBook.
<br>


## Example Usage ##

Read a single ADC sample from a single input channel:
```python
from __future__ import print_function, division
from PyIOTech import daq, daqh

device_name = b'DaqBoard3K0'
channel = 0
gain = daqh.DgainX1
flags = daqh.DafAnalog | daqh.DafUnsigned | daqh.DafBipolar | daqh.DafDifferential
max_voltage = 10.0
bit_depth = 16

try:
    dev = daq.daqDevice(device_name)
    data = dev.AdcRd(channel, gain, flags)
    # Convert sample from unsigned integer value to bipolar voltage.
    data = data*max_voltage*2/(2**bit_depth) - max_voltage
    print(data)
finally:
    dev.Close()
```

For more complex, commented examples, see the [examples](examples/) directory.
<br>


## Documentation ##

There is no official documentation for PyIOTech, however the python function-signature follows closely the C/C++ or Visual Basic function-signature, as documented in the [IOTech Programmer's Manual](IOTechProgrammersManual.pdf).  For the specific python API, consult the [source code](PyIOTech/daq.py) or the [examples](examples/).


## Installation ##

This is a pure python distribution with no external dependencies (except the IOTech device driver "daqx.dll"). Tested with python 2.7 and 3.4.

To install, run: `$ python setup.py install`


## Credits ##

Heavily based on [pydaqboard](https://code.google.com/archive/p/pydaqboard/).


## License ##

[GNU General Public License, version 2](LICENSE.txt).


## Maintainers wanted! ##

I'm currently no longer employed at a lab using IOTech devices, so I'm no longer in a position to maintain this library. If you're interested in being a maintainer for this package, just ask and I'll happily give you write permissions.
