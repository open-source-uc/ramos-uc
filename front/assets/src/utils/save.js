import { getCookie, setCookie } from "./cookies"
import ga_event from "./ga_event"


// Create share link and copy to clipboard
const share = () => {
    var saved = getCookie("ramos")
    saved = `${location.protocol}//${location.host}/share?h=${saved}`
    navigator.clipboard.writeText(saved)
        .then(() => {
            alert("Link copiado, ahora puedes compartirlo con quien quieras!")
        })
    ga_event("share", { event_category: "difusion", value: saved.split(",").length })
}

// Create share link to buscacursos and copy to clipboard
const buscacursos = () => {

    var saved = getCookie("ramos")
    saved = saved ? saved.split(",") : []

    // make link to buscacursos with actual schedule
    var buscacursos_link = "https://buscacursos.uc.cl/?cursos="
    var fst = 1

    for (let i in saved) {

        // get course initial in html
        let tb = $(`[name=ramo_${saved[i]}]`)
        let course_initial = tb.find("td").eq(3).text()

        // add coma only after the first course code
        fst == 0 ? (buscacursos_link += ",") : (fst = 0)

        buscacursos_link += course_initial
    }

    navigator.clipboard.writeText(buscacursos_link)
        .then(() => alert("Link copiado, ahora puedes ver tu horario en buscacursos!"))

}

// From share view, load ramos to cookie and redirect to root
const edit = (ids) => {
    ga_event("edit", { value: ids.split(",").length })

    if (confirm("Al editar este horario se perderá la información de cualquier otro horario que no hayas guardado.")) {
        setCookie("ramos", ids, 120)
        location.href = "/planifica"
    }
}

// Save cookie to local storage with name identifier
const save = () => {
    var name = `horario_${$("#saveName").val()}`
    var saved = getCookie("ramos")
    localStorage.setItem(name, saved)
    ga_event("save", { event_category: "persistence", value: saved.split(",").length })
}

// Load horarios names from local storage to modal
const viewSaved = () => {
    var modal = $("#savedTable")
    modal.html("")
    Object.keys(localStorage).forEach(key => {
        if (key.substring(0, 8) == "horario_") {
            let name = key.substring(8)
            let ids = localStorage[key]
            modal.append(`
                <div class="row mb-2">
                    <b class="col">${name}</b>
                    <div class="col">
                        <button onclick="wp.edit('${ids}')" class="btn btn-primary">Abrir</button>
                        <button onclick="wp.unsave('${key}')" class="btn btn-danger">Eliminar</button>
                    </div>
                </div>
            `)
        }
    })
    ga_event("view_saved", { event_category: "persistence" })
}

// Delete schedule from local storage and reload modal
const unsave = (key) => {
    localStorage.removeItem(key)
    viewSaved()
    ga_event("unsave", { event_category: "persistence" })
}

export { save, unsave, viewSaved, edit, share, buscacursos }
