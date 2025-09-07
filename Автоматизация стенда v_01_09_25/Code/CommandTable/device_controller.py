import time

if __name__ == "__main__":
    import command_table as ct
else:
    from . import command_table as ct

class DeviceController:
    def __init__(self, korad_device):
        self.korad_device = korad_device
        self.device_commands = {
            "Korad.Set_U" : self._korad_set_u,
            "Korad.Set_I" : self._korad_set_i,
            "Korad.Set_U_for_t" : self._korad_set_u_for_t,
            "Korad.Set_I_for_t" : self._korad_set_i_for_t}

    def _korad_set_u(self, args):
        h = args.split(";")
        if len(h) < 1:
            print("ABORT: CommandTable.Korad.Set_U has not enough values", h)
            return
        self.korad_device.set_uncheckedU(h[0])

    def _korad_set_i(self, args):
        h = args.split(";")
        if len(h) < 1:
            print("ABORT: CommandTable.Korad.Set_I has not enough values:", h)
            return
        self.korad_device.set_uncheckedI(h[0])

    def _korad_set_u_for_t(self, args):
        print("<" + args + ">")
        h = args.split(";")
        if len(h) < 2:
            print("ABORT: CommandTable.Korad.Set_U_for_t has not enough values:", h)
            return
        self.korad_device.set_uncheckedU(h[0])
        self.exec_time_sleep(h[1])

    def _korad_set_i_for_t(self, args):
        h = args.split(";")
        if len(h) < 2:
            print("ABORT: CommandTable.Korad.Set_I_for_t has not enough values:", h)
            return
        self.korad_device.set_uncheckedI(h[0])
        self.exec_time_sleep(h[1])

    def get_device_commands(self):
        return self.device_commands

    def exec_time_sleep(self, time_amount):
        flag = True
        try:
            k = float(time_amount.split(";")[0])
        except Exception as e:
            print(e)
            flag = False
        if flag:
            time.sleep(k)

def create_command_table_with_device_commands(korad_device, lcard_device):
    device_controller = DeviceController(korad_device)
    command_table = ct.CommandTable(command_to_functor = device_controller.get_device_commands())
    return command_table

def read_csv(command_table_filename, korad_device, lcard_device):
    device_controller = DeviceController(korad_device)
    command_table = ct.read_csv(
        command_table_filename,
        command_to_functor = device_controller.get_device_commands())
    return command_table


        
        

def test():
    print("CommandTable.device_controller.test:")
    from Code import Device_Korad, Lcard_EmptyDevice

    korad = Device_Korad.Korad("Korad.ini")
    lcard = Lcard_EmptyDevice.LcardE2010B_EmptyDevice("LcardE2010B.ini")
    dc = read_csv("User Configs/DeviceController_example.csv",
                  korad_device = korad, lcard_device = lcard)
    dc.start_table_execution()
    dc.wait_execution_finish()
    return dc

