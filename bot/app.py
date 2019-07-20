# magic "run all" here
import config
import requests
import typing
from datetime import date, datetime

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class PassOrderingError(Exception):
    ...


class VkAccount:
    ...


class Guest:
    def __init__(self, fio: str, vk_account: VkAccount=None):
        self.fio = fio
        self.vk_account = vk_account

    def __str__(self):
        return f'{self.fio}. Account {self.vk_account}'


class Pass:
    def __init__(self, guest: Guest, date_: date):
        self.guest = guest
        self.date = date_

    def __str__(self):
        return f'Pass for {self.guest}. To the date {self.date.isoformat()}'


class IQPark:
    """
    - create pass for guest
    """
    PASS_URL = 'https://2an.ru/new_order.aspx'

    def create_pass(self, guest: Guest=None):
        """
        Draft method. Take form data file and order pass.

        @raises PassOrderingError
        """
        with open('form_data/form.txt', 'r', encoding='utf-8') as f:
            s = lambda line: line.split(':')
            data = {
                s(line)[0]: s(line)[1].strip()
                for line in f.read().split('\n')
                if len(s(line)) > 1
            }
            # TODO - cleanup file. Move all private data to the config
            response = requests.post(self.PASS_URL, data, auth=(config.LOGIN, config.PASSWORD))
            if response.status_code == 200:
                # TODO - log success
                pass
            else:
                # TODO - log failure
                pass


class Admin:
    """
    Holds all complicated scheme semantic
    - add guest
    - is guest in lists
    - request iq_park for the pass for guest
    """

    def __init__(self, iq_park: IQPark):
        self.iq_park = iq_park

    def order(self, pass_: Pass):
        print('order pass', pass_)
        self.iq_park.create_pass(pass_)


# TODO - dockerize the app
# Waiting docker to use dataclasses from containerized py3.7
# @dataclass
class Message():
    messenger = 'VK'
    user_id: str
    text: str

    def __init__(self, user_id: str, text: str, messenger='VK'):
        self.user_id = user_id
        self.text = text


class VkMessenger:
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

    # TODO - only Admin should create passes. Refactor arch
    def order_pass(self, message: Message):
        # Питонов Андрей Андреевич 01.08.2019
        tokens = message.text.split(' ')
        self.admin.order(
            Pass(
                Guest(fio=' '.join(tokens[:3]), vk_account=message.user_id),
                date_=datetime.strptime(tokens[3], '%d.%m.%Y').date()
            )
        )

    def receive(self, message: Message):
        # TODO - log info there
        self.order_pass(message)

    def listen(self):
        for message in self.messenger.listen():
            self.receive(message)


Bot(
    Admin(IQPark()),
    VkMessenger()
).listen()
