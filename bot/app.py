# magic "run all" here
import config
import requests
from datetime import datetime

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


class Pass:
    def __init__(self, guest: Guest, date: datetime):
        self.guest = guest
        self.date = datetime


class IQPark:
    """
    - create pass for guest
    """
    PASS_URL = 'https://2an.ru/new_order.aspx'

    def create_pass(self, guest: Guest=None):
        """
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
        self.iq_park.create_pass(pass_)


class Bot:
    """
    - receive FIO for guest
    - create the pass for the guest with admin
    - send an answer for guest
    """

    def __init__(self, admin: Admin):
        self.admin = admin

    def order_pass(self, message: str):
        # Питонов Андрей Андреевич 01.08.2019
        tokens = message.split(' ')
        self.admin.order(
            Pass(
                Guest(' '.join(tokens[:3])),
                date=datetime(tokens[3])
            )
        )

    def receive(self, message: str):
        # TODO - log info there
        self.order_pass(message)

    VK_MESSAGE_TYPES = [VkBotEventType.MESSAGE_NEW, VkBotEventType.MESSAGE_REPLY, VkBotEventType.MESSAGE_EDIT]

    def listen_vk(self):
        # Long poll example
        # https://github.com/python273/vk_api/blob/master/examples/bot_longpoll.py
        # VK integration here
        # TODO - dev good arch for bot server
        vk_session = vk_api.VkApi(token=config.VK_GROUP_TOKEN)
        longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID)

        for event in longpoll.listen():
            if event.type in self.VK_MESSAGE_TYPES:
                user = event.obj.from_id
                text = event.obj.text
                print(user, text)


Bot(Admin(IQPark())).listen_vk()
