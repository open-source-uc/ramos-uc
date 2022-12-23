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
    let categories_keys = new Set();
    let categories = {};

    response.quota.forEach(({ category }) => {
        categories_keys.add(category);
    });

    categories_keys.forEach(category => {
        categories[category] = [];
    });

    response.quota.forEach(({ category, date, quota, banner }) => {
        categories[category].push({
            date: new Date(date),
            quota: quota,
            banner: banner,
            category: category
        });
    });

    categories_keys = Array.from(categories_keys);

    const data = [];
    categories_keys.forEach(category => {
        data.push(categories[category])
    });

    // Create the visualization using D3.js
    //npm install d3
    const d3 = require('d3');

    const WIDTH = 1000,
        HEIGHT = 500;

    const margins = {
        top: 63.5,
        left: 45.5,
        bottom: 52.5,
        right: 357.5
    };

    const width = WIDTH - margins.left - margins.right,
        height = HEIGHT - margins.top - margins.bottom;

    const divQuotaChart = d3.select("#quotaChart");

    const lineChart = divQuotaChart
        .append("svg")
        .attr("width", WIDTH)
        .attr("height", HEIGHT);

    lineChart
        .append("text")
        .attr("font-size", 16)
        .attr("fill", "#757575")
        .attr("x", margins.left/3)
        .attr("y", margins.top*3/4)
        .text("Disponibilidad de cupos");

    lineChart
        .append("text")
        .attr("font-size", 16)
        .attr("fill", "#757575")
        .attr("x", margins.left + width/2)
        .attr("y", HEIGHT - margins.bottom/5)
        .text("Fechas y horarios")
        .attr("text-anchor", "middle");

    const maxQuota = categories_keys.map(category => categories[category].map(d => d.quota).reduce((a, b) => Math.max(a, b), 0)).reduce((a, b) => Math.max(a, b), 0);

    const sortedDates = categories[categories_keys[0]].map(d => d.date).sort((a, b) => a - b);
    const firstDate = sortedDates[0],
        lastDate = sortedDates[sortedDates.length - 1];

    const quotaScale = d3
        .scaleLinear()
        .domain([0, maxQuota])
        .range([height, 0])
        .nice();

    const timeScale = d3
        .scaleTime()
        .domain([firstDate, lastDate])
        .range([0, width])
        .nice();

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    const axisQuota = d3.axisLeft(quotaScale);
    const containerAxisQuota = lineChart
        .append("g")
        .attr("transform", `translate(${margins.left}, ${margins.top})`)
        .call(axisQuota);

    containerAxisQuota
        .selectAll(".tick")
        .select("line")
        .attr("x1", width)
        .attr("stroke-dasharray", "8")
        .attr("opacity", 0.5)
        .attr("stroke", "#757575");

    containerAxisQuota
        .selectAll(".tick")
        .select("text")
        .attr("font-size", 12)
        .attr("fill", "#757575");

    const axisDates = d3.axisBottom(timeScale);
    lineChart
        .append("g")
        .attr("transform", `translate(${margins.left}, ${height + margins.top})`)
        .call(axisDates);

    const drawLines = d3
        .line(d3.curveStepAfter)
        .x((d) => timeScale(d.date))
        .y((d) => quotaScale(d.quota));

    const linesContainer = lineChart
        .append("g")
        .attr("transform", `translate(${margins.left}, ${margins.top})`);

    const circlesContainer = lineChart
        .append("g")
        .attr("transform", `translate(${margins.left}, ${margins.top})`);

    const captionSquaresContainer = lineChart
        .append("g")
        .attr("transform", `translate(${margins.left + width}, ${margins.top})`);

    const captionTextContainer = lineChart
        .append("g")
        .attr("transform", `translate(${margins.left + width}, ${margins.top})`);

    const highlight = (dato) => {
        linesContainer
            .selectAll("path")
            .attr("stroke-opacity", d => d == dato ? 1 : 0.3)
            .transition()
            .duration(500)
            .attr("stroke-width", d => d == dato ? 5 : 2.4);

        captionSquaresContainer
            .selectAll("rect")
            .attr("fill-opacity", d => d == dato ? 1 : 0.3);

        captionTextContainer
            .selectAll("text")
            .attr("fill-opacity", d => d == dato ? 1 : 0.3);

        circlesContainer
            .selectAll("circle")
            .data(dato)
            .join(
                enter => {
                    enter
                        .append("circle")
                        .attr("cx", d => timeScale(d.date))
                        .attr("cy", d => quotaScale(d.quota))
                        .attr("fill", d => colorScale(d.category))
                        .attr("r", 0)
                        .transition()
                        .duration(500)
                        .attr("r", 5);
                },
                update => {
                    update
                        .attr("cx", d => timeScale(d.date))
                        .attr("cy", d => quotaScale(d.quota))
                        .attr("fill", d => colorScale(d.category))
                        .attr("r", 0)
                        .transition()
                        .duration(500)
                        .attr("r", 5);

                },
                exit => {
                    exit
                        .transition()
                        .duration(500)
                        .attr("r", 0)
                        .remove();
                }
            );

        circlesContainer
            .selectAll("circle")
            .on("mouseenter", (event, dato) => {
                console.log(dato)
                circlesContainer
                    .selectAll("circle")
                    .transition()
                    .duration(500)
                    .attr("r", d => d == dato ? 5 : 0)
            });
    };

    const unhighlight = () => {
        linesContainer
            .selectAll("path")
            .attr("stroke-opacity", 1)
            .transition()
            .duration(500)
            .attr("stroke-width", 2.4);

        captionSquaresContainer
            .selectAll("rect")
            .attr("fill-opacity", 1);

        captionTextContainer
            .selectAll("text")
            .attr("fill-opacity", 1);
    };

    linesContainer
        .selectAll("path")
        .data(data)
        .join(
            (enter) => {
                enter.append("path")
                    .attr("stroke", d => colorScale(d[0].category))
                    .attr("fill", "transparent")
                    .attr("stroke-width", 2.4)
                    .attr("d", d => drawLines(d))
                    .on("mouseenter", (event, dato) => highlight(dato))
                    .on("mouseleave", unhighlight);
            }
        );

    lineChart
        .append("rect")
        .attr("width", WIDTH)
        .attr("height", HEIGHT)
        .attr("fill", "transparent")
        .lower()
        .on("mouseenter", () => {
            circlesContainer
                .selectAll("circle")
                .transition()
                .duration(500)
                .attr("r", 0);
        });


    captionSquaresContainer
        .selectAll("rect")
        .data(data)
        .join(
            (enter) => {
                enter
                    .append("rect")
                    .attr("width", 12)
                    .attr("height", 12)
                    .attr("fill", d => colorScale(d[0].category))
                    .attr("x", 30)
                    .attr("y", (_, i) => 50 + i * 50)
                    .attr("ry", 2)
                    .on("mouseenter", (event, dato) => highlight(dato))
                    .on("mouseleave", unhighlight)
            }
        );

    captionTextContainer
        .selectAll("rect")
        .data(data)
        .join(
            (enter) => {
                enter.append("text")
                    .attr("x", 30 + 20)
                    .attr("y", (_, i) => 50 + 12 + i * 50)
                    .text(d => d[0].category)
                    .attr("fill", "#757575")
                    .on("mouseenter", (event, dato) => highlight(dato))
                    .on("mouseleave", unhighlight)
            }
        )
}
