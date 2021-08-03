import { Course } from "./classes/Course"
import { Module } from "./classes/Module"
import { getCookie, setCookie } from "./cookies"

// Local variables
let combinations = []
let addedCourses = []
let combinationIndex = 0


const add = (initials) => {
    let course = wp.searchResults.find(c => c.initials == initials)
    if (course) {
        let c = addedCourses.find(c => c.initials == course.initials)
        if (!c) {
            addedCourses.push(course)
        }
    }
    updateCookie()
    generateCombinations()
    updateUI()
}

const remove = (initials) => {
    let index = addedCourses.findIndex(c => c.initials == initials)
    addedCourses.splice(index, 1)
    updateCookie()
    generateCombinations()
    updateUI()
}

const updateCookie = () => {
    let initials = addedCourses.map(course => course.initials)
    setCookie("ramos-crea", initials.join(","), 30)
}

const loadFromCookie = () => {
    let savedInitials = getCookie("ramos-crea")

    if (savedInitials != "") {
        let initialsToLoad = savedInitials.split(",")

        let promises = initialsToLoad.map(initials => {
            let body = {
                period: "2021-2",
                q: initials,
                overlap: false,
                overlap_except: false,
                without_req: false,
                free_quota: false,
            }
            return $.get("/p_search", body)
        })

        Promise.all(promises)
            .then(responses => {
                addedCourses = responses.map(({ results }) => {
                    let firstResult = results[0]
                    let course = new Course(firstResult.course_initials, firstResult.name, results)
                    course.group()
                    return course
                })
                generateCombinations()
                updateUI()
            }).catch(e => {
                console.error("No se pudo cargar ramos desde la cookie", e)
            })
    }
}

const next = () => {
    if (combinationIndex < combinations.length - 1) {
        combinationIndex += 1
    }
    updateUI()
}

const prev = () => {
    if (combinationIndex > 0) {
        combinationIndex -= 1
    }
    updateUI()
}

const generateCombinations = () => {
    combinationIndex = 0
    combinations = []

    addedCourses.forEach(course => course.group(true))

    if (addedCourses.length > 0) {
        let courses = [...addedCourses]
        let course = courses.shift()

        combinations = course.groups.map(group => [group])

        while(courses.length > 0) {
            let newCombinations = []
            course = courses.shift()

            combinations.forEach(combination => {
                course.groups.forEach(g => {
                    let compatible = combination.every(g2 =>
                        Module.compatibleSchedules(g.schedule_obj, g2.schedule_obj))

                    if (compatible) {
                        let newCombination = [...combination]
                        newCombination.push(g)
                        newCombinations.push(newCombination)
                    }
                })
            })

            combinations = newCombinations
        }
    }
}

const resetHorario = () => {
    let days = ["L", "M", "W", "J", "V", "S"]
    let modules = 8

    for (let i = 0; i < modules; i++) {
        days.forEach(day => {
            let slot = $(`#${day}${String(i + 1)}`)

            if (slot.html() != "") {
                slot.removeClass("table-secondary")
            }

            slot.html("")
        })
    }
}

