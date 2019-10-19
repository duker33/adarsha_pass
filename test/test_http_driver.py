"""Integration test. Http driver goes to the real IqPark panel."""
import pytest
from datetime import date

from bot import app, drivers


@pytest.mark.skip(reason='Waiting for #7 to enable CI tests')
def test_order():
    pass_ = app.Pass(
        app.Guest('Питонов', 'Амвросий', 'Аристархович'),
        date_=date.today()
    )
    driver = drivers.HTTP()
    driver.order(pass_)
