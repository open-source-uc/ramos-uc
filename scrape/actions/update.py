from datetime import datetime
from scraper.search import bc_search
from .schedule import process_schedule
from .errors import handle
import psycopg2
from . import queries as sql


# DB
db_conn, db_cursor = None, None
def open_db_conn(settings):
    global db_conn, db_cursor
    try:
        db_conn = psycopg2.connect(
            host=settings['db_host'],
            user=settings['db_user'],
            password=settings['db_passwd'],
            dbname=settings['db_name']
        )
        db_cursor = db_conn.cursor()
    except Exception as err:
        print('DB Error:', err)
        exit()
    print('DB connection set.')


procesed_initials = {}

'''For a list of courses, process and gathers all related data and commits to DB.
'''
def _process_course(c, section_id):
    try:
        # Update Course name, credits, area and category
        if c['initials'] not in procesed_initials:
            db_cursor.execute(sql.HALF_UPDATE_COURSE, (
                c['name'], c['credits'], c['area'], c['category'], c['initials']
            ))
            db_conn.commit()
            procesed_initials[c['initials']] = True

        # Process Section
        insert_full_sc_query, insert_info_sc_query = process_schedule(c['schedule'])

        # Save Section
        db_cursor.execute(sql.UPDATE_SECTION, (
            c['teachers'], c['schedule'], c['format'], c['campus'], c['is_english'],
            c['is_removable'], c['is_special'], c['available_quota'], c['total_quota'], section_id
        ))

        # Save schedules
        db_cursor.execute(sql.DELETE_FULL_SC, (section_id,))
        db_cursor.execute(sql.DELETE_INFO_SC, (section_id,))
        db_cursor.execute(insert_full_sc_query, (section_id,))
        db_cursor.execute(insert_info_sc_query, (section_id,))

        # Commit to DB
        db_conn.commit()
        print('Procesed: NRC', c['nrc'], c['name'])
    
    except Exception as err:
        handle(c, err)


'''Iterates a search throw all BC and process all courses and sections founded.
'''
def update(period, settings):
    open_db_conn(settings)
    BATCH_SIZE = settings['batch_size']

    db_cursor.execute(sql.COUNT_SECTIONS, (period,))
    total = int(db_cursor.fetchone()[0])
    deleted = 0

    offset = 0
    while offset < total:
        # Process by batches
        print('Updating from', offset, 'to', offset + BATCH_SIZE, 'of', total)
        db_cursor.execute(sql.GET_NRC_BATCH, (period, BATCH_SIZE, offset))
        rows = db_cursor.fetchall()
        for row in rows:
            nrc = row[0]
            section_id = row[1]
            courses = bc_search(nrc, period, nrc=True)

            # Check section existance in BC
            if not len(courses):
                deleted += 1
                print(nrc, 'give no results. Added to delete list.')
                with open('logs/delete.log', 'a+') as log:
                    log.write(str(datetime.now()) + ' NRC ' + nrc + ' ' + period + '\n')

            else:
                _process_course(courses[0], section_id)
        
        offset += BATCH_SIZE

    db_cursor.close()
    db_conn.close()

    print('Courses deleted:', str(deleted))