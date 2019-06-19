import logging
import requests
import typing

import config

FORM = 'https://2an.ru/new_order.aspx'
DELIMITER = ':'


def set_logger():
    logger = logging.getLogger(__name__)
    stream = logging.StreamHandler()
    file = logging.FileHandler('pass_post.log', encoding='utf8')
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


def order_pass():
    response = requests.post(
        FORM,
        headers=FileWithFields('headers.txt').dict(),
        data=FileWithFields('form.txt').dict(),
        auth=(config.LOGIN, config.PASSWORD)
    )
    logger.info(response.status_code)
    logger.info(response.text)
    logger.info(
        # TODO - doc how IQparks app works
        'The pass created successfully!'
        if 'theForm.submit();' in response.text
        else 'The pass creating failed!'
    )


order_pass()
