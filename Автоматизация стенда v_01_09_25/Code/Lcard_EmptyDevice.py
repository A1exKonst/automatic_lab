import configparser
import time
import numpy as np
from threading import Lock


if __name__ != "__main__":
    from . import Abstract_Device

    from .lcomp.lcomp import LCOMP
    from .lcomp.ldevioctl import (E2010, E2010B, L_ADC_PARAM,
                                 L_ASYNC_ADC_INP, L_ASYNC_DAC_OUT, L_ASYNC_TTL_CFG,
                                 L_ASYNC_TTL_INP, L_ASYNC_TTL_OUT, L_EVENT_ADC_BUF,
                                 L_STREAM_ADC, L_USER_BASE, WASYNC_PAR, WDAQ_PAR)
    from .lcomp.device import e2010
else:
    import Abstract_Device

    from lcomp.lcomp import LCOMP
    from lcomp.ldevioctl import (E2010, E2010B, L_ADC_PARAM,
                                 L_ASYNC_ADC_INP, L_ASYNC_DAC_OUT, L_ASYNC_TTL_CFG,
                                 L_ASYNC_TTL_INP, L_ASYNC_TTL_OUT, L_EVENT_ADC_BUF,
                                 L_STREAM_ADC, L_USER_BASE, WASYNC_PAR, WDAQ_PAR)
    from lcomp.device import e2010
'''
Перед использованием и модификацией классов Lcard на python,
прочитайте опыт неприятных ошибок:

Следующие методы LCOMP:
RequestBufferStream() 
SetParametersStream()
EnableCorrection()
StartLDevice()

Всегда должны находиться в одном Thread.
Нарушение этого правила приведет вас к синему экрану при запуске SetParametersStream
и 3 часам поиска ошибок без возможности нормальных методов дебага.
'''

