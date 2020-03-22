import attr
from bot import app, base


@attr.s(auto_attribs=True)
class Messenger(metaclass=base.Messenger):
    user_id: str
    text: str

    def listen(self):
        yield app.Message(user_id=self.user_id, text=self.text)

    def send(self, message: app.Message):
        pass
