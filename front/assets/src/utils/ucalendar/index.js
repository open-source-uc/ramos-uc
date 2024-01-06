/** @author @benjavicente */

/** @typedef {{[key: string]: string}} ScheduleMap */
/** @typedef {{ id: number, initials: string, name: string,  period: string, schedule: ScheduleMap }} Course */
/** @typedef {{ day: string, module: number, type: string, group: ScheduleElement[] }} ScheduleElement */
/** @typedef {{ days: string[], modules: number[], type: string }} ScheduleBlock */


import { module_start_time, holidays, every_year_holidays, module_length, ics_day_names, days, period_range } from "./consts"
import { calendarTemplate, eventTemplate, exDateTemplate } from "./templates"
import { dispatchDownload, eqSet, firstIndex } from "./utils"


// API

/** @type {Course[]} */
let courses = []
export const add_from_schedule_page = (id, course) => courses.push({ id, ...course })
export const remove_from_schedule_page = (id) => courses = courses.filter((c) => c.id !== id)
export const dowload_schedule = () => dispatchDownload(makeCalendarFromCoruses(courses), "horario.ics")


// UCalendar

/** @param {Course[]} courses */
function makeCalendarFromCoruses(courses, semester = "2023-1") {
    return calendarTemplate(courses.flatMap(groupModules).map((e) => toEvent(e, semester)).map(eventTemplate).join("\n"))
}

/** @param {Date} dateToChange, @param {Date} dateWithTime */
function changeTimeOfDate(dateToChange, dateWithTime) {
    dateToChange.setHours(dateWithTime.getHours(), dateWithTime.getMinutes(), dateWithTime.getSeconds())
    return dateToChange
}

/** @param {Date} start */
function generateExDates(start) {
    const ex_dates = holidays.map((h) => new Date(h))  // copy dates
    for (const [month, day] of every_year_holidays.map(h => h.split("-")))
        ex_dates.push(new Date(2023, month - 1, + day))
    return ex_dates.map(d => changeTimeOfDate(d, start)).map(exDateTemplate).join("\n")
}

/** @param {Course} course */
function groupModules({ schedule, ...course }) {

    const scheduleDays = Object.entries(schedule).map(([[day, m], type]) => {
        /** @type {ScheduleElement} */
        const self = { day, module: parseInt(m), type, group: [] }
        self.group.push(self)
        return self
    })

    // Vertical
    for (const bs of scheduleDays) {
        for (const rs of scheduleDays) {
            if (bs.group === rs.group || bs.type !== rs.type) continue

            // Ve si están juntos y en el mismo día
            if (bs.day !== rs.day) continue
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
            if (bs.group === rs.group || bs.type !== rs.type) continue

            // Ver si los grupos tienen los mismos modulos
            const bsModSet = new Set(bs.group.map((e) => e.module))
            const rsModSet = new Set(rs.group.map((e) => e.module))
            if (!eqSet(bsModSet, rsModSet)) continue

            bs.group.push(rs)
            rs.group = bs.group
        }
    }

    // Entregar grupos
    return [...new Set(scheduleDays.map((g) => g.group))].map((group) => {
        const days = [... new Set(group.map((g) => g.day))]
        const modules = [... new Set(group.map((g) => g.module))]
        const type = group[0].type
        return { days, modules, type, group, course }
    })
}

/** @param {ScheduleBlock} block, @param {string} semester */
function toEvent(block, semester) {
    const first_module = Math.min(...block.modules)
    const last_module = Math.max(...block.modules)
    const first_day_number = firstIndex(days, block.days)

    const [initial_date, last_date] = period_range[semester]

    // Se necesita mover el primer dia de clases para que este en el primer día del bloque
    // en específico, así podemos decir que el evento se repite de ahi hasta el ultimo dia
    const initial_date_day = new Date(initial_date).getDay()  // 0: Domingo, 1: Lunes, ...
    const initial_date_offset = ((first_day_number + 1) - initial_date_day + 7) % 7
    const initial_date_offsetted = new Date(initial_date)
    initial_date_offsetted.setDate(initial_date.getDate() + initial_date_offset)

    const { hour, minute } = module_start_time[first_module]
    const start = new Date(initial_date_offsetted)
    start.setHours(hour, minute, 0, 0)  // Parte en el minuto y segundo 0

    const end_delta = module_start_time[last_module]
    const end = new Date(start)
    end.setHours(end_delta.hour + module_length.hours, end_delta.minute + module_length.minutes)

    const block_days = block.days.map((d) => ics_day_names[d]).join(",")

    const summary = `${block.type === "CLAS" ? "" : `${block.type} `}${block.course.name}`
    const ex_dates = generateExDates(start)

    return { start, end, last_date, block_days, summary, ex_dates }
}
