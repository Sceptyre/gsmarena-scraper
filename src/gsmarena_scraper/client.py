from requests import Session
from os import path

from .classes import GSMArenaPhone, GSMArenaPhonesList

class GSMArenaClient(Session):
    _base_url: str

    def __init__(self) -> None:
        super().__init__()
        self._base_url = "https://gsmarena.com/"
        self.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": self._base_url
        })

    def _build_path(self, endpoint: str) -> str:
        return path.join(self._base_url, endpoint)
    
    def list_phones(self) -> GSMArenaPhonesList:
        res = self.get(self._build_path(
            "sitemap-phones.xml"
        ))
        res.raise_for_status()

        return GSMArenaPhonesList.from_sitemap_xml(res.content)

    def get_phone_by_id(self, id: str):
        res = self.get(self._build_path(
            f"_-{id}.php"
        ))
        res.raise_for_status()

        return GSMArenaPhone.from_html_response(res.content)

    