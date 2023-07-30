import requests
import logging
from time import sleep

log = logging.getLogger("scraper")


def get_text(query):
    tries = 10
    while tries > 0:
        try:
            rq = requests.get(query, timeout=5)
            rq.raise_for_status()
            text = rq.text
            return text
        except Exception:
            log.warn("GET %s failed, retrying...", query)
            tries -= 1
            if tries == 0:
                raise
            sleep(1)
