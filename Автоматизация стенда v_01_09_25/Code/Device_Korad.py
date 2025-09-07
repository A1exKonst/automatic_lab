import configparser
import numpy as np
import time
import pandas as pd
import serial
from threading import Lock
from enum import Enum

#from .Abstract_Device import Device, DeviceParameter

KORAD_COLUMNS = ["KORAD_TIME", "KORAD_U", "KORAD_I"]


"""
NOTE 19.06.25:
На Korad KWR102 аппаратно нельзя установить v = 0, i = 0
                (даже через кнопочки на его панели)
Чтобы установить (0;0) необходимо сделать FinishExperiment(), StartExperiment().
                (с кнопочками на панели все так же: нужно дважды нажать ON/OFF)
"""



class Korad: #(Device):

    type = "Korad"

    def __init__(self, config_filename:str):
        self.ConfigFilename = config_filename
        self.ser = None
        self.mutex = Lock()
        self._IsActiveMeasurements = False

    @property
    def IsConnected(self):
        return not(self.ser is None)
    
    @property
    def IsActiveMeasurements(self):
        if not(self.IsConnected):
            self._IsActiveMeasurements = False
        return self._IsActiveMeasurements

    def StartExperiment(self, set_OUT = False):
        print("Device_Korad.StartExperiment call")
        if not(self.IsConnected):
            print("Device_Korad.StartExperiment dismissed: Korad.IsConnected is", self.IsConnected)
            return
        if set_OUT:
            self.mutex.acquire()
            self.ser.write(f'OUT:1\r'.encode('ASCII'))
            self.mutex.release()
        self._IsActiveMeasurements = True
        print(self.IsConnected, self._IsActiveMeasurements, self.IsActiveMeasurements)
        print("Device_Korad.StartExperiment executed")
        return

    def FinishExperiment(self, set_OUT = False):
        if not(self.IsConnected):
            return
        #self.Set_v_i(0,0)
        if set_OUT:
            self.mutex.acquire()
            self.ser.write(f'OUT:0\r'.encode('ASCII'))
            self.mutex.release()
        self._IsActiveMeasurements = False
        return
    
    def TakeMeasurements(self):
        if not(self.IsConnected):
            time_sistem = time.time()
            #print("Korad is not connected; tried Korad.TakeMeasurements()")
            return pd.Series([time_sistem, None, None],index = KORAD_COLUMNS)

        if not(self.IsActiveMeasurements):
            time_sistem = time.time()
            #print("Korad is connected, but not active; tried Korad.TakeMeasurements()")
            return pd.Series([time_sistem, None, None],index = KORAD_COLUMNS)

        self.mutex.acquire()
        voltage = None # если мы опрашивали корад, а он отключился 
        current = None # то без этих строк можно получить ошибку:
                       # cannot access local variable "voltage"
                       # where it is not associated with value.
        try:
            #self.ser.write(b'\r')
            self.ser.write(b'VOUT?\r')
            voltage = float(self.ser.readline().decode()[:-1])
            self.ser.write(b'IOUT?\r')
            current = float(self.ser.readline().decode()[:-1])
        except Exception as e:
            print(e)
        self.mutex.release()
        time_sistem = time.time()
        
        return pd.Series([time_sistem, voltage, current],index = KORAD_COLUMNS)

    def Set_v_i(self,v=None,i=None):
        print("Korad set v i", v, i, self.IsConnected, self.IsActiveMeasurements)
        if not(self.IsConnected):
            #print("Korad is not connected; tried Korad.Set_v_i()")
            return
        elif not(self.IsActiveMeasurements):
            #print("Korad is connected, but not active; tried Korad.Set_v_i()")
            return
        else:
            self.mutex.acquire()
            if not(v is None):
                self.ser.write(f'VSET:{v}\r'.encode('ASCII'))
            if not(i is None):
                self.ser.write(f'ISET:{i}\r'.encode('ASCII'))
            self.mutex.release()

    def set_v_slope(self, v_slope):
        print("Korad set v slope", v_slope, self.IsConnected, self.IsActiveMeasurements)
        self.mutex.acquire()
        self.ser.write(f'VSLOPE:{v_slope}\r'.encode('ASCII'))
        """
        VSLOPE: 31.5
        Set the output voltage slope to be 31.5 V / 100 uS
        """
        self.mutex.release()

    def set_i_slope(self, i_slope):
        print("Korad set i slope", i_slope, self.IsConnected, self.IsActiveMeasurements)
        self.mutex.acquire()
        self.ser.write(f'ISLOPE:{i_slope}\r'.encode('ASCII'))
        """
        ISLOPE: 1.5
        Set the slope of the output current to be 1.5 A / 100 uS
        """
        self.mutex.release()

    def ConnectToPhysicalDevice(self, config_dict = None):
        print("Korad.ConnectToPhysicalDevice call")
        try:
            if not(config_dict):
                config_dict = self.LoadConfiguration()
            print(config_dict)
            self.ser = serial.Serial(config_dict['com port'],
                            config_dict['bits per second'],
                            timeout=1,
                            parity=config_dict['parity'],
                            stopbits=config_dict['stop bits'],
                            xonxoff=config_dict['xonxoff'],
                            rtscts=config_dict['rtscts'],
                            bytesize=config_dict['data bits'])
        except Exception as e:
            print("Try connect Korad:", e)
            self.ser = None
            return False
        print("Korad.ConnectToPhysicalDevice executed")
        return True 

    def DisconnectFromPhysicalDevice(self):
        print("Korad.DisconnectFromPhysicalDevice call")
        self.FinishExperiment()
        if self.ser:
            self.ser.close()
            self.ser = None
        print("Korad.DisconnectFromPhysicalDevice executed")

    def LoadConfiguration(self):
        config = configparser.ConfigParser()
        config.read(self.ConfigFilename)
        bits_per_second = config['COM settings']['bits per second']
        data_bits = config['COM settings']['data bits']
        parity_name = config['COM settings']['parity']
        stop_bits = config['COM settings']['stop bits']
        flow_control_bits = config['COM settings']['flow control']
        flow_control_bits_xon_xoff = (flow_control_bits == 'Xon / Xoff')
        flow_control_bits_hardware = (flow_control_bits == 'Hardware')
        com_port = config['COM settings']['com port']
        dict_parity = {'None': serial.PARITY_NONE,
                       'Even': serial.PARITY_EVEN,
                       'Odd': serial.PARITY_ODD,
                       'Mark': serial.PARITY_MARK,
                       'Space': serial.PARITY_SPACE}
        parity = dict_parity[parity_name]
        config_dict = {'com port':com_port,
                       'bits per second':int(bits_per_second),
                       'data bits':int(data_bits),
                        'parity':parity,
                       'stop bits':float(stop_bits),
                       'xonxoff':flow_control_bits_xon_xoff,
                       'rtscts':flow_control_bits_hardware}
        return config_dict

    def set_uncheckedI(self, value):
        s = None
        try:
            s = float(value)
        except Exception as e:
            pass
        if not(s is None):
            self.Set_v_i(i = s)
        return

    def set_uncheckedU(self, value):
        s = None
        try:
            s = float(value)
        except Exception as e:
            print(">>",e)
        if not(s is None):
            self.Set_v_i(v = s)
        return

    def __del__(self):
        if self.ser is None:
            return
        self.ser.write(f'VSET:0\r'.encode('ASCII'))
        self.ser.write(f'ISET:0\r'.encode('ASCII'))
        self.ser.write(f'OUT:0\r'.encode('ASCII'))
        return

    def getParameters(self):
        d = {"Korad.serial_port" : None}
        if not(self.ser):
            return d
        d["Korad.serial_port"] = self.ser.port
        d["Korad.baudrate"] = self.ser.baudrate
        d["Korad.bytesize"] = self.ser.bytesize
        d["Korad.parity"] = self.ser.parity
        d["Korad.stopbits"] = self.ser.stopbits
        d["Korad.timeout"] = self.ser.timeout
        d["Korad.xonxoff"] = self.ser.xonxoff
        d["Korad.rtscts"] = self.ser.rtscts
        d["Korad.dsrdtr"] = self.ser.dsrdtr
        return d

