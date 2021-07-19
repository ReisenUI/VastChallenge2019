function ScatterPlot(container, width, height, maxRange) {
    let color = ['#2F96E0', '#B23CB2', '#EE4395', '#AFF05B', '#D9C231', '#5465D6']
    let data = d3.json("./static/json/scatterPlot/data.json")
    data.then(data => {
        let padding = {
            top: 30,
            right: 50,
            bottom: 50,
            left: 90
        }
        let timeMax = d3.max(data, d => d.time)
        let valueMax = d3.max(data, d => d.value)
        const xScale = d3.scaleLinear()
            .domain([0, timeMax])
            .range([0, width - padding.left - padding.right])
        const xAxis = d3.axisBottom(xScale)
            .tickValues([0, 720, 1440, 2160, 2880, 3600, 4320, 5040, 5760, 6480, 7200])
            .tickFormat((d, i) => ['Mon06', '12PM', 'Tue07', '12PM', 'Wed08', '12PM', 'Thur09', '12PM', 'Fri10', '12PM', 'Sat11'][i])
        const range = d3.scaleLinear()
            .domain([0, Math.log2(valueMax + 1)])
            .range([0, 10])
        const yScale = d3.scaleLinear()
            .domain([0, 19 * 6 - 1])
            .range([height - padding.top - padding.bottom, 0])
        const yAxis = d3.axisLeft(yScale)
            .tickValues([3, 9, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117])
            // 下面这行 y 轴的标签
            .tickFormat((d, i) => ['Palace Hills', 'Northwest', 'Old Town', 'Safe Town', 'Southwest', 'Downtown',
                                   'Wilson Forest', 'Scenic Vista', 'Broadview', 'Chapparal', 'Terrapin Springs',
                                   'Pepper Mill', 'Cheddarford', 'Easton', 'Weston', 'Southton', 'Oak Willow',
                                   'East Parton', 'West Parton'][i])
        let svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .attr("cx", function (d) {
                return xScale(d.time)
            })
            .attr("cy", function (d) {
                return yScale((d.location - 1) * 6 + d.tag)
            })
            .attr("r", function (d) {
                return range(Math.log2(d.value + 1))
            })
            .attr("fill", function (d) {
                return color[d.tag]
            })
            .attr("opacity", 0.3)

        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
            .call(xAxis)
        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .call(yAxis)
    })
}
