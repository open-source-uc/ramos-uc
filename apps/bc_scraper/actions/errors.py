from datetime import datetime
import json
from django.conf import settings
import logging

log = logging.getLogger("scraper")


def handle(context, err):
    log.error("%s", err)
    log.error("Context: %s", json.dumps(context, indent=2))
