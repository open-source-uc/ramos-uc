import json
import sys
import re
from apps.bc_scraper.actions.search import search
from apps.bc_scraper.actions.collect import collect
from apps.bc_scraper.actions.update import update
from apps.bc_scraper.actions.delete import delete


# Call as "python main.py <ACTION> [PERIOD] [OPTIONS]"
ACTIONS = [
    "collect",  # collect from all BC and Catalogo (update or create). Does not detect deletions.
    "update",  # update existing NRCs with BC data. Log unfounded for deletion.
    "delete",  # review deletions propositions and execute deletion
    "search",  # search initials for debugging and testing
    "help",
]

# Validate call
ACTION = "help"
if len(sys.argv) >= 2 and sys.argv[1] in ACTIONS:
    ACTION = sys.argv[1]

PERIOD = "0000-0"
PERIOD_PROVIDED = False
if len(sys.argv) >= 3 and re.match("\d{4}-[012]", sys.argv[2]):
    PERIOD = sys.argv[2]
    PERIOD_PROVIDED = True

# Load settings
SETTINGS = None
with open("settings.json") as file:
    SETTINGS = json.load(file)

if ACTION == "help":
    print('Call as "python main.py <ACTION> [PERIOD] [OPTIONS]"')
    print("ex: python main.py collect 2021-2")
    print()
    print("Available actions are:")
    print(" ", "\n  ".join(ACTIONS))
    print()
    print("PERIOD must be in the form of YYYY-S")
    exit()

elif ACTION == "delete":
    delete(SETTINGS)

elif not PERIOD_PROVIDED:
    print("Provide PERIOD in the form of YYYY-S")
    exit()

elif ACTION == "collect":
    collect(PERIOD, SETTINGS)

elif ACTION == "update":
    update(PERIOD, SETTINGS)

elif ACTION == "quota":
    print("Not implemented yet, and maybe never. Just run banner.py.")

elif ACTION == "search":
    if len(sys.argv) != 4:
        print("Call: search PERIOD <initials>")
        exit()
    search(sys.argv[3], PERIOD)
