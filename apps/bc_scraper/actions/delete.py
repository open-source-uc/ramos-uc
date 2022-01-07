import requests
import psycopg2
from . import queries as sql
import logging

log = logging.getLogger("scraper")

db_conn, db_cursor = None, None


def open_db_conn(settings):
    global db_conn, db_cursor
    db_conn = psycopg2.connect(
        host=settings["db_host"],
        user=settings["db_user"],
        password=settings["db_passwd"],
        dbname=settings["db_name"],
    )
    db_cursor = db_conn.cursor()
    log.info("DB connection set.")


def delete(settings):
    """Searchs the delete log courses in BC. In the case it does not found
    the course, removes it from DB.
    """
    open_db_conn(settings)

    with open("logs/delete.log") as del_log:
        for line in del_log:
            # line format -> DATE NRC 12345 YYYY-S
            copy = line.strip().split(" NRC ")
            # date = copy[0].strip()
            course = copy[1].split(" ")

            nrc = course[0].strip()
            period = course[1].strip()

            log.info("Searching %s %s", nrc, period)
            resp = requests.get(
                f"http://buscacursos.uc.cl/?cxml_semestre={period}&cxml_nrc={nrc}"
            )

            not_result = "La búsqueda no produjo resultados" in resp.text
            if not_result:
                log.info("No result found. Deleting...")
                try:
                    db_cursor.execute(sql.GET_SECTION_ID_FROM_NRC, (nrc, period))
                    section_id = db_cursor.fetchone()[0]

                    db_cursor.execute(sql.DELETE_FULL_SC, (section_id,))
                    db_cursor.execute(sql.DELETE_INFO_SC, (section_id,))
                    db_cursor.execute(sql.DEL_SECTION_QUOTA, (section_id,))
                    db_cursor.execute(sql.DEL_SECTION, (section_id,))
                    db_conn.commit()
                except:
                    log.warn("Already deleted.")
            else:
                log.warn("Course found. Not deleted.")

    db_cursor.close()
    db_conn.close()
