# magic "run all" here
import config
import requests
from datetime import datetime


class PassOrderingError(Exception):
    ...


class VkAccount:
    ...


class Guest:
    def __init__(self, fio: str, vk_account: VkAccount):
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


class Administrator:
    """
    Holds all complicated scheme semantic
    - add guest
    - is guest in lists
    - request iq_park for the pass for guest
    """

    def __init__(self, iq_park: IQPark):
        self.iq_park = iq_park


class Bot:
    """
    - receive FIO for guest
    - create the pass for the guest with admin
    - send an answer for guest
    """
