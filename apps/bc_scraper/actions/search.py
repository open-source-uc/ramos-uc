from ..scraper.search import bc_search
from .errors import handle
from ..exceptions.exceptions import EmptyResponseError


def search(initials, period):
    """Search for a initial and period in BuscaCursosUC.
    Prints the results. Useful for testing only.
    """
    print("Searching in BC:", initials)
    try:
        courses = bc_search(initials, period)
        for c in courses:
            print(c["initials"], c["section"], c["name"], "-", c["teachers"])
        if len(courses) >= 50:
            print("> Some results may have been truncated.")
    except EmptyResponseError as e_err:
        handle({"initials": initials, "period": period, "url": e_err.url}, e_err)
    except Exception as err:
        handle({"initials": initials, "period": period}, err)
