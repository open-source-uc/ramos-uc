export const every_year_holidays = [
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

export const period_range = {
    "2023-1": [new Date(2023, 2, 6), new Date(2023, 5, 30)],
    "2023-2": [new Date(2023, 7, 7), new Date(2023, 10, 1)],
}


export const holidays = [
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

export const module_length = { hours: 1, minutes: 20 }

export const module_start_time = {
    1: { hour: 8, minute: 30 },
    2: { hour: 10, minute: 0 },
    3: { hour: 11, minute: 30 },
    4: { hour: 14, minute: 0 },
    5: { hour: 15, minute: 30 },
    6: { hour: 17, minute: 0 },
    7: { hour: 18, minute: 30 },
    8: { hour: 20, minute: 0 },
}

export const ics_day_names = { l: "MO", m: "TU", w: "WE", j: "TH", v: "FR", s: "SA", d: "SU" }
export const days = [...Object.keys(ics_day_names)]
