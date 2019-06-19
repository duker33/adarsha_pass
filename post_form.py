"""Failed try to post form in automated mode without selenium."""

import logging
import requests
import typing

import config
from dataclasses import dataclass


@dataclass
class FormData:
    url: str
    headers_path: str
    data_path: str


DELIMITER = ':'


def set_logger():
    logger = logging.getLogger(__name__)
    stream = logging.StreamHandler()
    file = logging.FileHandler('pass_post.txt', encoding='utf8')
    stream.setLevel(logging.INFO)
    file.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream)
    logger.addHandler(file)
    return logger


logger = set_logger()


class FileWithFields:
    def __init__(self, path: str):
        self.path = path

    def dict(self) -> typing.Dict[str, str]:
        with open(self.path, 'r', encoding='cp1251') as f:
            data = f.read()
        split = lambda s: s.split(DELIMITER)
        return dict([
            (split(line)[0], split(line)[1].strip())
            for line in data.split('\n') if line
        ])


def order_pass(form: FormData, session: requests.Session):
    response = session.post(
        form.url,
        headers=FileWithFields(form.headers_path).dict(),
        data=FileWithFields(form.data_path).dict(),
        auth=(config.LOGIN, config.PASSWORD)
    )
    logger.info(30*'-' + form.url + 30*'-')
    logger.info(response.status_code)
    logger.info(response.text)


with requests.Session() as session:
    order_pass(
        FormData(
            url='https://2an.ru/new_order.aspx',
            headers_path='headers.txt',
            data_path='form.txt'
        ),
        session
    )

    url = 'https://2an.ru/orders.aspx'
    response = session.get(url, auth=(config.LOGIN, config.PASSWORD))
    logger.info(30*'-' + url + 30*'-')
    logger.info(response.status_code)
    logger.info(response.text)
