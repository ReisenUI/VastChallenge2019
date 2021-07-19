function LineChart(container, width, height, color) {
    let padding = {
        top: 50,
        right: 50,
        bottom: 50,
        left: 70
    }
    let data = d3.json("./static/json/lineChart/data.json")
    data.then(data => {
        let maxValue = 1078456.85
        let maxTime = 7200

        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        const xScale = d3.scaleLinear()
            .domain([0, maxTime])
            .range([0, width - padding.left - padding.right])
        const xAxis = d3.axisBottom(xScale)
            .tickValues([0, 720, 1440, 2160, 2880, 3600, 4320, 5040, 5760, 6480, 7200])
            .tickFormat((d, i) => ['Mon06', '12PM', 'Tue07', '12PM', 'Wed08', '12PM', 'Thur09', '12PM', 'Fri10', '12PM', 'Sat11'][i])
        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
            .call(xAxis)
        const yScale = d3.scaleLinear()
            .domain([0, maxValue])
            .range([height - padding.top - padding.bottom, 0])
        const yAxis = d3.axisLeft(yScale)
        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .call(yAxis)
        const linePath = d3.line()
            .x(d => xScale(d.time))
            .y(d => yScale(d.value))
            .curve(d3.curveBasis)
        for (let item in data) {
            svg.append('path')
                .datum(data[item])
                .attr('class', 'line-path')
                .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
                .attr('d', linePath)
                .attr('fill', 'none')
                .attr('stroke-width', 1)
                .attr('stroke', () => color(item))
        }
    })
}