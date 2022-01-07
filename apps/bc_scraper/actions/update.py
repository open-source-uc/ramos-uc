from datetime import datetime
from ..scraper.search import bc_search
from .schedule import process_schedule
from .errors import handle
import psycopg2
from . import queries as sql
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


procesed_initials = {}


def _process_course(c, section_id):
    """For a list of courses, process and gathers all related data and commits to DB."""
    try:
        # Update Course name, credits, area and category
        if c["initials"] not in procesed_initials:
            db_cursor.execute(
                sql.HALF_UPDATE_COURSE,
                (c["name"], c["credits"], c["area"], c["category"], c["initials"]),
            )
            db_conn.commit()
            procesed_initials[c["initials"]] = True

        # Process Section
        insert_full_sc_query, insert_info_sc_query = process_schedule(c["schedule"])

        # Save Section
        db_cursor.execute(
            sql.UPDATE_SECTION,
            (
                c["teachers"],
                c["schedule"],
                c["format"],
                c["campus"],
                c["is_english"],
                c["is_removable"],
                c["is_special"],
                c["available_quota"],
                c["total_quota"],
                section_id,
            ),
        )

        # Save schedules
        db_cursor.execute(sql.DELETE_FULL_SC, (section_id,))
        db_cursor.execute(sql.DELETE_INFO_SC, (section_id,))
        db_cursor.execute(insert_full_sc_query, (section_id,))
        db_cursor.execute(insert_info_sc_query, (section_id,))

        # Commit to DB
        db_conn.commit()
        log.info("Procesed: NRC %s %s", c["nrc"], c["name"])

    except Exception as err:
        handle(c, err)


def update(period, settings):
    """Iterates a search throw all BC and process all courses and sections found."""
    open_db_conn(settings)
    BATCH_SIZE = settings["batch_size"]

    db_cursor.execute(sql.COUNT_SECTIONS, (period,))
    total = int(db_cursor.fetchone()[0])
    deleted = 0

    offset = 0
    while offset < total:
        # Process by batches
        log.info("Updating from %s to % of %s", offset, offset + BATCH_SIZE, total)
        db_cursor.execute(sql.GET_NRC_BATCH, (period, BATCH_SIZE, offset))
        rows = db_cursor.fetchall()
        for row in rows:
            nrc = row[0]
            section_id = row[1]
            courses = bc_search(nrc, period, nrc=True)

            # Check section existance in BC
            if not len(courses):
                deleted += 1
                log.info("%s give no results. Added to delete list.", nrc)
                with open("logs/delete.log", "a+") as del_log:
                    del_log.write(
                        str(datetime.now()) + " NRC " + nrc + " " + period + "\n"
                    )

            else:
                _process_course(courses[0], section_id)

        offset += BATCH_SIZE

    db_cursor.close()
    db_conn.close()

    log.info("Courses deleted: %s", str(deleted))
