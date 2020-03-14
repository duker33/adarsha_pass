"""Integration test. Http driver goes to the real IqPark panel."""
from datetime import date

from bot import app, drivers


def test_order():
    pass_ = app.Pass(
        app.Guest('Питонов', 'Амвросий', 'Аристархович'),
        date_=date.today()
    )
    driver = drivers.HTTP()
    driver.order(pass_)
    assert driver.confirm(pass_)
