import threading
import time
if __name__ == "__main__":
    from Lcard_EmptyDevice import LcardE2010B_EmptyDevice
else:
    from .Lcard_EmptyDevice import LcardE2010B_EmptyDevice

class LcardSyncdController:
    def __init__(self, LcardDevice, interrupt_on_Lcard_stop = True):
        self.myThread = None
        self.myEventListener = None
        self.IsActiveController = False
        self.ThreadSleepTime = None
        self.myLcardDevice = LcardDevice
        self.InterruptOnLcardStop = interrupt_on_Lcard_stop

    def startController(self, EventListener, ThreadSleepTime):
        if self.myLcardDevice is None:
            return
        if self.myLcardDevice.syncd is None:
            return
        if self.IsActiveController:
            return
        self.ThreadSleepTime = ThreadSleepTime
        self.myEventListener = EventListener
        self.myThread = threading.Thread(target = self.checkWithTimeout)
        self.IsActiveController = True
        self.myLcardDevice.addListener()
        self.myThread.start()

    def checkWithTimeout(self):
        while self.IsActiveController:
            time.sleep(self.ThreadSleepTime)
            if self.InterruptOnLcardStop and not(self.myLcardDevice.IsActiveMeasurements):
                self.IsActiveController = False
            else:
                self.myEventListener(self.myLcardDevice.syncd())

    def finishController(self):
        self.myLcardDevice.removeListener()
        self.IsActiveController = False
        if self.myThread:
            self.myThread.join()
        self.myThread = None

    def getParameters(self):
        d = self.myLcardDevice.getParameters()
        d["SyncdController.IsActiveController"] = self.IsActiveController
        d["SyncdController.ThreadSleepTime"] = self.ThreadSleepTime
        return d


def test():
    print("Lcard_syncdController test")
    def example(syncd):
        print(syncd)
        #if syncd > 25000:
        #    print("syncd > 25000 !!!")
        return
    lcard = LcardE2010B_EmptyDevice("LcardE2010B.ini")
    lcard_controller = LcardSyncdController(lcard)
    
    lcard.connectToPhysicalDevice()
    lcard_controller.startController(example, 0.03)
    
    time.sleep(10)
    
    lcard.disconnectFromPhysicalDevice()

if __name__ == "__main__":
    try:
        test()
        print(">>success")
    except Exception as e:
        print(">>", e)
        a = input()
