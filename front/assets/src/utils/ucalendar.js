/**
 * @typedef {{
 *  id: number,
 *  initials: string,
 *  name: string,
 *  period: string,
 *  schedule: {[key: string]: string},
 * }} Course
 */
/** @typedef {{ day: string, module: number, type: string, group: ScheduleElement[] }} ScheduleElement */
/** @typedef {{ days: string[], modules: number[], type: string }} ScheduleBlock */


// Cosas hard-codeadas

const every_year_holidays = [
    "05-01",  // Día del trabajo
    "05-21",  // Días de las Glorias Navales
    "08-15",  // Asunción de la Virgen
    "09-18",  // Primera Junta Nacional de Gobierno
    "09-19",  // Glorias del Ejército
    "10-11",  // Celebración del Día del Encuentro de Dos Mundos
    "10-31",  // Día de las Iglesias Evangélicas y Protestantes
    "11-01",  // Día de Todos los Santos
    "12-08",  // Inmaculada Concepción de la Virgen
    "12-25",  // Navidad
]

const period_range = {
    "2023-1": [new Date(2023, 2, 6), new Date(2023, 5, 30)],
    "2023-2": [new Date(2023, 7, 7), new Date(2023, 10, 1)],
}


const holidays = [
    // Semana Santa
    new Date(2023, 3, 6),
    new Date(2023, 3, 7),
    new Date(2023, 3, 8),
    new Date(2023, 3, 9),
    // Receso
    new Date(2023, 4, 2),
    new Date(2023, 4, 3),
    new Date(2023, 4, 4),
    new Date(2023, 4, 5),
    new Date(2023, 4, 6),
    // San Pedro y San Pablo
    new Date(2023, 5, 26),
    // Asunción de la Virgen
    new Date(2023, 7, 14),
    // Receso
    new Date(2023, 9, 2),
    new Date(2023, 9, 3),
    new Date(2023, 9, 4),
    new Date(2023, 9, 5),
    new Date(2023, 9, 6),
    new Date(2023, 9, 7),
]

const module_length = { hours: 1, minutes: 20 }

const module_start_time = {
    1: { hour: 8, minute: 30 },
    2: { hour: 10, minute: 0 },
    3: { hour: 11, minute: 30 },
    4: { hour: 14, minute: 0 },
    5: { hour: 15, minute: 30 },
    6: { hour: 17, minute: 0 },
    7: { hour: 18, minute: 30 },
    8: { hour: 20, minute: 0 },
}


// Funciones de utilidad

const days = ["l", "m", "w", "j", "v", "s"]
const ics_day_names = { l: "MO", m: "TU", w: "WE", j: "TH", v: "FR", s: "SA", d: "SU" }

const eqSet = (a, b) => a.size === b.size && [...a].every(value => b.has(value))

const to_ics_datetime = (date) => {
    const year = date.getFullYear()
    const month = `0${date.getMonth() + 1}`.slice(-2)
    const day = `0${date.getDate()}`.slice(-2)
    const hours = `0${date.getHours()}`.slice(-2)
    const minutes = `0${date.getMinutes()}`.slice(-2)
    const seconds = `0${date.getSeconds()}`.slice(-2)
    return `${year}${month}${day}T${hours}${minutes}${seconds}`
}

function firstIndex(array_to_search, values) {
    for (const value of array_to_search) if (values.includes(value)) return array_to_search.indexOf(value)
}

const calendar_template = (calendar) => `
BEGIN:VCALENDAR
PRODID:-//remos-uc//ucalendar//CL
VERSION:2.0
CALSCALE:GREGORIAN
X-WR-TIMEZONE:America/Santiago
BEGIN:VTIMEZONE
TZID:America/Santiago
X-LIC-LOCATION:America/Santiago
BEGIN:STANDARD
TZOFFSETFROM:-0300
TZOFFSETTO:-0400
TZNAME:-04
DTSTART:19700405T000000
RRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1SU
END:STANDARD
BEGIN:DAYLIGHT
TZOFFSETFROM:-0400
TZOFFSETTO:-0300
TZNAME:-03
RRULE:FREQ=YEARLY;BYMONTH=9;BYDAY=1SU
END:DAYLIGHT
END:VTIMEZONE
${calendar}
END:VCALENDAR
`

let event_id = 0
const event_template = (e) => `
BEGIN:VEVENT
DTSTART;TZID=America/Santiago:${e.start}
DTEND;TZID=America/Santiago:${e.end}
RRULE:FREQ=WEEKLY;UNTIL=${e.last};BYDAY=${e.days}
${e.ex_dates}
DTSTAMP:${to_ics_datetime(new Date())}
UID:${event_id++}
DESCRIPTION:${e.description}
SUMMARY:${e.summary}
END:VEVENT
`

const ex_date_template = (date) => `EXDATE;TZID=America/Santiago:${to_ics_datetime(date)}`

