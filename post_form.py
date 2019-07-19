import logging
import requests
import typing

import config

FORM = 'https://2an.ru/new_order.aspx'
DELIMITER = ': '


def set_logger():
    logger = logging.getLogger(__name__)
    stream = logging.StreamHandler()
    file = logging.FileHandler('out.txt', mode='a', encoding='utf8')
    stream.setLevel(logging.INFO)
    file.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    # logger.addHandler(stream)
    logger.addHandler(file)
    return logger


logger = set_logger()


class FileWithFields:
    def __init__(self, path: str):
        self.path = path

    def dict(self) -> typing.Dict[str, str]:
        with open(self.path, 'r', encoding='cp1251') as f:
            data = f.read()
        return dict([tuple(line.split(DELIMITER)) for line in data.split('\n') if line])


def order_pass():
    response = requests.post(
        FORM,
        headers=FileWithFields('headers.txt').dict(),
        data=FileWithFields('form.txt').dict(),
        auth=(config.LOGIN, config.PASSWORD)
    )
    logger.info(response.status_code)
    logger.info(response.text)


def test_logger():
    response = requests.get('https://ya.ru')
    logger.info(response.status_code)
    logger.info(response.text)


# order_pass()
test_logger()
