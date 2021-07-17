import psycopg2
import json


# SETUP
settings = None
with open("settings.json") as file:
    settings = json.load(file)
BATCH_SIZE = settings["batch_size"]

# START
db_conn = psycopg2.connect(
    host=settings["db_host"],
    user=settings["db_user"],
    password=settings["db_passwd"],
    dbname=settings["db_name"],
)
db_cursor = db_conn.cursor()

# Courses
db_cursor.execute(f"SELECT COUNT(*) FROM courses_course;")
total = int(db_cursor.fetchone()[0])
print(total, "courses found.")

output = open("courses.json", "w")
offset = 0
while offset < total:
    # Process by batches
    print("Collecting from", offset, "to", offset + BATCH_SIZE, "of", total)
    db_cursor.execute(
        f"SELECT id, initials, name, req, program FROM courses_course ORDER BY id LIMIT {BATCH_SIZE} OFFSET {offset};"
    )
    cursos = db_cursor.fetchall()
    for curso in cursos:
        program = (
            curso[4]
            .replace("\\", "")
            .replace("/", "\\/")
            .replace("\t", "\\t")
            .replace("\b", "\\b")
            .replace("\f", "\\f")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "")
            .replace("\u001f", "")
        )
        name = curso[2].replace("\\", "")
        output.write('{{"index":{{"_id":"{}"}}}}\n'.format(curso[0]))
        output.write(
            f'{{"initials":"{curso[1]}","name":"{name}","req":"{curso[3]}","program":"{program}","teachers":[]}}\n'
        )

    offset += BATCH_SIZE

# Teachers
db_cursor.execute(f"SELECT COUNT(*) FROM courses_section;")
total = int(db_cursor.fetchone()[0])
print(total, "sections found.")

offset = 0
while offset < total:
    # Process by batches
    print("Collecting from", offset, "to", offset + BATCH_SIZE, "of", total)
    db_cursor.execute(
        f"SELECT course_id, teachers FROM courses_section ORDER BY id LIMIT {BATCH_SIZE} OFFSET {offset};"
    )
    cursos = db_cursor.fetchall()
    for curso in cursos:
        teachers = curso[1].replace(",", " ")
        output.write('{{"update":{{"_id":"{}"}}}}\n'.format(curso[0]))
        output.write(
            f'{{"script":{{"source":"ctx._source.teachers.add(params.a)","params":{{"a":"{teachers}"}} }} }}\n'
        )

    offset += BATCH_SIZE
output.close()

db_cursor.close()
db_conn.close()
