import "multiple-select"


// Toogle availability state in schedule, for one module
const toggle = (module) => {
    module.className = (module.className === "" ? "table-secondary" : "")
}

// Toogle availability state in schedule, for all row
const toggleRow = (module) => {
    let toogle = ""
    if (document.getElementById(`L${module.toString()}`).className == "") {
        toogle = "table-secondary"
    }
    "LMWJVS".split("").forEach(day => {
        document.getElementById(day + module.toString()).className = toogle
    })
}

// Toogle availability state in schedule, for all day
const toggleDay = (day) => {
    let toogle = ""
    if (document.getElementById(`${day}1`).className == "") {
        toogle = "table-secondary"
    }
    "12345678".split("").forEach(module => {
        document.getElementById(day + module).className = toogle
    })
}

// Clear multiple select filters
const clearSelects = () => {
    $("#campus").multipleSelect("uncheckAll")
    $("#formato").multipleSelect("uncheckAll")
    $("#escuela").multipleSelect("uncheckAll")
    $("#tipos_modulo").multipleSelect("uncheckAll")
    $("#area").multipleSelect("uncheckAll")
    $("#categoria").multipleSelect("uncheckAll")
}

export { toggle, toggleRow, toggleDay, clearSelects }
