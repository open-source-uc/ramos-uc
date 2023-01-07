import psycopg2
from ..scraper.request import get_text
from datetime import datetime
from time import sleep
from .errors import handle
from ..scraper.banner import BannerParser, BannerBCParser
import logging

log = logging.getLogger("scraper")

# DB
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


def banner(period, settings, banner="0"):
    """Collects available quota for all sections of period."""
    open_db_conn(settings)

    BATCH_SIZE = settings["batch_size"]
    BUSCACURSOS_URL = settings["buscacursos_url"]
    INSERT = f"INSERT INTO courses_quota (section_id, date, category, quota, banner) VALUES (%s, %s, %s, %s, '{banner}');"
    UPDATE = "UPDATE courses_section SET available_quota=%s WHERE id=%s;"

    db_cursor.execute(
        f"SELECT COUNT(*) FROM courses_section WHERE period = '{period}';"
    )
    total = int(db_cursor.fetchone()[0])
    log.info("%s courses found.", total)

    offset = 0
    parser = BannerParser()
    parser_bc = BannerBCParser()
    while offset < total:
        # Process by batches
        log.info("Collecting from %s to %s of %s", offset, offset + BATCH_SIZE, total)
        try:
            db_cursor.execute(
                f"SELECT id, nrc FROM courses_section WHERE period = '{period}' ORDER BY id LIMIT {BATCH_SIZE} OFFSET {offset};"
            )
            cursos = db_cursor.fetchall()
            for curso in cursos:
                id = int(curso[0])
                nrc = curso[1]
                query = f"{BUSCACURSOS_URL}/informacionVacReserva.ajax.php?nrc={nrc}&termcode={period}"
                text = get_text(query)

                date = str(datetime.now())
                cupos_dict = parser.process(text)
                if not len(cupos_dict):
                    # Solo vacantes libres, buscar en página principal
                    query = f"{BUSCACURSOS_URL}/?cxml_semestre={period}&cxml_nrc={nrc}"
                    text = get_text(query)
                    cupos_dict = {"Total": parser_bc.process(text)}

                values = []
                free_quota = 0
                for categoria, cupos in cupos_dict.items():
                    values.append((id, date, categoria, cupos))
                    free_quota += cupos
                if not len(values):
                    raise Exception("Nothing scrapped.")
                db_cursor.executemany(INSERT, values)
                db_cursor.execute(UPDATE, (str(free_quota), id))
                db_conn.commit()
                log.info("%s id scrapped: %s", db_cursor.rowcount, id)

        except BrokenPipeError:
            db_conn.close()
            open_db_conn(settings)
            sleep(5)
            continue

        except Exception as err:
            handle({"id": id}, err)

        offset += BATCH_SIZE
        sleep(1.5)

    db_cursor.close()
    db_conn.close()
