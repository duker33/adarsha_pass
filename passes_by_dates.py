import random
import typing
from datetime import date
from bot.app import drivers, Admin, Guest, Pass
from time import sleep

DAYS = [
    # 1, 2,
    4, 5, 6, 7, 8, 9,
    11, 12, 13, 14, 15, 16,
    18, 19, 20, 21, 22, 23,
    25, 26, 27, 28, 29, 30,
]


def fetch_guests() -> typing.List[str]:
    with open('../adarsha_november_passes.csv', 'r', encoding='utf8') as f:
        return [fio for fio in f.read().split('\n') if fio]


def gen_passes(guests: typing.List[str]) -> typing.Generator[Pass, None, None]:
    for day in DAYS:
        for guest in guests:
            yield Pass(Guest.from_fio(guest), date(year=2019, month=11, day=day))


def order_bunch(passes: typing.Iterable[Pass]):
    admin = Admin(drivers.HTTP())
    for pass_ in passes:
        # sleep to stabilize somehow IQPark responses
        sleep(random.randint(1, 10) / 200)
        admin.order(pass_)


order_bunch(gen_passes(fetch_guests()))
