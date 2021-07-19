function timeline(container, dataset, width, height, interval, timeInterval, click) {
    let timeMax = 0
    let totMax = 0
    let padding = {
        top: 50,
        right: 50,
        bottom: 50,
        left: 50
    }
    let curTime = 0
    clock.pause = false;
    let data = d3.json("./static/json/timeline/Timeline.json")
    data.then(data => {
        timeMax = d3.max(data, d => d.time);
        totMax = d3.max(data, d => d.value);
        
        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        const xScale = d3.scaleLinear()
            .domain([0, timeMax])
            // .domain(data.map(item => item.time))
            .range([0, width - padding.left - padding.right])
        // .domain(['Mon06', 'Tue07', 'Wed08', 'Thur09', 'Fri10', 'Sat11'])
        const yScale = d3.scaleLinear()
            .domain([0, totMax])
            .range([height - padding.top - padding.bottom, 0])
        const xAxis = d3.axisBottom(xScale)
            .tickValues([0, 720, 1440, 2160, 2880, 3600, 4320, 5040, 5760, 6480, 7200])
            .tickFormat((d, i) => ['Mon06', '12PM', 'Tue07', '12PM', 'Wed08', '12PM', 'Thur09', '12PM', 'Fri10', '12PM', 'Sat11'][i])
        const yAxis = d3.axisLeft(yScale)

        svg.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
            .call(xAxis)
        const linePath = d3.line()
            .x(d => xScale(d.time))
            .y(d => yScale(d.value))
            .curve(d3.curveBasis)

        svg.append('path')
            .datum(data)
            .attr('class', 'line-path')
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .attr('d', linePath)
            .attr('fill', 'none')
            .attr('stroke-width', 1)
            .attr('stroke', 'rgba(255, 50, 50, 1)')
        const areaPath = d3.area()
            .x((d, i) => xScale(d.time))
            .y0((d, i) => yScale(d.value))
            .y1((d, i) => height - padding.bottom - padding.top)
        svg.append('path')
            .datum(data)
            .attr('class', 'line-path')
            .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
            .attr('d', areaPath)
            .attr('stroke-width', '3px')
            .attr('fill', 'rgba(255, 100, 100, 0.3)')

        let timeLine = svg.append("line")
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('x2', 0)
            .attr('y2', height - padding.bottom)
            .attr("stroke", 'rgba(0, 0, 0, 1)')
            .attr('transform', 'translate(' + (xScale(curTime) + padding.left) + ', 0)')
            .attr("fill", "none")
            .attr("stroke-width", 1)
        
        let timeLine5 = svg.append("line")
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('x2', 0)
            .attr('y2', height - padding.bottom)
            .attr("stroke", 'rgba(0, 0, 0, 1)')
            .attr("stroke-dasharray", "5, 5")
            .attr('transform', 'translate(' + (xScale(3770) + padding.left) + ', 0)')
            .attr("fill", "none")
            .attr("stroke-width", 1)

        let timeLine30 = svg.append("line")
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('x2', 0)
            .attr('y2', height - padding.bottom)
            .attr("stroke", 'rgba(0, 0, 0, 1)')
            .attr("stroke-dasharray", "5, 5")
            .attr('transform', 'translate(' + (xScale(5250) + padding.left) + ', 0)')
            .attr("fill", "none")
            .attr("stroke-width", 1)

        let hoverLine = svg.append("line")
            .attr('x1', 0)
            .attr('y1', 0)
            .attr('x2', 0)
            .attr('y2', height - padding.bottom)
            .attr("stroke", 'rgba(100, 100, 100, 0.5)')
            .attr("fill", "none")
            .attr("stroke-width", 1)
            .attr('visibility', 'hidden')
        clock.lineInterval = setInterval(() => {
            curTime += timeInterval
            timeLine.attr('transform', 'translate(' + (xScale(curTime) + padding.left) + ', 0)')
        }, interval)
        svg.on("mouseover", function (e) {
            let m = d3.pointer(e, this)
            if (m[0] < padding.left || m[0] > width - padding.right) return
            hoverLine.attr('visibility', 'visible')
            hoverLine.attr('transform', 'translate(' + m[0] + ', 0)')
        })
        svg.on("mouseout", function (e) {
            let m = d3.pointer(e, this)
            if (m[0] < padding.left || m[0] > width - padding.right) return
            hoverLine.attr('visibility', 'hidden')
            hoverLine.attr('transform', 'translate(' + m[0] + ', 0)')
        })
        svg.on("mousemove", function (e) {
            let m = d3.pointer(e, this)
            if (m[0] < padding.left || m[0] > width - padding.right) return
            hoverLine.attr('transform', 'translate(' + m[0] + ', 0)')
        })
        svg.on("click", function (e) {
            let m = d3.pointer(e, this)
            if (m[0] < padding.left || m[0] > width - padding.right) return
            timeLine.attr('transform', 'translate(' + m[0] + ', 0)')
            curTime = Math.floor((xScale.invert(m[0] - padding.left)) / 5) * 5
            click(curTime)
        })

    })
    // let data = []
    // dataset.forEach((v, i) => {
    //     let tmp = {
    //         time: dataset[i].time,
    //         tot: 0
    //     }
    //     for (a in dataset[i].total.children)
    //         for (b in dataset[i].total.children[a].children)
    //             tmp.tot += dataset[i].total.children[a].children[b].value
    //     data.push(tmp)
    // })
    // const xScale = d3.scaleBand()
    
    // svg.append('g')
    //     .attr('class', 'axis')
    //     .attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
    //     .call(yAxis)
    // console.log(d3)
        // })
}
