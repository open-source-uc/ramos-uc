from background_task import background
from .actions.collect import collect
from .actions.update import update
from .actions.delete import delete
from .actions.banner import banner
from django.conf import settings


def get_scraper_settings():
    db_settings = getattr(settings, "DATABASES")["default"]
    settings_dict = {
        "db_host": db_settings["HOST"],
        "db_user": db_settings["USER"],
        "db_passwd": db_settings["PASSWORD"],
        "db_name": db_settings["NAME"],
        "batch_size": getattr(settings, "SCRAPE_BATCH_SIZE"),
        "buscacursos_url": getattr(settings, "BUSCACURSOS_URL"),
        "catalogo_url": getattr(settings, "CATALOGO_URL"),
    }
    return settings_dict


@background
def collect_task(period):
    collect(period, get_scraper_settings())


@background
def update_task(period):
    update(period, get_scraper_settings())


@background
def delete_task():
    delete(get_scraper_settings())


@background
def banner_task(period, banner_name=None):
    if banner_name is None:
        banner(period, get_scraper_settings())
    else:
        banner(period, get_scraper_settings(), banner_name)
