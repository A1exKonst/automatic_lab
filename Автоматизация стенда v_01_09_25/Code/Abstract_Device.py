class Device:
    type = "Undefined_Device"

    def __init__(self, config_filename: str):
        super().__init__()
        self._ConfigFilename = config_filename
        self._MeasurementsFile = None
        self.ConfigFilename = config_filename

    @property
    def CurrentMeasurementsFile(self):
        return self._MeasurementsFile

    def ConnectToPhysicalDevice(self, args):
        # Все действия, необходимые при первом
        # налаживании общения с устройством
        return

    def DisconnectFromPhysicalDevice(self):
        # Все действия, необходимые при отключении
        # отключении нас от управления этим устройством
        # aka отдаем управление им системе
        return

    def LoadConfiguration(self):
        # Загружаем все параметры из .config файла
        return

    def StartMeasurements(self, measurements_file: str):
        self._MeasurementsFile = open(measurements_file)
        # Создание и инициализация потока
        # для записи в файл.
        # Передача в поток функции self.TakeMeasurements
        return

    def TakeMeasurements(self):
        # функция, запускаемая в потоке и проверяющая,
        # пора ли запрашивать новые данные от устройства

        # При необходимости запрашивает данные и записывает их в файл
        # self._MeasurementsFile. Периодически запускает fflush()

        # При обнаружении ошибок / условий для прекращения снятия данных
        # может самостоятельно запустить self.FinishMeasurements
        return

    def FinishMeasurements(self):
        # Корректное закрытие файла self._MeasurementsFile
        # Корректное уничтожение дочернего потока
        return

    def GetDeviceParameters(self):
        return

class DeviceParameter:
    def __init__(self, device, par_name: str,
                 is_gettable = (lambda dev: True),
                 get_value = (lambda dev, name: getattr(dev, name)),
                 is_settable = (lambda dev, val: False),
                 set_value = (lambda dev, name, val: setattr(dev, name, val))):
        
        self.myDevice = device
        self.myParName = par_name
        
        self.myIsSettable = is_settable
        self.mySetValue = set_value

        self.myIsGettable = is_gettable
        self.myGetValue = get_value
        return

    def Get(self):
        print("DeviceParameter::Get")
        if (self.myIsGettable(self.myDevice)):
            return self.myGetValue(self.myDevice, self.myParName)
        return None
    
    def Set(self, new_value)-> bool:
        print("DeviceParameter::Set")
        if (self.myIsSettable(self.myDevice, new_value)):
            self.mySetValue(self.myDevice, self.myParName, new_value)
            return True
        print("DeviceParameter", self.myParName, "set: declined")
        return False 

class MultipleChoiceDeviceParameter(DeviceParameter):
    def __init__(self, device, par_name: str,
                 choice_to_value: {},
                 value_to_choice: {},
                 is_settable = (lambda dev, val: True)):
        super().__init__(device, par_name, is_settable=is_settable)
        self.dChoiceToValue = dchoice_to_value
        self.dValueToChoice = dvalue_to_choice

    def Get(self):
        print("MultipleChoice::Get")
        k = super().Get()
        if(k in self.dValueToChoice.keys()):
            return self.dValueToChoice[k]
        print(k, "not found in values of", self.myParName)
        return None

    def Set(self, choise):
        print("MultipleChoice::Set")
        if(choice in self.dChoiceToValue.keys()):
            return super().Set(self.dChoiceToValue[choise])
        print(choice, "not found in choices of", self.myParName)
        return False


