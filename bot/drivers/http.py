"""Interacts with IqPark panel with the plain http."""

import requests
from functools import lru_cache

from bot import config
from . import base, ssl_adapter


def pass_fields(surname: str, name: str, patronymic: str, date_: str):
    """
    :param date_: '01.01.1970' for example.
    """
    return {
        'ctl00$PageContent$TbxFirstName': surname,
        'ctl00$PageContent$TbxMiddleName': name,
        'ctl00$PageContent$TbxSecondName': patronymic,
        'ctl00$PageContent$HfSelectedDates': date_,
    }


class HTTP(base.Driver):
    @property
    @lru_cache(maxsize=1)
    def session(self) -> requests.Session:
        session = requests.Session()
        session.mount(config.IQPARK_URL, ssl_adapter.AncientCiphersAdapter())
        return session

    def order(self, pass_):
        response = self.session.post(
            config.IQPARK_ORDER_URL,
            data={**pass_.as_form_data(), **DATA},
            auth=(config.LOGIN, config.PASSWORD)
        )
        if response.status_code == 200:
            # waiting #6 to be logged
            pass
        else:
            # waiting #6 to be logged
            pass

    def confirm(self, pass_) -> bool:
        # @todo #1:120m  Implement drivers.http.confirm method.
        #  And invoke it in existing tests.
        raise NotImplementedError()

    def cancel(self, pass_):
        # @todo #1:120m  Implement drivers.http.cancel method.
        #  And invoke it in existing tests.
        #  It's not trivial tasks since http request building is required.
        pass


# IQPark's form data
DATA = {
    **config.FORM_PRIVATE_FIELDS,
    'DXScript': '1_49,2_15,2_14,2_13,2_8,1_46,1_29,2_11,1_42,2_7',
    '__EVENTARGUMENT': '',
    '__EVENTTARGET': '',
    '__SCROLLPOSITIONX': '0',
    '__SCROLLPOSITIONY': '0',
    '__VIEWSTATE': '',
    '__VIEWSTATEGENERATOR': '9B8E9023',
    'ctl00$PageContent$CmbAccessType': '- категория отсутствует -',
    'ctl00$PageContent$CmbAccessType$DDD$L': '1012',
    'ctl00$PageContent$CmbCarNumberType': 'Российский',
    'ctl00$PageContent$CmbCarNumberType$DDD$L': 'RUS',
    'ctl00$PageContent$CmbCarType': 'Легковой',
    'ctl00$PageContent$CmbCarType$DDD$L': '2',
    'ctl00$PageContent$CmbCarWeight': '-- Выберите --',
    'ctl00$PageContent$CmbCarWeight$DDD$L': '0',
    'ctl00$PageContent$CmbComplexSelect': 'Бизнес-квартал IQ-Park',
    'ctl00$PageContent$CmbComplexSelect$DDD$L': '29',
    'ctl00$PageContent$CmbDocType': '---выберите---',
    'ctl00$PageContent$CmbDocType$DDD$L': '0',
    'ctl00$PageContent$CmbMark': '- нет -',
    'ctl00$PageContent$CmbMark$DDD$L': '0',
    'ctl00$PageContent$CmbPassType': 'разовый пропуск на посетителя',
    'ctl00$PageContent$CmbPassType$DDD$L': '2',
    'ctl00$PageContent$CmbPersonType': 'посетитель',
    'ctl00$PageContent$CmbPersonType$DDD$L': '2',
    'ctl00$PageContent$DbxBirthDate': '',
    'ctl00$PageContent$DbxBirthDate$DDD$C': '06/06/2019',
    'ctl00$PageContent$FilePhoto$ctl00': '',
    'ctl00$PageContent$FilePhoto$ctl02': '',
    'ctl00$PageContent$FileScan$ctl00': '',
    'ctl00$PageContent$FileScan$ctl02': '',
    'ctl00$PageContent$HfPassType': '2',
    'ctl00$PageContent$HfUserComplex': '29',
    'ctl00$PageContent$HfUserEppCustomer': '0',
    'ctl00$PageContent$TbxAccessDescription': '',
    'ctl00$PageContent$TbxCarMark': '',
    'ctl00$PageContent$TbxCarNumber': '',
    'ctl00$PageContent$TbxDocAddress': '',
    'ctl00$PageContent$TbxDocDate': '',
    'ctl00$PageContent$TbxDocDate$DDD$C': '06/06/2019',
    'ctl00$PageContent$TbxDocNumber': '',
    'ctl00$PageContent$TbxDocOrg': '',
    'ctl00$PageContent$TbxDocSeriya': '',
    'ctl00$PageContent$TbxMarkDescription': '',
    'ctl00$PageContent$TbxWay': '',
    'ctl00$PageContent$btnSave': '',
    'ctl00_PageContent_CmbAccessType_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbAccessType_DDD_LCustomCallback': '',
    'ctl00_PageContent_CmbAccessType_DDD_LDeletedItems': '',
    'ctl00_PageContent_CmbAccessType_DDD_LInsertedItems': '',
    'ctl00_PageContent_CmbAccessType_VI': '1012',
    'ctl00_PageContent_CmbCarNumberType_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbCarNumberType_VI': 'RUS',
    'ctl00_PageContent_CmbCarType_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbCarType_DDD_LCustomCallback': '',
    'ctl00_PageContent_CmbCarType_DDD_LDeletedItems': '',
    'ctl00_PageContent_CmbCarType_DDD_LInsertedItems': '',
    'ctl00_PageContent_CmbCarType_VI': '2',
    'ctl00_PageContent_CmbCarWeight_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbCarWeight_VI': '0',
    'ctl00_PageContent_CmbComplexSelect_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbComplexSelect_VI': '29',
    'ctl00_PageContent_CmbDocType_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbDocType_VI': '0',
    'ctl00_PageContent_CmbMark_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbMark_VI': '0',
    'ctl00_PageContent_CmbPassType_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbPassType_DDD_LCustomCallback': '',
    'ctl00_PageContent_CmbPassType_DDD_LDeletedItems': '',
    'ctl00_PageContent_CmbPassType_DDD_LInsertedItems': '',
    'ctl00_PageContent_CmbPassType_VI': '2',
    'ctl00_PageContent_CmbPersonType_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_CmbPersonType_VI': '2',
    'ctl00_PageContent_CropImg_url': '',
    'ctl00_PageContent_DbxBirthDate_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_DbxBirthDate_DDD_C_FNPWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_DbxBirthDate_Raw': 'N',
    'ctl00_PageContent_FilePhoto_ClientState': '',
    'ctl00_PageContent_FileScan_ClientState': '',
    'ctl00_PageContent_TbxDocDate_DDDWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_TbxDocDate_DDD_C_FNPWS': '0:0:-1:0:0:0:0:0',
    'ctl00_PageContent_TbxDocDate_Raw': 'N',
}
