# magic "run all" here
import attr
import random
import typing
from datetime import date, datetime
from itertools import zip_longest
from returns.pipeline import pipeline
from returns.result import Result, Success, Failure
from requests.exceptions import RequestException

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from bot import config, base, drivers, form


class VkAccount:
    ...


class Guest:
    def __init__(
        self,
        surname: str, name: str, patronymic: str,
        vk_account: typing.Union[VkAccount, str, None] = None
    ):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.vk_account = vk_account

    @classmethod
    def from_fio(cls, fio: str, vk_account: VkAccount = None):
        tokens = fio.split(' ', maxsplit=2)
        # someone has no patronymic, someone - complex one
        assert len(tokens) >= 2, tokens
        tokens = [t or d for t, d in zip_longest(tokens, 3*[''])]
        return cls(*tokens, vk_account)

    @property
    def fio(self):
        return ' '.join([self.surname, self.name, self.patronymic])

    def __str__(self):
        return f'FIO: {self.fio}. VK id: {self.vk_account}'


class Pass:
    def __init__(self, guest: Guest, date_: date):
        self.guest = guest
        self.date = date_

    def __str__(self):
        return f'Pass for {self.guest}. To the date {self.date.isoformat()}'

    def valid_for_order(self) -> Result[bool, str]:
        return (
            Success(True) if self.date >= date.today()
            else Failure('Past date pass')
        )

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

    @pipeline(Result)
    def order(self, pass_: Pass) -> Result[bool, str]:
        print('order pass', pass_)
        pass_.valid_for_order().unwrap()
        return self.driver.order(pass_)

    def confirm(self, pass_: Pass) -> bool:
        res = self.driver.confirm(pass_)
        word = 'confirmed' if res else 'rejected'
        print(f'{word} pass', pass_)
        return res


# @todo #1:15m  Cast Message to dataclass.
class Message:
    messenger = 'VK'
    user_id: str
    text: str

    def __init__(self, user_id: str, text: str, messenger='VK'):
        self.user_id = user_id
        self.text = text

    def __str__(self):
        return f'user={self.user_id}. {self.text}'


class VkMessenger(base.Messenger):
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
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type in self.MESSAGE_TYPES:
                        yield Message(user_id=event.obj.from_id, text=event.obj.text)
            except RequestException as e:
                print(str(e))

    def send(self, message: Message):
        vk = self.session.get_api()
        vk.messages.send(
            user_id=message.user_id,
            random_id=random.randrange(0, 2**64),
            message=message.text
        )


@attr.s(auto_attribs=True)
class Bot:
    admin: Admin
    messenger: VkMessenger
    MY_MESSAGES = [
        'Пропуск', 'Не могу сделать пропуск',
    ]

    def receive(self, message: Message) -> Message:
        # waiting #6 to log message receiving
        # Питонов Андрей Андреевич 01.08.2019
        result = ''
        tokens = message.text.split()
        pass_ = Pass(
            Guest(*tokens[:3], vk_account=message.user_id),
            date_=datetime.strptime(tokens[3], '%d.%m.%Y').date()
        )
        ordered = self.admin.order(pass_)
        if ordered.value_or(None) is None:
            result = 'Не могу сделать пропуск с неверными данными'
            if 'Past date pass' in ordered.fix(lambda x: x).unwrap():
                result = 'Не могу сделать пропуск с прошедшей датой'
        return Message(
            user_id=message.user_id,
            text=result or (
                f'Пропуск успешно заказан'
                if self.admin.confirm(pass_) else f'Ошибка при заказе пропуска'
            )
        )

    def listen(self):
        for message in self.messenger.listen():
            if all(msg not in message.text for msg in self.MY_MESSAGES):
                answer = self.receive(message)
                self.messenger.send(answer)
