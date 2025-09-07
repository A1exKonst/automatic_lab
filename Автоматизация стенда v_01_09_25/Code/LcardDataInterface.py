from .Lcard_EmptyDevice import LcardE2010B_EmptyDevice
import numpy as np
import pandas as pd
import time

class LcardDataInterface:
    def __init__(self, LcardDevice):
        self.myLcardDevice = LcardDevice
        self.data = None
        self.syncd = -1
        self.read_time = -1
        
    def readBuffer(self):
        if not(self.myLcardDevice):
            return
        self.data, self.syncd = self.myLcardDevice.readBuffer()
        self.read_time = time.time()

    def free(self):
        self.data = None
        self.syncd = None
        


AveragedDataColumns = np.array(
    [["LCARD_CH0MEAN","LCARD_CH1MEAN","LCARD_CH2MEAN","LCARD_CH3MEAN"],
     ["LCARD_CH0STD", "LCARD_CH1STD", "LCARD_CH2STD", "LCARD_CH3STD"],
     ["LCARD_CH0MIN", "LCARD_CH1MIN", "LCARD_CH2MIN", "LCARD_CH3MIN"],
     ["LCARD_CH0MAX", "LCARD_CH1MAX", "LCARD_CH2MAX", "LCARD_CH3MAX"]]
    )

def calculateAverage(lcard_IF):
    data = pd.Series([None]*16, index = np.ravel(AveragedDataColumns))
    data["LCARD_COMP_TIME"] = lcard_IF.read_time
    if lcard_IF.data is None:
        lcard_IF.data = data
        return
    N_channels = lcard_IF.data.shape[0]
    columns = np.ravel(AveragedDataColumns[:, :N_channels])
    values = np.ravel(
            [np.mean(lcard_IF.data, axis = 1),
             np.std(lcard_IF.data, axis = 1),
             np.min(lcard_IF.data, axis = 1),
             np.max(lcard_IF.data, axis = 1)])
    data[columns] = values
    lcard_IF.data = data
    return

"""
def calculateAverage_old(lcard_IF):
    if lcard_IF.data is None:
        time_sistem = time.time()
        lcard_IF.data = pd.Series([None]*17, index = LCARD_NAMES._member_map_.values())
        return
    N_channels = lcard_IF.data.shape[0]
    columns = [[f"MeanCh{i}" for i in range(N_channels)], [f"StdCh{i}" for i in range(N_channels)],
              [f"MinCh{i}" for i in range(N_channels)], [f"MaxCh{i}" for i in range(N_channels)]]
    DataPiece = np.ravel(
            [np.mean(lcard_IF.data, axis = 1),
             np.std(lcard_IF.data, axis = 1),
             np.min(lcard_IF.data, axis = 1),
             np.max(lcard_IF.data, axis = 1)])
    columns = np.ravel(columns)
    lcard_IF.data = pd.Series(DataPiece,index = columns)
    return
"""

def cropBuffer(lcard_IF, start, end):
    if lcard_IF.data is None:
        return
    if start > end:
        lcard_IF.data = np.concatenate([lcard_IF.data[:,start : lcard_IF.data.shape[1]],
                                        lcard_IF.data[:, 0 : end]],
                                       axis = 1)
    else:
        lcard_IF.data = lcard_IF.data[:, start : end]
    return

def cropToRequestedBuffer(lcard_IF, requested_buffer_size):
    #print("cropToRequestedBuffer 0")
    if lcard_IF.data is None:
        return
    #print("cropToRequestedBuffer 1")
    try:
        N_channels = lcard_IF.myLcardDevice.adcPar.t4.NCh

        end = lcard_IF.syncd//N_channels
        #print(N_channels)
        start = end - requested_buffer_size
        if start < 0:
            lcard_IF.data = np.concatenate([lcard_IF.data[:,(lcard_IF.data.shape[1] + start) : lcard_IF.data.shape[1]],
                                            lcard_IF.data[:, 0 : end]],
                                           axis = 1)
        else:
            lcard_IF.data = lcard_IF.data[:, start : end]
    except Exception as e:
        print(e)
    #print("cropToRequestedBuffer 2")
    return

def addSynthChannels(lcard_IF, synth_channels_function):
    if not(lcard_IF.data):
        return
    synth_data = synth_channels_function(lcard_IF.data)
    lcard_IF.data = np.concatenate([lcard_IF.data, synth_data])
    return


def test():
    print("LcardDataInterface test")
    import time
    lcard = LcardE2010B_EmptyDevice("LcardE2010B.ini")
    lcard_IF = LcardDataInterface(lcard)
    lcard_IF2 = LcardDataInterface(lcard)
    
    lcard.connectToPhysicalDevice()
    lcard.loadConfiguration()
    lcard.startMeasurements()
    time.sleep(1)

    lcard_IF.readBuffer()
    lcard_IF2.readBuffer()
    
    lcard.finishMeasurements()
    lcard.disconnectFromPhysicalDevice()

    calculateAverage(lcard_IF)
    print(lcard_IF.data)
    cropToRequestedBuffer(lcard_IF2, 8000)
    import matplotlib.pyplot as plt
    plt.scatter(np.arange(len(lcard_IF2.data[0])), lcard_IF2.data[0])
    plt.show()


if __name__ == "__main__":
    try:
        test()
        print(">> success")
    except Exception as e:
        print(">>", e)
    
    
    
