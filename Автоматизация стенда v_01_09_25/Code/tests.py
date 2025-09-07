"""
# ------ GUI --------------
import MainWindow_CloseEvent
import Tab_Device_Manager, Tab_Filament_and_Anode, Tab_Lcard_VAC_GUI
import Tab_Device_Connections

# ----- Devices -----------
import Lcard_EmptyDevice, Device_Korad

# ----- Device Interfaces -------
import LcardDataInterface, Lcard_IF_FullBuffers
import Lcard_syncdController
"""
from Code.CommandTable import device_controller

tests = [
         device_controller.test
         #Lcard_EmptyDevice.test, Device_Korad.test, # Devices
         #LcardDataInterface.test,                   # Device Interfaces
         #Lcard_syncdController.test, Lcard_IF_FullBuffers.test,
         #Tab_Filament_and_Anode.test,               # GUI
         #Tab_Device_Connections.test,
         #Tab_Lcard_VAC_GUI.test,
         #Tab_Device_Manager.test
         ]



if __name__ == "__main__":
    for itest in tests:
        try:
            itest()
            print(">> success")
            a = input()
            print()
        except Exception as e:
            print(">>", e)
            a = input()
