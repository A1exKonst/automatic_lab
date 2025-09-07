import PyQt5

class Parameter:
    def __init__(self):
        self.value = None

    def __get__(self):
        return self.value

    def __set__(self, value):
        self.value = value
