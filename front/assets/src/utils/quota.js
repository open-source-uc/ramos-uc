import ga_event from "./ga_event.js"


// Retrieve ramo info to modal, triggered on modal show
export const loadQuota = (id) => {
    var modal = $("#quotaChart")
    modal.html("<div class=\"spinner-border\" role=\"status\"></div>")

    $.get(`/banner/${id.toString()}`)
        .done((response) => loadQuotaHandleResponse(response, modal))
        .catch(error => {
            console.log(error)
            modal.html("Error al cargar información.")
        })
}


const loadQuotaHandleResponse = (response, modal) => {
    $("#quotaTitle").text(response.initials)
    // Format data
    var categories = {}
    var dates = {}
    response.quota.forEach(({ category, date }) => {
        categories[category] = null
        dates[date] = null
    })
    categories = Object.keys(categories)

    // Prefill with nulls
    Object.keys(dates).forEach(date => {
        dates[date] = new Array(categories.length).fill(null)
    })

    // Fill with data
    response.quota.forEach(({ category, date, quota }) => {
        dates[date][categories.indexOf(category)] = quota
    })

    // Create Google Charts
    const drawChart = () => {
        var data = new google.visualization.DataTable()
        // Columns -> Tiempo, ...categories
        data.addColumn("string", "Tiempo")
        categories.forEach(col => {
            data.addColumn("number", col)
            // data.addColumn({type: 'string', role: 'tooltip'});
        })

        // Rows -> Date, ...quotas ordered by categories
        Object.keys(dates).forEach(date => {
            try {
                let str_date = (new Date(date)).toLocaleString("es-CL", { timeZone: "America/Santiago" })
                /* Tooltips
                let interpolated = [];
                dates[date].forEach(quota => {
                    interpolated.push(quota.quota, quota.banner.toString());
                });
                data.addRow([str_date, ...interpolated]);
                */
                data.addRow([str_date, ...dates[date]])
            } catch (error) {
                console.log(error)
            }
        })

        // Chart options
        var options = {
            chart: {
                title: "Disponibilidad de cupos",
            },
            legend: {
                position: "top",
                alignment: "center",
            },
            width: 1000,
            height: 500,
            vAxis: { viewWindow: { min: 0 } },
            isStacked: true,
            bar: {
                groupWidth: 15,
            },
        }

        // Generate
        var chart = new google.charts.Line(document.getElementById("quotaChart"))
        google.visualization.events.addListener(chart, "error", error => {
            console.log(error)
            modal.html("No hay datos disponibles.")
        })
        chart.draw(data, google.charts.Line.convertOptions(options))
    }
    google.charts.load("current", { packages: ["line"] })
    google.charts.setOnLoadCallback(drawChart)

    ga_event("detail", { event_category: "follow", event_label: response.initials })
}
