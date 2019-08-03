import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

import config

# taken from
# https://ssl-config.mozilla.org/#server=nginx&server-version=1.17.0&config=old
ANCIENT_CIPHERS = (
    'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256'
    ':ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384'
    ':ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305'
    ':DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384'
    ':DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-SHA256'
    ':ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA'
    ':ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA'
    ':ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256'
    ':AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256'
    ':AES128-SHA:AES256-SHA:DES-CBC3-SHA'
)


# Taken decision from
# https://stackoverflow.com/questions/40373115/how-to-select-specific-the-cipher-while-sending-request-via-python-request-modul
class AncientCiphersAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=ANCIENT_CIPHERS)
        kwargs['ssl_context'] = context
        return super(AncientCiphersAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=ANCIENT_CIPHERS)
        kwargs['ssl_context'] = context
        return super(AncientCiphersAdapter, self).proxy_manager_for(*args, **kwargs)

# TODO - move it to some integration tests
if __name__ == '__main__':
    s = requests.Session()
    s.mount('https://2an.ru', AncientCiphersAdapter())
    assert 200 == s.get(
        'https://2an.ru/new_order.aspx',
        auth=(config.LOGIN, config.PASSWORD)
    ).status_code
