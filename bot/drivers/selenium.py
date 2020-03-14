"""
Selenium is in reserve now. We are using plain http requests with http driver.

The code below taken from another project.
Need to be adapted in case of start working with it.
"""

from functools import lru_cache
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, ui
from selenium.webdriver.remote.webelement import WebElement
from seleniumrequests import Remote

from bot import config
from . import base


CAPABILITIES = {
    'browserName': 'chrome',
    'chromeOptions': {
        # the rationale for these options: https://bit.ly/2Vo6klZ
        'args': [
            'start-maximized',
            'enable-automation',
            '--disable-infobars',
            '--no-sandbox',
            '--disable-browser-side-navigation',
            # it's for credentials sharing
            '--disable-blink-features=BlockCredentialedSubresources',
        ]
    }
}


class Browser(Remote):
    """"
    Represents selenium microservice.

    It's redundant class. Needs to be removed.
    """

    SELENIUM_URL = config.SELENIUM_SERVER_URL
    # using old styled and unsafe url credentials
    # because of auth alert doesn't work well with Selenium.
    # It hangs at the `selenium.WebDriver.get('https://2an.ru')` call,
    # so `selenium.WebDriver.switch_to.alert` won't help.
    SITE_BASE_URL = f'https://{config.LOGIN}:{config.PASSWORD}@2an.ru'

    def __init__(self, **kwargs):
        super().__init__(
            command_executor=self.SELENIUM_URL,
            desired_capabilities=CAPABILITIES,
            **kwargs
        )
        self.wait = ui.WebDriverWait(self, config.SELENIUM_WAIT_SECONDS)
        self.short_wait = ui.WebDriverWait(self, config.SELENIUM_WAIT_SECONDS // 4)

    def get(self, path: str):
        super().get(urljoin(self.SITE_BASE_URL, path))


class ModalWindow:
    """Annoying modal window with notifications."""

    def __init__(self, browser: Browser):
        self.browser = browser

    @property
    @lru_cache(maxsize=1)
    def element(self) -> WebElement:
        return self.browser.find_element_by_css_selector('#boxes > #dialog')

    def is_displayed(self) -> bool:
        return self.element.is_displayed()

    def close(self):
        button = self.element.find_element_by_class_name('close')
        button.click()
        self.browser.wait.until(EC.invisibility_of_element(button))


class OrderPassPage:
    PATH = '/new_order.aspx'
    INPUT = 'input[name="{}"]'

    def __init__(self, browser: Browser):
        self.browser = browser

    def reload(self):
        self.browser.get(self.PATH)

    def load(self):
        self.reload()

    def fill_input(self, field: str, value: str):
        self.browser.execute_script(
            f'$("{self.INPUT.format(field)}").value = "{value}";'
        )

    def send_form(self):
        button = self.browser.find_element_by_css_selector(
            self.INPUT.format('ctl00$PageContent$btnAddOrder')
        )
        button.click()


class Selenium(base.Driver):
    @property
    @lru_cache(maxsize=1)
    def browser(self):
        return Browser()

    def wait_page_loading(self):
        ui.WebDriverWait(self.browser, 60).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'content')
            )
        )

    def order(self, pass_):
        from time import sleep
        page = OrderPassPage(self.browser)
        page.load()
        modal = ModalWindow(self.browser)
        if modal.is_displayed():
            modal.close()
        sleep(2)
        page.fill_input('ctl00$PageContent$TbxFirstName', pass_.guest.surname)
        page.fill_input('ctl00$PageContent$TbxMiddleName', pass_.guest.name)
        page.fill_input('ctl00$PageContent$TbxSecondName', pass_.guest.patronymic)
        page.fill_input('ctl00$PageContent$HfSelectedDates', f'{pass_.date:%d.%m.%Y}')
        page.fill_input('ctl00$PageContent$CmbPersonType', 'посетитель')
        page.fill_input('ctl00$PageContent$CmbPassType', 'разовый пропуск на посетителя')
        page.send_form()

    def confirm(self, pass_) -> bool:
        raise NotImplementedError()

    def cancel(self, pass_) -> bool:
        raise NotImplementedError()
