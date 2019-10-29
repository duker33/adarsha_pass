# magic "run all" here
import typing
from datetime import date, datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from bot import config, drivers, form


class VkAccount:
    ...


class Guest:
    def __init__(
        self,
        surname: str, name: str, patronymic: str,
        vk_account: VkAccount = None
    ):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.vk_account = vk_account

    @classmethod
    def from_fio(cls, fio: str, vk_account: VkAccount = None):
        # use maxsplit because some patronymics could contain whitespaces
        tokens = fio.split(' ', maxsplit=2)
        assert len(tokens) == 3, tokens
        # noinspection PyTypeChecker
        return cls(*tokens, vk_account)

    @property
    def fio(self):
        return ' '.join([self.surname, self.name, self.patronymic])

    def __str__(self):
        return f'FIO: {self.fio}. VK id: {self.vk_account}'

    def __repr__(self):
        return f'FIO: {self.fio}. VK id: {self.vk_account}'


class Pass:
    def __init__(self, guest: Guest, date_: date):
        self.guest = guest
        self.date = date_

    def __str__(self):
        return f'Pass for {self.guest}. To the date {self.date.isoformat()}'

    def __repr__(self):
        return f'Pass for {self.guest}. To the date {self.date.isoformat()}'

    def as_form_data(self) -> typing.Dict[str, str]:
        return form.pass_fields(
            self.guest.surname, self.guest.name, self.guest.patronymic,
            f'{self.date:%d.%m.%Y}'
        )


class Admin:
    """
    Holds all complicated scheme semantic
    - add guest
    - is guest in lists
    - request iq_park for the pass for guest
    """

    def __init__(self, driver: drivers.Driver):
        self.driver = driver

    def order(self, pass_: Pass):
        self.driver.order(pass_)


# @todo #1:15m  Cast Message to dataclass.
class Message:
    messenger = 'VK'
    user_id: str
    text: str

    def __init__(self, user_id: str, text: str, messenger='VK'):
        self.user_id = user_id
        self.text = text


class VkMessenger:
    """Vk bot docs: https://vk.com/dev/bots_docs"""

    MESSAGE_TYPES = [
        VkBotEventType.MESSAGE_NEW,
        VkBotEventType.MESSAGE_REPLY,
        VkBotEventType.MESSAGE_EDIT,
    ]

    @property
    def session(self):
        return vk_api.VkApi(token=config.VK_GROUP_TOKEN)

    @property
    def longpoll(self):
        """
        Long poll integration example
        https://github.com/python273/vk_api/blob/master/examples/bot_longpoll.py
        """
        return VkBotLongPoll(self.session, config.VK_GROUP_ID)

    def listen(self) -> typing.Generator[Message, None, None]:
        for event in self.longpoll.listen():
            if event.type in self.MESSAGE_TYPES:
                yield Message(user_id=event.obj.from_id, text=event.obj.text)


class Bot:
    def __init__(self, admin: Admin, messenger: VkMessenger):
        self.admin = admin
        self.messenger = messenger

    def receive(self, message: Message):
        # waiting #6 to log message receiving
        # Питонов Андрей Андреевич 01.08.2019
        tokens = message.text.split(' ')
        self.admin.order(
            Pass(
                Guest(*tokens[:3], vk_account=message.user_id),
                date_=datetime.strptime(tokens[3], '%d.%m.%Y').date()
            )
        )

    def listen(self):
        for message in self.messenger.listen():
            self.receive(message)
