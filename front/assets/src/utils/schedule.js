import { getCookie, setCookie } from "./cookies"

// Add ramo to cookie and load it to schedule
const add = (id) => {
    id = id.toString()
    // Save in cookie
    var saved = getCookie("ramos")
    saved = saved ? saved.split(",") : []
    if (saved.includes(id)) {
        return
    }
    saved.push(id)
    setCookie("ramos", saved.join(","), 30)

    loadRamo(id)

    // google analytics
    try {
        gtag("event", "add_to_schedule", {
            event_category: "schedule",
            event_label: id,
        })
    } catch (error) {
        console.log("No analytics.")
    }
}

// Remove ramo from horario and cookie
const remove = (id) => {
    // Remove from cookie
    var saved = getCookie("ramos")
    saved = saved ? saved.split(",") : []
    var index = saved.indexOf(id)
    if (index != -1) {
        saved.splice(index, 1)
    }
    setCookie("ramos", saved.join(","), 120)

    var parents = $(`td > [name='ramo_${id}']`).parent().get()
    $(`td > [name='ramo_${id}']`).next().remove()
    $(`[name='ramo_${id}']`).remove()
    parents.forEach((td) => {
        if (td.children.length == 0) {
            $(`#${td.id}`).removeClass("table-secondary")
        }
    })

    // google analytics
    try {
        gtag("event", "remove_from_schedule", {
            event_category: "schedule",
            event_label: id,
        })
    } catch (error) {
        console.log("No analytics.")
    }
}

// Retrieve ramo info and show it on schedule
const loadRamo = (id, showDelete = true) => {
    var ramos = $("#ramos")
    ramos.append("<div class=\"spinner-border ramos_load\" role=\"status\"></div>")

    $.get(`/detalle/${id}/horario`)
        .then(response => {
            var ramo = response
            // Print in horario
            for (let [key, value] of Object.entries(ramo.schedule)) {
                if (value == "CLAS") value = "warning text-dark"
                else if (value == "AYU") value = "success"
                else if (value == "LAB") value = "primary"
                else if (value == "TAL") value = "secondary"
                else if (value == "TER") value = "info text-dark"
                else value = "danger"
                var slot = $(`#${key.toUpperCase()}`)
                slot.append(`<span name="ramo_${id}" class="badge bg-${value}" style="font-size: 0.85em;">${ramo.initials}</span><br>`)
                slot.addClass("table-secondary")
            }
            // Print on detalles
            let row = `<tr name="ramo_${id}">`
            if (showDelete) {
                row += `
                <td><button onclick="wp.remove('${id}')" type="button" class="btn" aria-label="Eliminar"><img src="/dist/images/close.svg" height="15"/></button></td>
            `
            }
            row += `
            <td>${ramo.period}</td>
            <td><a data-bs-toggle="modal" href="#quotaModal" onclick="wp.loadQuota(${id})"><img src="/dist/images/chart.svg" height="20"/></a></td>
            <td><a class="badge bg-secondary" data-bs-toggle="modal" href="#infoModal" onclick="wp.loadInfo(${id})">${ramo.initials}</a></td>
            <td>${ramo.name}</td>
            </tr>
        `
            ramos.append(row)
            $(".ramos_load").remove()
        })
        .catch(error => {
            console.log(error)
            $(".ramos_load").remove()
        })
}

// Autoload ramos saved in cookie
const loadFromCookie = () => {
    var saved = getCookie("ramos")
    saved = saved ? saved.split(",") : []
    saved.forEach((id) => {
        loadRamo(id)
    })
}

export { add, remove, loadRamo, loadFromCookie }
