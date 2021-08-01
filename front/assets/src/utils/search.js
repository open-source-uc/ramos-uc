import ga_event from "./ga_event"

// Make ajax search request and load results to table
export const search = (page = 1) => {
    var table = $("#results")
    table.html("<div class=\"spinner-border\" role=\"status\"></div>")

    var overlap = $("#tope_horario").prop("checked")
    const events = []
    if (overlap) {
        "LMWJVS".split("").forEach(day => {
            "12345678".split("").forEach(module => {
                if ($(`#${day}${module}`).hasClass("table-secondary")) {
                    events.push(day + module)
                }
            })
        })
    }

    var request_content = {
        overlap,
        page,
        area: $("#area").val(),
        campus: $("#campus").val(),
        category: $("#categoria").val(),
        credits: $("#creditos").val(),
        format: $("#formato").val(),
        free_quota: $("#quota").prop("checked"),
        max_mod: $("#modulos").val(),
        mod_types: $("#tipos_modulo").val(),
        overlap_except: $("#tope_ayu").prop("checked"),
        period: $("#periodSelect").val(),
        q: $("#inputQuery").val(),
        schedule: events.join(","),
        school: $("#escuela").val(),
        without_req: $("#requisitos").prop("checked"),
    }
    ga_event("search", { event_category: request_content.period, event_label: request_content.q })
    $.get("/p_search", request_content)
        .done((response) => searchHandleResults(response, table, page))
        .fail(error => {
            console.log(error)
            $("#resultsFoot").html("<tr><td>Error en la búsqueda</td></tr>")
        })
    return false
}

const searchHandleResults = (response, table, page) => {
    if (response.error) {
        $("#resultsFoot").html("<tr><td>Error en la búsqueda</td></tr>")
        return false
    }
    const results = response.results

    if (! results.length) {
        table.html("<tr><td colspan=\"5\">No se encontaron resultados.</td></tr>")
        return false
    }
    table.html("")

    results.forEach(({ id, initials, name, teachers, format, available_quota, schedule }) => {
    // Characteristics
        let row = "<tr class=\"border-top\">"
        row += `<td><button class="btn p-0 m-1" onclick="wp.add(${id})"><img src="/dist/images/add.svg" height="25"/></button>`
        row += `<button class="btn p-0 m-1" data-bs-toggle="modal" href="#quotaModal" onclick="wp.loadQuota(${id})"><img src="/dist/images/chart.svg" height="25"/></button></td>`
        row += `<td><a class="badge bg-secondary" data-bs-toggle="modal" href="#infoModal" onclick="wp.loadInfo(${id})">${initials}</a></td>`
        row += `<td>${name}</td>`
        row += `<td>${teachers.replace(/,/g, "<br>")}</td>`
        row += `<td>${format}</td>`
        row += `<td>${available_quota}</td>`

        // Schedule
        let horario = schedule.split("\n").slice(1)
        row += "<td>"
        horario.forEach(line => {
            line = line.substring(4)
            line = line.split("<>")
            row += `<b>${line[1]}</b>${line[0]}<br>`
        })
        row += "</td>"
        row += "</tr>"

        // Print
        table.append(row)
    })
    table.focus()

    var footer = $("#resultsFoot")
    footer.html("")
    if (page > 1) {
        footer.append(`<button onclick="wp.search(${(page - 1).toString()});" class="btn btn-outline-primary me-3"><< Anterior</button>`)
    }
    if (response.length == 25) {
        footer.append(`<button onclick="wp.search(${(page + 1).toString()});" class="btn btn-outline-primary">Siguiente >></button>`)
    }
}
