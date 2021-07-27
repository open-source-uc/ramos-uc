from datetime import datetime
import json
from django.conf import settings


def handle(context, err):
    print("ERROR:", err)
    with open(getattr(settings, "SCRAPE_LOG"), "a+") as log:
        log.write(str(datetime.now()) + " Error: " + str(err) + "\n")
        log.write("Context: " + json.dumps(context, indent=4) + "\n")
