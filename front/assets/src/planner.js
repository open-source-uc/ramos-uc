// CSS
import "./css/entry"

// Dependencies
import "bootstrap"
import "multiple-select"

// Public functions
import { toggle, toggleRow, toggleDay, clearSelects } from "./utils/filters"
import { save, unsave, viewSaved, edit, share, buscacursos } from "./utils/save"
import { add, remove, loadRamo, loadFromCookie } from "./utils/schedule"
import { loadInfo } from "./utils/info"
import { search } from "./utils/search"
import { loadQuota } from "./utils/quota"
import * as ucalendar from "./utils/ucalendar"

export {
    toggle, toggleRow, toggleDay, clearSelects,
    save, unsave, viewSaved, edit, share, buscacursos,
    add, remove, loadRamo, loadFromCookie,
    loadInfo,
    search,
    loadQuota,
}

// Automatic execution
$(() => {
    // Menu highlight
    $("a[name=\"menu_planner\"]").addClass("active")

    // Load ramos from cookie
    wp.loadFromCookie()

    $("#ucalendar").on("click", () => ucalendar.dowload_schedule())

    // Load filters dropdowns
    $("#campus").multipleSelect({ selectAll: false, showClear: true })
    $("#formato").multipleSelect({ selectAll: false, showClear: true })
    $("#escuela").multipleSelect({ selectAll: false, showClear: true, filter: true })
    $("#tipos_modulo").multipleSelect({ selectAll: false, showClear: true })
    $("#categoria").multipleSelect({ selectAll: false, showClear: true })
    $("#area").multipleSelect({ selectAll: false, showClear: true })
})
