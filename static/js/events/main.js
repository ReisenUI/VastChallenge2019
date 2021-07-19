function Event(container, width, height, color) {
    let typeProjection = [
        "earthquake",
        "shelter",
        "distribution",
        "school",
        "transportation",
        "gas",
        "water/sewer/flood",
        "food",
        "power",
        "emergency",
        "communication",
        "social"
    ]
    let data = d3.json("./static/json/events/data.json")
    data.then(data => {
        let padding = {
            top: 50,
            right: 100,
            bottom: 50,
            left: 100
        }
        let timeMax = d3.max(data, d => d.time)
        let typeMax = d3.max(data, d => d.type)
        const xScale = d3.scaleLinear()
            .domain([0, timeMax])
            .range([0, width - padding.left - padding.right])
        const xAxis = d3.axisBottom(xScale)
            .tickValues([0, 720, 1440, 2160, 2880, 3600, 4320, 5040, 5760, 6480, 7200])
            .tickFormat((d, i) => ['Mon06', '12PM', 'Tue07', '12PM', 'Wed08', '12PM', 'Thur09', '12PM', 'Fri10', '12PM', 'Sat11'][i])
        const yScale = d3.scaleLinear()
            .domain([-1, typeMax])
            .range([height - padding.top - padding.bottom, 0])
        const yAxis = d3.axisLeft(yScale)
            .tickValues([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            .tickFormat((d, i) => typeProjection[i])
        let svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .call(yAxis)
        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
            .call(xAxis)
        let hover = d3.select('#hover')
        let body = d3.select('#body')
        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .attr("cx", function (d) {
                return xScale(d.time)
            })
            .attr("cy", function (d) {
                return yScale(d.type)
            })
            .attr("r", function (d) {
                return '10'
            })
            .attr("fill", function (d) {
                return color[d.type];
            })
            .attr("opacity", 0.5)
            .on('mouseover', function (e, d) {
                let m = d3.pointer(e, body)
                hover.style('left', m[0] + 'px')
                    .style('top', m[1] + 'px')
                    .style('display', 'block')
                    .html(d.message)
            })
            .on('mousemove', function (e, d) {
                let m = d3.pointer(e, body)
                hover.style('left', m[0] + 'px')
                    .style('top', m[1] + 'px')
            })
            .on('mouseout', function (e) {
                hover.style('display', 'none')
            })
    })
}