const generateExDates = (start) => {
    const ex_dates = [...holidays]
    for (const [month, day] of every_year_holidays.map(h => h.split("-"))) {
        const date = new Date(2023, month - 1, + day)
        ex_dates.push(date)
    }
    return ex_dates.map(date => {
        date.setHours(start.getHours(), start.getMinutes(), start.getSeconds())
        return ex_date_template(date)
    }).join("\n")
}

function dispatch_download(content, name = "horario.ics") {
    const e = document.createElement("a")
    e.setAttribute("href", `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`)
    e.setAttribute("download", name)
    e.style.display = "none"
    document.body.appendChild(e)
    e.click()
    document.body.removeChild(e)
}



// Aquí empieza la lógica de UCalendar

/** @param {Course[]} courses  */
function make_block_schedule(courses){
    return courses.flatMap(({ schedule, ...course }) => {
        const scheduleDays = Object.entries(schedule).map(([[day, m], type]) => {
            /** @type {ScheduleElement} */
            const self = { day, module: parseInt(m), type, group: [] }
            self.group.push(self)
            return self
        })

        // Vertical
        for (const bs of scheduleDays) {
            for (const rs of scheduleDays) {
                if (bs.group === rs.group) continue
                if (bs.day !== rs.day || bs.type !== rs.type) continue
                if (Math.abs(bs.module - rs.module) > 1) continue

                // No se puede expandir entre 3 y 4 (almuerzo)
                if (bs.module === 3 && rs.module === 4) continue
                if (bs.module === 4 && rs.module === 3) continue

                bs.group.push(rs)
                rs.group = bs.group
            }
        }

        // Horizontal
        for (const bs of scheduleDays) {
            for (const rs of scheduleDays) {
                if (bs.group === rs.group) continue
                if (bs.type !== rs.type) continue

                // Ver si los grupos tienen los mismos modulos
                const bsModSet = new Set(bs.group.map((e) => e.module))
                const rsModSet = new Set(rs.group.map((e) => e.module))
                if (!eqSet(bsModSet, rsModSet)) continue

                bs.group.push(rs)
                rs.group = bs.group
            }
        }

        // Entregar grupos
        const groupSet = new Set(scheduleDays.map((g) => g.group))

        const groupsWithMeta = Array.from(groupSet).map((group) => {
            const days = [... new Set(group.map((g) => g.day))]
            const modules = [... new Set(group.map((g) => g.module))]
            const type = group[0].type
            return { days, modules, type, group, course }
        })

        return groupsWithMeta
    })
}

class UCalendar {
    constructor() {
        this.semester = "2023-1"
        /** @type {Course[]} */
        this.schedule = []
    }

    add_from_schedule_page(id, course) {
        this.schedule.push({ id, ...course })
    }

    remove_from_schedule_page(id) {
        this.schedule = this.schedule.filter((c) => c.id !== id)
    }

    dowload_schedule() {
        console.log("Downloading schedule", this.schedule)
        const blockSchedule = make_block_schedule(this.schedule)
        const events = blockSchedule.map((block) => this._make_events(block))
        const ics = calendar_template(events.map((e) => event_template(e)).join("\n"))
        dispatch_download(ics.split("\n").filter((l) => l.trim()).join("\r\n"))
    }

    /** @param {ScheduleBlock} block */
    _make_events(block) {
        const first_module = Math.min(...block.modules)
        const last_module = Math.max(...block.modules)
        const first_day_number = firstIndex(days, block.days)

        const [initial_date, last_date] = period_range[this.semester]

        // Se necesita mover el primer dia de clases para que este en el primer día del bloque
        // en específico, así podemos decir que el evento se repite de ahi hasta el ultimo dia
        const initial_date_day = new Date(initial_date).getDay()  // 0: Domingo, 1: Lunes, ...
        const initial_date_offset = ((first_day_number + 1) - initial_date_day + 7) % 7
        const initial_date_offsetted = new Date(initial_date)
        initial_date_offsetted.setDate(initial_date.getDate() + initial_date_offset)

        const { hour, minute } = module_start_time[first_module]
        const start = new Date(initial_date_offsetted)
        start.setHours(hour, minute, 0, 0)

        const end_delta = module_start_time[last_module]
        const end = new Date(start)
        end.setHours(end_delta.hour + module_length.hours, end_delta.minute + module_length.minutes)

        const block_days = block.days.map((d) => ics_day_names[d]).join(",")

        const name_prefix = block.type === "CLAS" ? "" : `${block.type} `


        return {
            start: to_ics_datetime(start),
            end: to_ics_datetime(end),
            last: to_ics_datetime(last_date),
            days: block_days,
            summary: `${name_prefix}${block.course.name}`,
            description: "",
            ex_dates: generateExDates(start),
        }
    }
}

export const ucalendar = new UCalendar()
