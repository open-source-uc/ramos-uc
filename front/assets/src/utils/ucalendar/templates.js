const toICSDatetime = (date) => {
    const year = date.getFullYear()
    const month = `0${date.getMonth() + 1}`.slice(-2)
    const day = `0${date.getDate()}`.slice(-2)
    const hours = `0${date.getHours()}`.slice(-2)
    const minutes = `0${date.getMinutes()}`.slice(-2)
    const seconds = `0${date.getSeconds()}`.slice(-2)
    return `${year}${month}${day}T${hours}${minutes}${seconds}`
}


export const calendarTemplate = (calendar) => `
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
export const eventTemplate = (e) => `
BEGIN:VEVENT
DTSTART;TZID=America/Santiago:${toICSDatetime(e.start)}
DTEND;TZID=America/Santiago:${toICSDatetime(e.end)}
RRULE:FREQ=WEEKLY;UNTIL=${toICSDatetime(e.last_date)};BYDAY=${e.block_days}
${e.ex_dates}
DTSTAMP:${toICSDatetime(new Date())}
UID:${event_id++}
DESCRIPTION:${e.description || ""}
SUMMARY:${e.summary}
END:VEVENT
`

export const exDateTemplate = (date) => `EXDATE;TZID=America/Santiago:${toICSDatetime(date)}`
