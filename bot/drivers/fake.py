from . import base


class Fake(base.Driver):
    ordered = []

    def order(self, pass_):
        # waiting #3 for the logger
        self.ordered.append(pass_)
        print(f'pass {pass_} ordered')

    def confirm(self, pass_):
        return pass_ in self.ordered
