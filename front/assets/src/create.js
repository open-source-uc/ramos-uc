// CSS
import "./css/entry"

// Dependencies
import "bootstrap"
import "multiple-select"

// Public functions
import { toggle, toggleRow, toggleDay, clearSelects } from "./utils/filters"
import { add, remove, next, prev, loadFromCookie } from "./utils/creator"
import { createSearch } from "./utils/createSearch"
import { loadInfo } from "./utils/info"
import { loadQuota } from "./utils/quota"

export {
    toggle, toggleRow, toggleDay, clearSelects,
    add, remove, next, prev, loadFromCookie,
    createSearch,
    loadInfo,
    loadQuota,
}

// Automatic execution
$(() => {
    // Global variables
    wp.searchResults = []

    wp.loadFromCookie()

    // Menu highlight
    $("a[name=\"menu_create\"]").addClass("active")

    // Load filters dropdowns
    $("#campus").multipleSelect({
        selectAll: false,
        showClear: true,
    })
    $("#formato").multipleSelect({
        selectAll: false,
        showClear: true,
    })
    $("#escuela").multipleSelect({
        selectAll: false,
        filter: true,
        showClear: true,
    })
    $("#tipos_modulo").multipleSelect({
        selectAll: false,
        showClear: true,
    })
    $("#categoria").multipleSelect({
        selectAll: false,
        showClear: true,
    })
    $("#area").multipleSelect({
        selectAll: false,
        showClear: true,
    })
})
