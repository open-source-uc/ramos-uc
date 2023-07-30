import json
import logging

log = logging.getLogger("scraper")


def handle(context, err):
    log.error("%s", err)
    if isinstance(err, Exception) and err.__traceback__:
        filename = err.__traceback__.tb_frame.f_code.co_filename
        line_number = err.__traceback__.tb_lineno
        log.error("Error at %s:%s", filename, line_number)
    log.error("Context: %s", json.dumps(context, indent=2))
