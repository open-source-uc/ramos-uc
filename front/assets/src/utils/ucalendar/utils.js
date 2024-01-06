export const eqSet = (a, b) => a.size === b.size && [...a].every(value => b.has(value))

export function firstIndex(array_to_search, values) {
    for (const value of array_to_search) if (values.includes(value)) return array_to_search.indexOf(value)
}

export function dispatchDownload(content, name = "horario.ics") {
    const e = document.createElement("a")
    e.setAttribute("href", `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`)
    e.setAttribute("download", name)
    e.style.display = "none"
    document.body.appendChild(e)
    e.click()
    document.body.removeChild(e)
}
