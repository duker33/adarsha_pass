import random
import typing
from datetime import date
from bot.app import drivers, Admin, Guest, Pass
from time import sleep

DAYS = [
    2, 3, 4, 6, 7, 8, 9, 10, 11, 
    13, 14, 15, 16, 17, 18, 
    20, 21, 22, 23, 24, 25, 
    27, 28, 29, 30, 31
]


def fetch_guests() -> typing.List[str]:
    with open('~/adarsha_passes_jan.csv', 'r', encoding='utf8') as f:
        return [fio for fio in f.read().split('\n') if fio]


def gen_passes(guests: typing.List[str]) -> typing.Generator[Pass, None, None]:
    for day in DAYS:
        for guest in guests:
            yield Pass(Guest.from_fio(guest), date(year=2020, month=1, day=day))


def order_bunch(passes: typing.Iterable[Pass]):
    driver = drivers.HTTP()
    for pass_ in passes:
        # sleep to stabilize somehow IQPark responses
        sleep(random.randint(1, 10) / 200)
        print('order pass', pass_)
        driver.order(pass_)


order_bunch(gen_passes(fetch_guests()))
