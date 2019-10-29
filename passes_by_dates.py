import typing
from datetime import date
from bot.app import Admin, Guest, Pass

DAYS = [
    1, 2,
    4, 5, 6, 7, 8, 9,
    11, 12, 13, 14, 15, 16,
    18, 19, 20, 21, 22, 23,
    25, 26, 27, 28, 29, 30,
]


def fetch_guests() -> typing.List[str]:
    with open('../adarsha_november_passes.csv', 'r', encoding='utf8') as f:
        return [fio for fio in f.read().split('\n') if fio]


def gen_passes() -> typing.Generator[Pass, None, None]:
    guests = fetch_guests()
    for day in DAYS:
        for guest in guests:
            yield Pass(Guest.from_fio(guest), date(year=2019, month=11, day=day))


len(list(iter(gen_passes())))
