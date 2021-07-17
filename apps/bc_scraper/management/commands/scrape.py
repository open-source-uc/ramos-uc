import re
from apps.bc_scraper.actions.search import search
from apps.bc_scraper.actions.collect import collect
from apps.bc_scraper.actions.update import update
from apps.bc_scraper.actions.delete import delete
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = (
        "Scrapes Buscacursos and Catálogo to update database. See docs for more info."
    )

    def add_arguments(self, parser):
        parser.add_argument("action", type=str)
        parser.add_argument("period", type=str)
        parser.add_argument("--initials")

    def handle(self, *args, **options):
        action = options["action"]
        # TODO: Implement banner action
        ACTIONS = ["collect", "update", "delete", "search"]
        if action not in ACTIONS:
            raise CommandError("Invalid action.")

        period = options["period"]
        if not re.match("\d{4}-[012]", period):
            raise CommandError("Period must follow format YYYY-S")

        db_settings = getattr(settings, "DATABASES")["default"]
        settings_dict = {
            "db_host": db_settings["HOST"],
            "db_user": db_settings["USER"],
            "db_passwd": db_settings["PASSWORD"],
            "db_name": db_settings["NAME"],
            "batch_size": getattr(settings, "SCRAPE_BATCH_SIZE"),
        }

        if action == "collect":
            collect(period, settings_dict)
        elif action == "update":
            update(period, settings_dict)
        elif action == "delete":
            delete(settings_dict)
        elif action == "search":
            if not options["initials"]:
                raise CommandError("Must provide initials to search")
            search(options["initials"], period)
