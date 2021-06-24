from scraper.search import bc_search
from scraper.programs import get_program
from scraper.requirements import get_requirements
import psycopg2
from . import queries as sql
from .schedule import process_schedule
from .errors import handle


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


# Global procesed courses and sections
procesed_initials = {}
procesed_nrcs = {}
new_sections = 0
new_courses = 0

'''For a list of courses, process and gathers all related data and commits to DB.
'''
def _process_courses(courses, period):
    global procesed_initials, procesed_nrcs
    global new_courses, new_sections
    for c in courses:
        # Skip recently procesed sections
        if c['nrc'] in procesed_nrcs:
            continue

        # Mark as procesed inmediatly to avoid repeating errors
        procesed_nrcs[c['nrc']] = True

        try:
            # Save Course if needed
            if c['initials'] not in procesed_initials:
                # Get Course related data
                program = get_program(c['initials'])
                req, con, restr = get_requirements(c['initials'])

                # Get course id from DB
                db_cursor.execute(sql.GET_COURSE_ID, (c['initials'],))
                course_id = db_cursor.fetchone()

                # Save Course
                if course_id is None:
                    db_cursor.execute(sql.CREATE_COURSE, (
                        c['initials'], c['name'], c['credits'], req, con, restr, program,
                        c['school'], c['area'], c['category']
                    ))
                    course_id = db_cursor.fetchone()[0]
                    new_courses += 1
                else:
                    course_id = course_id[0]
                    db_cursor.execute(sql.UPDATE_COURSE, (
                        c['name'], c['credits'], req, con, restr, program, c['area'],
                        c['category'], c['initials']
                    ))

                db_conn.commit()
                procesed_initials[c['initials']] = True

            # Process Section
            insert_full_sc_query, insert_info_sc_query = process_schedule(c['schedule'])

            # Get section id from DB
            db_cursor.execute(sql.GET_SECTION_ID, (c['initials'], c['section'], period))
            section_id = db_cursor.fetchone()

            # Save Section
            if section_id is None:
                db_cursor.execute(sql.CREATE_SECTION, (
                    course_id, period, c['section'], c['nrc'], c['teachers'], c['schedule'],
                    c['format'], c['campus'], c['is_english'], c['is_removable'],
                    c['is_special'], c['available_quota'], c['total_quota']
                ))
                section_id = db_cursor.fetchone()[0]
                new_sections += 1
            else:
                section_id = section_id[0]
                db_cursor.execute(sql.UPDATE_SECTION, (
                    c['teachers'], c['schedule'], c['format'], c['campus'], c['is_english'],
                    c['is_removable'], c['is_special'], c['available_quota'], c['total_quota'],
                    section_id
                ))

            # Save schedules
            db_cursor.execute(sql.DELETE_FULL_SC, (section_id,))
            db_cursor.execute(sql.DELETE_INFO_SC, (section_id,))
            db_cursor.execute(insert_full_sc_query, (section_id,))
            db_cursor.execute(insert_info_sc_query, (section_id,))

            # Commit to DB
            db_conn.commit()
            print('Procesed:', c['initials'] + '-' + str(c['section']), c['name'])

        except Exception as err:
            handle(c, err)


'''Iterates a search throw all BC and process all courses and sections founded.
'''
def collect(period, settings):
    open_db_conn(settings)

    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for l1 in LETTERS:
        comb = l1
        print('Searching', comb)
        courses = bc_search(comb, period)
        _process_courses(courses, period)
        if len(courses) < 50:
            continue

        for l2 in LETTERS:
            comb = l1 + l2
            print('Searching', comb)
            courses = bc_search(comb, period)
            _process_courses(courses, period)
            if len(courses) < 50:
                continue

            for l3 in LETTERS:
                comb = l1 + l2 + l3
                print('Searching', comb)
                courses = bc_search(comb, period)
                _process_courses(courses, period)
                if len(courses) < 50:
                    continue

                for n1 in '0123456789':
                    comb = l1 + l2 + l3 + n1
                    print('Searching', comb)
                    courses = bc_search(comb, period)
                    _process_courses(courses, period)
                    if len(courses) < 50:
                        continue

                    for n2 in '0123456789':
                        comb = l1 + l2 + l3 + n1 + n2
                        print('Searching', comb)
                        courses = bc_search(comb, period)
                        _process_courses(courses, period)

    db_cursor.close()
    db_conn.close()

    global procesed_nrcs, procesed_initials
    global new_sections, new_courses
    print()
    print('New courses:', new_courses)
    print('New sections:', new_sections)
    print('Total courses:', len(procesed_initials))
    print('Total sections:', len(procesed_nrcs))
