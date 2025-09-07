from Code.CommandTable import CommandTable as CT

def read_csv(CommandTable_filename, Korad_device, Lcard_device):
    device_commands = {"Korad.Set_U" : Korad_device.set_uncheckedU,
                       "Korad.Set_I" : Korad_device.set_uncheckedI}
    ct = CT.read_csv(CommandTable_filename,
                     dCommand_to_Functor = device_commands)
    return ct
        
def test():
    from Code import Device_Korad, Lcard_EmptyDevice

    korad = Device_Korad.Korad("Korad.ini")
    lcard = Lcard_EmptyDevice.LcardE2010B_EmptyDevice("LcardE2010B.ini")
    dc = read_csv("User Configs/DeviceController_example.csv",
                  Korad_device = korad, Lcard_device = lcard)
    dc.startTableExecution()
    dc.waitExecutionFinish()
