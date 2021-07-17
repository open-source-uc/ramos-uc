# BuscaCursosUC Scrapper
Python scripts that retrieve courses data from BuscaCursosUC and Catálogo UC
and save it to a Postgres database.

## How to use
```python main.py <command> [YYYY-S] [...]```

### Available commands
+ `collect` -> Runs a full search in BC and Catalogo. Inserts or updates all BC content. Does NOT delete removed courses.
+ `update` -> Updates data of courses present in simple BC search. Creates a delete log with courses not founded.
+ `delete` -> For every course in the delete log, retries the search in BC and deletes if the course does not exist. The delete log must be cleared manually.
+ `search` -> A course initial must be provided as extra argumemt. Retrives results for that initial in BC.
+ `help` -> Shows available commands and usage format.

## Database Schema
+ courses_course (id, initials, name, credits, req, con, restr, program, school, area, category)
+ courses_section (id, course_id, period, section, nrc, teachers, schedule, format, campus, is_english, is_removable, is_special, available_quota, total_quota)
+ courses_quota (section_id, date, category, quota, banner)
+ courses_fullschedule (section_id, LMWJVS x 12345678)
+ courses_scheduleinfo (section_id, total, ayu, clas, lab, pra, sup, tal, ter, tes)
+ courses_category (id, name)

## BuscaCursos and Catálogo Endpoints
+ Courses main data
  http://buscacursos.uc.cl/?cxml_semestre={PERIOD}&cxml_sigla={SIGLA}
  http://buscacursos.uc.cl/?cxml_semestre={PERIOD}&cxml_nrc={NRC}

+ Quota details
  http://buscacursos.uc.cl/informacionVacReserva.ajax.php?nrc={NRC}&termcode={YEAR}-{SEMESTER}

+ Programs
  http://catalogo.uc.cl/index.php?tmpl=component&view=programa&sigla={SIGLA}

+ Requirements and restrictions
  http://catalogo.uc.cl/index.php?tmpl=component&view=requisitos&sigla=PSI5005


## ```banner```
Scrapes available cupos for all courses in a given YEAR SEMESTER. Accepts a
banner name parameter that adds to the database. Saves the cupos by category
and with a retrieval datetime.
Run ```python banner.py YEAR SEMESTER```.
