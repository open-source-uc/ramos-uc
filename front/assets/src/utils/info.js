import ga_event from "./ga_event"

// Retrieve ramo info to modal, triggered on modal show
export const loadInfo = (id) => {
    var modal = $("#courseInfo")
    modal.html("<div class=\"spinner-border\" role=\"status\"></div>")
    $.get(`/detalle/${id.toString()}`)
        .done((response) => loadInfoHandleResponse(response, modal))
        .catch(error => {
            console.log(error)
            modal.html("Error al cargar información.")
        })
}

const loadInfoHandleResponse = (response, modal) => {
    var course = response
    // Title
    $("#courseTitle").html(`<span class="badge bg-secondary">${course.initials}</span> ${course.name}`)

    // Cupos total and available
    var cupos_html = `<b>Cupos totales:</b> ${course.available_quota}/${course.total_quota}<br>`
    if (course.quota.length) {
        let date = new Date(course.quota[0].date)
        date = date.toLocaleString("es-CL", { timeZone: "America/Santiago" })
        cupos_html += `<b>Detalle cupos:</b>(${date})<ul>`
    }
    else {
        cupos_html += "<b>No hay información sobre cupos disponibles.</b><ul>"
    }
    course.quota.forEach(row => {
        cupos_html += `<li><b>${row.category}:</b>${row.quota} cupos disponibles.</li>`
    })
    $("#courseBanner").html(`${cupos_html}</ul>`)

    // Alerts
    var alerts = ""
    if (!course.is_removable)
        alerts += "<span class=\"badge bg-danger m-2 mt-0\">No retirable</span>"
    if (course.is_english)
        alerts += "<span class=\"badge bg-danger m-2 mt-0\">Inglés</span>"
    if (course.is_special)
        alerts += "<span class=\"badge bg-danger m-2 mt-0\">Aprobación Especial</span>"
    modal.html(alerts === "" ? `<span style="font-size: larger;">${alerts}</span><br>` : "")

    // Rest of info
    modal.append(`
        <b>Campus:</b> ${course.campus}<br>
        <b>Créditos:</b> ${course.credits}<br>
        <b>Escuela:</b> ${course.school}<br>
        <b>Área:</b> ${course.area}<br>
        <b>Categoría:</b> ${course.category}<br>
        <b>Formato:</b> ${course.format}<br>
        <b>Profesor/es:</b> ${course.teachers}<br>
        <hr>
        <b>Requisitos:</b> ${course.req}<br>
        <b>Relación requistos con restricciones:</b> ${course.con}<br>
        <b>Restricciones:</b> ${course.restr}<br>
        <a class="btn btn-primary mt-2" href="${course.url}">Más información</a>
    `)

    ga_event("info", { event_category: course.escuela, event_label: course.nombre })
}
