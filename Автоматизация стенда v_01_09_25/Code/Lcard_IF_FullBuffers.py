import numpy as np
import pandas as pd
import time

from PyQt5 import QtCore, QtGui, QtWidgets

if __name__ == "__main__":
        import LcardDataInterface as LDIF
        from Lcard_syncdController import LcardSyncdController
else:
        from . import LcardDataInterface as LDIF
        from .Lcard_syncdController import LcardSyncdController

"""
Lcard_Interface_FullBuffers continuously saves all buffers
received from LcardDevice.

Buffers are stored in list Lcard_Interface_FullBuffers.myDataChunks

This interface uses LcardSyncdController to understand, when
to read data. Data is read when each half of the buffer is full,
then data is cropped to the needed half of buffer and
stored into Lcard_Interface_FullBuffers.myDataChunks.
"""

"""
Design decision: 

Initially Lcard_Interface_FullBuffers supported events upon each buffer fullfillment.
But Lcard outputs data so fast, it calls listeners each 0.05 seconds

For matplotlib.pyplot this was too fast:
it created forbidden access of Data being already updated with Lcard,
but not being drawn in the plot.

In this version Lcard_Interface_FullBuffers stores all data in self.myDataChunks,
so that already stored DataChunks are not modified, and any listener 
can watch stored DataChunks on their own.
"""

class Lcard_Interface_FullBuffers(object):
        def __init__(self, LcardDevice):
                self.myLcardDataInterface = LDIF.LcardDataInterface(LcardDevice)
                self.myDataChunks = []
                self.myLcardController = LcardSyncdController(LcardDevice)
                self.last_syncd = 0

        def startFullBuffersRead(self, ThreadSleepTime):
                print("LcardIFFB.startFullBuffersRead call")
                self.last_syncd = self.myLcardDataInterface.syncd
                self.myLcardController.startController(EventListener = self.onControllerCall,
                                                       ThreadSleepTime = ThreadSleepTime)
                return

        def onControllerCall(self, syncd):
                try:
                        half_buffer = self.myLcardController.myLcardDevice.buffer_size // 2
                        if (self.last_syncd < half_buffer) and (syncd < half_buffer):
                                return # сейчас заполняется первый полубуффер
                        if (self.last_syncd > half_buffer) and (syncd > half_buffer):
                                return # сейчас заполняется второй полубуффер
                        self.myLcardDataInterface.readBuffer()
                        LDIF.cropBuffer(lcard_IF = self.myLcardDataInterface,
                                        start = self.last_syncd,
                                        end = self.myLcardDataInterface.syncd)
                        self.myDataChunks.append(np.copy(self.myLcardDataInterface.data))
                        self.last_syncd = self.myLcardDataInterface.syncd
                except Exception as e:
                        print(e)
                return

        def finishFullBuffersRead(self):
            self.myLcardController.finishController()
            return

        def clearData(self):
            self.myDataChunks = []

        def getIsActiveInterface(self):
            if self.myLcardController is None:
                return False
            return self.myLcardController.IsActiveController

        def getNumpyData(self):
            if self.myDataChunks == []:
                    return np.zeros((1,4))
            if self.myLcardController.IsActiveController:
                    return np.hstack(self.myDataChunks[:-1])
            return np.hstack(self.myDataChunks)

        def getBufferByIndex(self, index):
            index = max(0, min(index, len(self.myDataChunks) - 1 - int(self.myLcardController.IsActiveController)))
            if index < len(self.mydataChunks):
                    return self.myDataChunks[index]
            return np.zeros((1,4)), 0

        def getParameters(self):
            d = self.myLcardController.getParameters()
            d["len(LcardIFFB.myDataChunks)"] = len(self.myDataChunks)
            return d


def test():
    print("Lcard_IF_FullBuffers test")
    
    import Lcard_EmptyDevice
    import matplotlib.pyplot as plt
    
    lcard = Lcard_EmptyDevice.LcardE2010B_EmptyDevice("LcardE2010B.ini")
    lcard.connectToPhysicalDevice()
    #lcard.startMeasurements()
    LcardIFFB = Lcard_Interface_FullBuffers(lcard)
    LcardIFFB.startFullBuffersRead(ThreadSleepTime = 0.03)
    time.sleep(3)
    LcardIFFB.finishFullBuffersRead()

    #lcard.finishMeasurements()
    #lcard.disconnectFromPhysicalDevice()
    
    for idata in LcardIFFB.myDataChunks:
            print(idata.shape)
    data = LcardIFFB.getNumpyData()
    print(data.shape)
    plt.scatter(np.arange(len(data[0])), data[0], s=1)
    plt.show()

if __name__ == "__main__":
    try:
        test()
        print(">> success")
        print()
    except Exception as e:
        print(">>", e)
        a = input()