class LcardE2010B_EmptyDevice(object):
    def __init__(self, config_filename: str):
        super().__init__()
        self.ConfigFilename = config_filename
        
        # Code Controls:
        self._IsActiveMeasurements = False
        self._IsConnected = False
        self.BufferMutex = Lock()
        self.SyncdMutex = Lock()
        self.ListenersAmount = 0
        
        # Lcard buffer parameters:
        self.buffer_size = None
        self.adcPar = None
        self.slPar = None
        self.ldev = None
        self.plDescr = None
        self.data_ptr = None
        self.syncd_ptr = None
        return

    @property
    def IsConnected(self):
        return self._IsConnected
    
    @property
    def IsActiveMeasurements(self):
        if not(self.IsConnected):
            self._IsActiveMeasurements = False
        return self._IsActiveMeasurements

    def __del__(self):
        if self.IsConnected:
            self.disconnectFromPhysicalDevice()
        return

    def connectToPhysicalDevice(self, slot: int = 0):    
        print("Try connect to Lcard")
        if self.IsConnected:
            print("Already connected to Lcard")
            return True
        try:
            self.ldev = LCOMP(slot)
            self.ldev.OpenLDevice()
            self.ldev.LoadBios("Code/e2010m")
            self._IsConnected = bool(self.ldev.PlataTest())
            print("Connect to Lcard E2010. PlataTest: {}".format(self.ldev.PlataTest()))

            self.slPar = self.ldev.GetSlotParam()
            self.plDescr = self.ldev.ReadPlataDescr()
            self._loadConfiguration()
        except Exception as e:
            self._IsConnected = False
            print(e)
            return False
        return True

    def disconnectFromPhysicalDevice(self):
        if not(self.IsConnected):
            return
        self.finishMeasurements()
        if self.ldev:
            print("ldev.CloseLDevice call")
            self.ldev.CloseLDevice()
            print("Lcard disconnected")
        self._IsConnected = False
        return

    def setDAQPAR(self, parameters):
        self.adcPar = WDAQ_PAR()
        self.adcPar.t4.s_Type = L_ADC_PARAM                                     # Для E2010B:
        self.adcPar.t4.FIFO = int(parameters["FIFO"])                               # 4096
        self.adcPar.t4.IrqStep = int(parameters["IrqStep"])                         # 4096
        self.adcPar.t4.Pages = int(parameters["Pages"])                             # 32
        self.adcPar.t4.AutoInit = int(parameters["AutoInit"])                       # 1
        self.adcPar.t4.dRate = float(parameters["dRate"])                           # 1000.0
        self.adcPar.t4.dKadr = float(parameters["dKadr"])                           # 0.001
        self.adcPar.t4.SynchroType = e2010.dSynchroType[parameters["SynchroType"]]  # e2010.INT_START_TRANS
        self.adcPar.t4.SynchroSrc = e2010.dSynchroSrc[parameters["SynchroSrc"]]     # e2010.INT_CLK_TRANS
        self.adcPar.t4.NCh = int(parameters["NCh"])                                 # 1 - 4
        self.adcPar.t4.IrqEna = int(parameters["IrqEna"])                           # 1
        self.adcPar.t4.AdcEna = int(parameters["AdcEna"])                           # 1
        MaskPar = parameters["AdcIMask"].split()       
        print("MaskPar:",MaskPar)
        if MaskPar == ['DEFAULT']:
            tmp = ""
            for i in range(self.adcPar.t4.NCh):
                tmp += "SIG_" + str(i) + " V30_" + str(i) + " "
            MaskPar = tmp.split()
        self.adcPar.t4.AdcIMask = e2010.dCH_BITS[MaskPar[0]]
        for j in range(1, len(MaskPar)):
            self.adcPar.t4.AdcIMask = self.adcPar.t4.AdcIMask | e2010.dCH_BITS[MaskPar[j]]
            # | e2010.SIG_1 | e2010.V10_1 | e2010.SIG_2 | e2010.V03_2 | e2010.GND_3
        for i in range(self.adcPar.t4.NCh):
            self.adcPar.t4.Chn[i] = e2010.dChn[i]                               # e2010.CH_0

    def getDAQPAR(self):
        d = {"Device" : "LcardE2010B", "Connected" : self.IsConnected, "IsActiveMeasurements": None,
             "s_Type": None,"FIFO": None,"IrqStep": None,"Pages": None,"AutoInit": None,
             "dRate": None,"dKadr": None,"SynchroType": None,"SynchroSrc": None,
             "AdcIMask": None,"NCh": None,"IrqEna": None,"AdcEna": None
             }
        if not(self.IsConnected):
            return d
        d["IsActiveMeasurements"] = self.IsActiveMeasurements
        if not(self.adcPar) or not(self.IsActiveMeasurements) or not(self.ldev):
            return d
        #self.adcPar = 
        d["s_Type"] = self.adcPar.t4.s_Type
        d["FIFO"] = self.adcPar.t4.FIFO
        d["IrqStep"] = self.adcPar.t4.IrqStep
        d["Pages"] = self.adcPar.t4.Pages
        d["AutoInit"] = self.adcPar.t4.AutoInit
        d["dRate"] = self.adcPar.t4.dRate
        d["dKadr"] = self.adcPar.t4.dKadr
        d["SynchroType"] = self.adcPar.t4.SynchroType
        d["SynchroSrc"] = self.adcPar.t4.SynchroSrc
        d["AdcIMask"] = self.adcPar.t4.AdcIMask
        d["NCh"] = self.adcPar.t4.NCh
        #d["Chn"] = np.array(self.adcPar.t4.Chn)
        d["IrqEna"] = self.adcPar.t4.IrqEna
        d["AdcEna"] = self.adcPar.t4.AdcEna
        return d

    
    def _loadConfiguration(self):
        if not(self.IsConnected):
            return
        f = open(self.ConfigFilename)
        config = configparser.ConfigParser()
        config.read_file(f)
        if (config["Validation"]["BoardType"] != "E2010B"):
            print("Lcard E2010B: invalid BoardType ini file: ")
            return
        self.setDAQPAR(config["ADC_Parameters"])
        #self.adcPar.t4.s_Type = L_ADC_PARAM                                     # Для E2010B:
        #self.adcPar.t4.FIFO = ADCpar.getint("FIFO")                             # 4096
        #self.adcPar.t4.IrqStep = ADCpar.getint("IrqStep")                       # 4096
        #self.adcPar.t4.Pages = ADCpar.getint("Pages")                           # 32
        #self.adcPar.t4.AutoInit = ADCpar.getint("AutoInit")                     # 1
        #self.adcPar.t4.dRate = ADCpar.getfloat("dRate")                         # 1000.0
        #self.adcPar.t4.dKadr = ADCpar.getfloat("dKadr")                         # 0.001
        #self.adcPar.t4.SynchroType = e2010.dSynchroType[ADCpar["SynchroType"]]  # e2010.INT_START_TRANS
        #self.adcPar.t4.SynchroSrc = e2010.dSynchroSrc[ADCpar["SynchroSrc"]]     # e2010.INT_CLK_TRANS
        #self.adcPar.t4.NCh = ADCpar.getint("NCh")                               # 1 - 4
        #self.adcPar.t4.IrqEna = ADCpar.getint("IrqEna")                         # 1
        #self.adcPar.t4.AdcEna = ADCpar.getint("AdcEna")                         # 1
        #MaskPar = ADCpar["AdcIMask"].split()
        f.close()        
        #print("MaskPar:",MaskPar)
        #if MaskPar == ['DEFAULT']:
        #    tmp = ""
        #    for i in range(self.adcPar.t4.NCh):
        #        tmp += "SIG_" + str(i) + " V30_" + str(i) + " "
        #    MaskPar = tmp.split()
        #self.adcPar.t4.AdcIMask = e2010.dCH_BITS[MaskPar[0]]
        #for j in range(1, len(MaskPar)):
        #    self.adcPar.t4.AdcIMask = self.adcPar.t4.AdcIMask | e2010.dCH_BITS[MaskPar[j]]
        #    # | e2010.SIG_1 | e2010.V10_1 | e2010.SIG_2 | e2010.V03_2 | e2010.GND_3
        #for i in range(self.adcPar.t4.NCh):
        #    self.adcPar.t4.Chn[i] = e2010.dChn[i]                               # e2010.CH_0
        self.ldev.FillDAQparameters(self.adcPar.t4)
        return

    def startMeasurements(self):
        print("Lcard.startMeasurements call")
        if not(self.IsConnected):
            self.connectToPhysicalDevice()
        if not(self.IsConnected):
            return
        if self.IsActiveMeasurements:
            return
        self._IsActiveMeasurements = True
        self.buffer_size = self.ldev.RequestBufferStream(size=131072, stream_id = L_STREAM_ADC)
        self.data_ptr, self.syncd_ptr = self.ldev.SetParametersStream(self.adcPar.t3, self.buffer_size)
        self.ldev.EnableCorrection(True)
        self.ldev.InitStartLDevice()
        self.ldev.StartLDevice()
        return

    def finishMeasurements(self):
        print("Lcard.finishMeasurements call")
        if not(self.IsConnected):
            return
        if not(self.IsActiveMeasurements):
            return
        if self.ldev:
            self.ldev.StopLDevice()
        self._IsActiveMeasurements = False
        return

    def readBuffer(self):
        if not(self.IsConnected) or not(self.IsActiveMeasurements):
            return None, None
        self.BufferMutex.acquire()
        self.SyncdMutex.acquire()
        syncd = self.syncd_ptr()
        data = e2010.GetDataADC(self.adcPar.t4, self.plDescr, # считываем буффер с Lcard
                            self.data_ptr, self.buffer_size)
        self.SyncdMutex.release()
        self.BufferMutex.release()
        return data, syncd

    
    def syncd(self):
        if not(self.IsConnected) or not(self.IsActiveMeasurements):
            print("tried syncd() when", self.IsConnected, self.IsActiveMeasurements)
            return
        self.SyncdMutex.acquire()
        syncd = self.syncd_ptr()
        self.SyncdMutex.release()
        return syncd

    def addListener(self):
        self.ListenersAmount += 1
        if not(self.IsActiveMeasurements):
            self.startMeasurements()

    def removeListener(self):
        self.ListenersAmount -= 1
        if (self.ListenersAmount <= 0) and self.IsActiveMeasurements:
            self.finishMeasurements()
            self.ListenersAmount = 0


def test():
    print("LcardE2010B EmptyDevice test")
    myLcard = LcardE2010B_EmptyDevice("LcardE2010B.ini")
    myLcard.connectToPhysicalDevice(slot=0)
    print(myLcard.getParameters())
    print()
    myLcard.startMeasurements()
    data, syncd = myLcard.readBuffer()
    print("data.shape, syncd:", data.shape, syncd)
    time.sleep(3)
    data, syncd = myLcard.readBuffer()
    print("data.shape, syncd:", data.shape, syncd)
    myLcard.finishMeasurements()
    myLcard.disconnectFromPhysicalDevice()
    if data is None:
        return
    print(">>", np.mean(data,axis=1), np.std(data,axis=1))
    print(">> data.shape, syncd:",data.shape, syncd)
    return

if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        print(">>", e)