const updateUI = () => {
    // Update tabla agregados
    let table = $("#ramos")

    if (addedCourses.length == 0)
        table.html("<tr><td colspan=\"5\">No has agregado ningún ramo.</td></tr>")
    else {
        table.html("")

        addedCourses.forEach(({ initials, name, sections, groups, selections }) => {
            let row = "<tr>"
            row += `<td><button onclick="wp.remove('${initials}')" type="button" class="btn" aria-label="Eliminar"><img src="/dist/images/close.svg" height="15"/></button></button>`
            row += `<td><span class="badge bg-secondary">${initials}</span></td>`
            row += `<td>${name}</td>`
            row += `<td><a href="#sectionSelectorModal" data-bs-toggle="modal" onclick="wp.openSectionSelect('${initials}')">${selections.length > 0 ? `${selections.length}/${sections.length}` : sections.length}</a></td>`
            row += `<td>${groups.length}</td></tr>`

            table.append(row)
        })
    }

    resetHorario()

    // Show combination
    if (combinations.length > 0) {
        $("#combination-title").html(`Combinación ${String(combinationIndex + 1)} de ${String(combinations.length)}`)
        $("#combination").html("")

        let combination = combinations[combinationIndex]

        combination.forEach(({ initials, schedule_obj, sections, name }) => {
            // Horario
            schedule_obj.forEach(module => {
                let color = "danger"
                if (module.type == "CLAS") color = "warning text-dark"
                else if (module.type == "AYU") color = "success"
                else if (module.type == "LAB") color = "primary"
                else if (module.type == "TAL") color = "secondary"
                else if (module.type == "TER") color = "info text-dark"

                module.days.forEach(day => {
                    module.mods.forEach(mod => {
                        let slot = $(`#${day + String(mod)}`)
                        slot.append(`<span name="ramo_${initials}" class="badge bg-${color}" style="font-size: 0.85em;">${initials}</span><br>`)
                    })
                })
            })

            // Tabla
            let firstSection = sections[0]
            let otherSections = sections.slice(1)

            let row = "<tr>"
            row += `<td rowspan=${sections.length} class="align-middle">${name}</td>`
            row += `<td><a class="badge bg-secondary" data-bs-toggle="modal" href="#infoModal" onclick="wp.loadInfo(${firstSection.id})">${firstSection.initials}</a></td>`
            row += `<td>${firstSection.teachers.replaceAll(",", ", ")}</td>`
            row += `<td>${firstSection.available_quota}</td>`
            row += `<td><button class="btn p-0 m-1" data-bs-toggle="modal" href="#quotaModal" onclick="wp.loadQuota(${firstSection.id})"><img src="/dist/images/chart.svg" height="25"/></button></td>`
            row += "</tr>"


            otherSections.forEach(section => {
                row += "<tr>"
                row += `<td><a class="badge bg-secondary" data-bs-toggle="modal" href="#infoModal" onclick="wp.loadInfo(${section.id})">${section.initials}</a></td>`
                row += `<td>${section.teachers.replaceAll(",", ", ")}</td>`
                row += `<td>${section.available_quota}</td>`
                row += `<td><button class="btn p-0 m-1" data-bs-toggle="modal" href="#quotaModal" onclick="wp.loadQuota(${section.id})"><img src="/dist/images/chart.svg" height="25"/></button></td>`
                row += "</tr>"
            })

            $("#combination").append(row)

        })
    } else {
        $("#combination-title").html("Combinación")
        $("#combination").html("<tr><td colspan=\"5\">No hay ninguna combinación</td></tr>")
    }

    // Buttons
    let prev = true
    let next = true

    if (combinations.length == 0) {
        prev = false
        next = false
    }
    if (combinationIndex == 0) {
        prev = false
    }
    if (combinationIndex == combinations.length - 1) {
        next = false
    }

    $("#btn-prev").prop("disabled", !prev)
    $("#btn-next").prop("disabled", !next)


}

const openSectionSelect = (initials) => {
    let course = addedCourses.find(c => c.initials == initials)

    if (!course) {
        console.error("No se ha podido abrir el modal para seleccionar las secciones correctamente", initials)
        return
    }

    $("#sectionSelectorTitle").html(`${course.initials} - ${course.name}`)

    let table = $("#sectionSelectorTable")
    table.html("")
    console.log(course)
    course.sections.forEach(section => {
        let section_number = section.section
        let selected = course.selections.includes(section_number)

        let row = "<tr>"
        row += `<td><input class="form-check-input" type="checkbox" value="" id="section-${section_number}-checkbox" ${selected ? "checked" : ""}></td>`
        row += `<td>${section_number}</td>`
        row += `<td>${section.teachers.replaceAll(",", ", ")}</td>`
        row += `<td>${section.format}</td>`
        row += `<td>${section.available_quota}</td>`
        row += `<td>${section.schedule.replace("\nROW:", "").replaceAll("\nROW:", "<br>").replaceAll("<>", " ")}</td>`
        row += "</tr>"

        table.append(row)
    })

    $("#closeSectionSelectorButton").attr("onclick", `wp.saveSectionSelections('${initials}')`)
}

const saveSectionSelections = (initials) => {
    let course = addedCourses.find(c => c.initials == initials)

    if (!course) {
        console.error("No se ha guardar las selecciones", initials)
        return
    }

    let selections = []

    course.sections.forEach(({ section }) => {
        if ($(`#section-${section}-checkbox`).is(":checked")) {
            selections.push(section)
        }
    })

    course.selections = selections

    generateCombinations()
    updateUI()
}

export { add, remove, next, prev, loadFromCookie, openSectionSelect, saveSectionSelections }
