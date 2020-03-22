import abc

from returns.result import Result


class Driver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def order(self, pass_) -> Result[bool, str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def confirm(self, pass_) -> bool:
        """Returns "False" in case of connection errors."""
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self, pass_) -> bool:
        """Returns "False" in case of connection errors."""
        raise NotImplementedError()
