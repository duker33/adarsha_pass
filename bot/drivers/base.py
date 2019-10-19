class Driver:
    # TODO - add annotation
    def order(self, pass_):
        raise NotImplementedError()

    def confirm(self, pass_) -> bool:
        """Returns "False" in case of connection errors."""
        raise NotImplementedError()
