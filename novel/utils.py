import mechanicalsoup

from typing import Optional, Text, Tuple
from mechanicalsoup import StatefulBrowser
import requests
from . import logger

from config import USER_AGENT

REQUESTS_COMMON_EXCEPTIONS = (
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.SSLError
)

def browser_open(
        url: Text,
        user_agent: Optional[Text] = USER_AGENT,
        timeout: Optional[Tuple] = (10, 60),
        soup: Optional = None,
    ) -> None:
    browser = StatefulBrowser(
        user_agent=user_agent,
        soup_config={"feature": ""},
    )
    try:
        browser.open(url, timeout=timeout)
    except REQUESTS_COMMON_EXCEPTIONS as e:
        logger.error()
    except Exception as e:
        logger.error()
    else:
        soup = browser.page
    finally:
        browser.close()
    return soup
