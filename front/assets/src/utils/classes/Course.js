import { Module } from "./Module"

export class Course {
    constructor (initials, name, sections) {
        this.initials = initials
        this.sections = sections
        this.name = name
        this.groups = []
        this.selections = []
    }

    addSection(section){
        this.sections.push(section)
    }

    // Group sections that have the same schedule
    group(onlySelected = false){
        let sections = this.sections

        if (onlySelected && this.selections.length > 0) {
            sections = sections.filter(({ section }) => this.selections.includes(section))
        }

        sections = sections.map(s => {
            s.schedule_obj = Module.scheduleFromString(s.schedule)
            return s
        })

        let groups = []

        while (sections.length > 0) {
            let section = sections.shift()
            let { schedule_obj, schedule } = section

            let group_sections = []
            group_sections = sections.filter(s2 => Module.equalSchedules(schedule_obj, s2.schedule_obj))

            group_sections.forEach(s => sections.splice(sections.indexOf(s), 1))

            group_sections.unshift(section)

            let section_numbers = group_sections.map(s => s.section).join()

            groups.push({
                initials: `${this.initials}-${section_numbers}`,
                name: this.name,
                schedule,
                schedule_obj,
                sections: group_sections,
            })
        }

        this.groups = groups

        return groups
    }

}
