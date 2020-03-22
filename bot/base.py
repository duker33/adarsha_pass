import abc


class Messenger(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def listen(self):
        pass

    @abc.abstractmethod
    def send(self, message):
        pass
