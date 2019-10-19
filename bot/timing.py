"""
Hides the complex algorithm to pass order.
"""
import typing
from datetime import datetime


class WrongWeekError(Exception):
    pass


class BaseDateTime:

    def __init__(self, datetime_: datetime):
        self.datetime = datetime_


class Week(BaseDateTime):
    # keys are in datetime.isoweekday format
    DAYS = {1: 'MO', 2: 'TU', 3: 'WD', 4: 'TH', 5: 'FR', 6: 'ST', 7: 'SU'}

    def today(self) -> str:
        return self.DAYS[self.datetime.isoweekday()]

    def days(self, days: typing.List[str]) -> typing.List[str]:
        wrong_days = set(days) - set(self.DAYS.values())
        if wrong_days:
            raise WrongWeekError(
                f'{wrong_days} are not week days!'
                f' Possible week days list: {self.DAYS.values()}'
            )
        return days


class PassTiming:
    # TODO - add typing for pass
    def __init__(self, pass_):
        self.pass_ = pass_

    def calc(self) -> [bool, str]:
        pass

# Input: date="01.08.2019", question="before this WD 22:00 of after?"
# "before this WD 22:00 of after?" ->
# DateTime.from_string(given) < DateTime(week=Week.current())
