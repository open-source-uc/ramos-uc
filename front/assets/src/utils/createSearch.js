import { Course } from "./classes/Course"

// Make ajax search request and load results to table
export const createSearch = (page = 1) => {
    var table = $("#results")
    table.html("<div class=\"spinner-border\" role=\"status\"></div>")

    var query = $("#inputQuery").val()
    var period = $("#periodSelect").val()
    var campus = $("#campus").val()
    var formato = $("#formato").val()
    var escuela = $("#escuela").val()
    var tipos_mod = $("#tipos_modulo").val()
    var area = $("#area").val()
    var categoria = $("#categoria").val()
    var max_mod = $("#modulos").val()
    var creditos = $("#creditos").val()
    var requisitos = $("#requisitos").prop("checked")
    var tope = true
    var tope_excep = false
    var free_quota = $("#quota").prop("checked")
    var horario = []
    if (tope) {
        "LMWJVS".split("").forEach(day => {
            "12345678".split("").forEach(module => {
                if ($(`#${day}${module}`).hasClass("table-secondary")) {
                    horario.push(day + module)
                }
            })
        })
        horario = horario.join(",")
    }

    var query_body = {
        q: query,
        period: period,
        campus: campus,
        format: formato,
        school: escuela,
        mod_types: tipos_mod,
        area: area,
        category: categoria,
        max_mod: max_mod,
        credits: creditos,
        without_req: requisitos,
        overlap: tope,
        overlap_except: tope_excep,
        schedule: horario,
        free_quota: free_quota,
        page: page,
    }

    $.get("/p_search", query_body)
        .done(response => {
            if (response.error) {
                $("#resultsFoot").html("<tr><td>Error en la búsqueda</td></tr>")
                return false
            }
            response = response.results

            if (! response.length) {
                table.html("<tr><td colspan=\"5\">No se encontaron resultados.</td></tr>")
                return false
            }
            table.html("")

            // Group results by initials
            let courses = []

            response.forEach(result => {
                let course = courses.find(c => c.initials === result.course_initials)

                if (course) {
                    course.addSection(result)
                } else {
                    courses.push(new Course(result.course_initials, result.name, [result]))
                }
            })

            // Group each course by its schedule
            courses.forEach(course => course.group())

            wp.searchResults = courses

            courses.forEach(course => {
            // Characteristics
                let row = "<tr class=\"border-top\">"
                row += `<td><button class="btn p-0 m-1" onclick="wp.add('${course.initials}')"><img src="/dist/images/add.svg" height="25"/></button>`
                row += `<td><span class="badge bg-secondary" href="#">${course.initials}</span></td>`
                row += `<td>${course.name}</td>`
                row += `<td>${course.sections.length}</td>`
                row += `<td>${course.groups.length}</td>`

                // Print
                row += "</tr>"
                table.append(row)
            })
            table.focus()

            var footer = $("#resultsFoot")
            footer.html("")
            if (page > 1) {
                footer.append(`<button onclick="wp.createSearch(${(page - 1).toString()});" class="btn btn-outline-primary me-3"><< Anterior</button>`)
            }
            if (response.length == 25) {
                footer.append(`<button onclick="wp.createSearch(${(page + 1).toString()});" class="btn btn-outline-primary">Siguiente >></button>`)
            }
        })
        .fail(error => {
            console.log(error)
            $("#resultsFoot").html("<tr><td>Error en la búsqueda</td></tr>")
        })

    // google analytics
    try {
        gtag("event", "createSearch", {
            event_category: period,
            event_label: query,
        })
    } catch (error) {
        console.log("No analytics.")
    }
    return false
}