def test():
    print("Device_Korad.test\n")
    myKorad = Korad('Korad.ini')
    print(myKorad.getParameters(), "\n")
    myKorad.ConnectToPhysicalDevice()
    print(myKorad.getParameters(), "\n")
    myKorad.StartExperiment()
    print("myKorad.StartExperiment executed\n")
    myKorad.Set_v_i(1, None)
    print("myKorad.Set_v_i(1, None) executed\n")
    print(myKorad.TakeMeasurements(), "\n")
    print("myKorad.TakeMeasurements executed\n")
    time.sleep(2)
    myKorad.FinishExperiment()
    myKorad.DisconnectFromPhysicalDevice()
    #print(time.time())
    #for i in range(1000):
    #    v = myKorad.TakeMeasurements()
    #print(time.time())
    return

if __name__ == "__main__":
    print("Device_Korad.test\n")
    myKorad = Korad('Korad.ini')
    print(myKorad.getParameters(), "\n")
    myKorad.ConnectToPhysicalDevice()
    print(myKorad.getParameters(), "\n")
    myKorad.StartExperiment()
    print("myKorad.StartExperiment executed\n")
    myKorad.Set_v_i(1, None)
    print("myKorad.Set_v_i(1, None) executed\n")
    print(myKorad.TakeMeasurements(), "\n")
    print("myKorad.TakeMeasurements executed\n")
    time.sleep(2)
    myKorad.FinishExperiment()
    myKorad.DisconnectFromPhysicalDevice()
    print(">> success")
        


