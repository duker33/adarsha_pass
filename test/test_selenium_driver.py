import pytest
from datetime import date

from bot import app, drivers


@pytest.mark.skip(reason='Selenium driver is in reserve now')
def test_order():
    pass_ = app.Pass(
        app.Guest('Питонов', 'Амвросий', 'Аристархович'),
        date_=date.today()
    )
    driver = drivers.Selenium()
    driver.order(pass_)
