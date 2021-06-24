# (initials, )
GET_COURSE_ID = 'SELECT id FROM courses_course WHERE initials= %s;'

# (initials, section, period)
GET_SECTION_ID = 'SELECT courses_section.id FROM courses_section, courses_course ' +\
            'WHERE courses_course.initials= %s AND courses_section.section = %s ' +\
            'AND courses_section.period= %s AND courses_section.course_id = courses_course.id;'

# (initials, name, credits, req, con, restr, program, school, area, category)
CREATE_COURSE = 'INSERT INTO courses_course (initials, name, credits, req, con, restr, program, school, area, category) ' +\
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'

# (course_id, period, section, nrc, teachers, schedule, format, campus, is_english, is_removable, is_special, available_quota, total_quota)
CREATE_SECTION = 'INSERT INTO courses_section (course_id, period, section, nrc, teachers, ' +\
            'schedule, format, campus, is_english, is_removable, is_special, available_quota, total_quota) ' +\
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'

# (name, credits, req, con, restr, program, area, category, initials)
UPDATE_COURSE = 'UPDATE courses_course SET name=%s, credits=%s, req=%s, con=%s, restr=%s, program=%s, area=%s, category=%s ' +\
            'WHERE initials=%s;'

# (name, credits, area, category, initials)
HALF_UPDATE_COURSE = 'UPDATE courses_course SET name=%s, credits=%s, area=%s, category=%s ' +\
            'WHERE initials=%s;'

# (teachers, schedule, format, campus, is_english, is_removable, is_special, available_quota, total_quota, section_id)
UPDATE_SECTION = 'UPDATE courses_section SET teachers=%s, schedule=%s, format=%s, campus=%s, is_english=%s, ' +\
            'is_removable=%s, is_special=%s, available_quota=%s, total_quota=%s ' +\
            'WHERE id=%s;'

# (id,)
DELETE_FULL_SC = 'DELETE FROM courses_fullschedule WHERE section_id=%s;'
DELETE_INFO_SC = 'DELETE FROM courses_scheduleinfo WHERE section_id=%s;'

# (period,)
COUNT_SECTIONS = 'SELECT COUNT(*) FROM courses_section WHERE period=%s;'

# (period, batch_size, offset)
GET_NRC_BATCH = 'SELECT nrc, id FROM courses_section WHERE period=%s ORDER BY id LIMIT %s OFFSET %s;'

# (nrc, period)
GET_SECTION_ID_FROM_NRC = 'SELECT id FROM courses_section WHERE nrc=%s AND period=%s;'

# (id,)
DEL_SECTION = 'DELETE FROM courses_section WHERE id=%s;'
DEL_SECTION_QUOTA = 'DELETE FROM courses_quota WHERE section_id=%s;'
