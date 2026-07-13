import logging
import time
from typing import Optional
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import REQUEST_RETRY, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def build_headers(company_name: str = "") -> dict:
    referer = "https://www.cninfo.com.cn/new/disclosure"
    if company_name:
        referer = (
            "https://www.cninfo.com.cn/new/fulltextSearch"
            f"?notautosubmit=&keyWord={quote(company_name)}&searchType=0"
        )

    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.cninfo.com.cn",
        "Referer": referer,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/150.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }


def create_session(company_name: str = "") -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=REQUEST_RETRY,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(build_headers(company_name))
    return session


def post_form(session: requests.Session, url: str, data: dict) -> dict:
    response = session.post(url, data=data, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def sleep_between_requests(seconds: float = 0.5):
    time.sleep(seconds)
