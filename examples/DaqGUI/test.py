

import DAQScan as DaqS
import time
import queVars


IOTechConfig = DaqS.IOTechConfiguration()
IOTechConfig.localBuffer = queVars.RingBuffer(10000)
IOTechConfig.logDataRam = False
daqint = DaqS.IOTechInterface(IOTechConfig)

time.sleep(1)

daqint.startCapture(writeFile = False)

time.sleep(1)

daqint.stopCapture()

time.sleep(1)

daqint.startCapture(writeFile = False)

time.sleep(1)

daqint.stopCapture()

time.sleep(1)

