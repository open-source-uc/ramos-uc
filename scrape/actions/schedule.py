from copy import copy


DEFAULT_SCHEDULE = {}
for day in "lmwjvs":
    for mod in "12345678":
        DEFAULT_SCHEDULE[day + mod] = "'FREE'"


def process_schedule(text_sc):
    """For a given schedule text in BC format, returns the SQL queries for inserting
    the full schedule and schedule info. Those queries have to format ID.
    """
    ### Full Schedule
    data = text_sc.split("\nROW: ")[1:]
    # data rows -> day-day:module,module <> type <> room <><>
    schedule = copy(DEFAULT_SCHEDULE)
    for row in data:
        row = row.split("<>")[:2]
        horario = row[0].split(":")
        days = horario[0].split("-")
        modules = horario[1].split(",")
        for day in days:
            for mod in modules:
                if len(day) and len(mod):
                    schedule[day.lower() + mod] = "'" + row[1] + "'"

    cols = ",".join(schedule.keys())
    values = ",".join(schedule.values())
    full_sc_query = (
        f"INSERT INTO courses_fullschedule (section_id, {cols}) VALUES (%s, {values});"
    )

    ### Info Schedule
    schedule_info = {"total": 0}
    for type in ["AYU", "CLAS", "LAB", "PRA", "SUP", "TAL", "TER", "TES"]:
        schedule_info[type] = list(schedule.values()).count("'" + type + "'")
        schedule_info["total"] += schedule_info[type]
        schedule_info[type] = str(schedule_info[type])
    schedule_info["total"] = str(schedule_info["total"])

    cols = ",".join(schedule_info.keys())
    values = ",".join(schedule_info.values())
    info_sc_query = (
        f"INSERT INTO courses_scheduleinfo (section_id, {cols}) VALUES (%s, {values});"
    )

    return full_sc_query, info_sc_query
