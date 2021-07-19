async function MobileSensor(container, width, height, color){
    let MapContainer = {};
    let padding = {
        top: 50,
        right: 50,
        bottom: 50,
        left: 50
    }

    let dataHimark = d3.json("./static/json/geoJson/StHimark.json");
    dataHimark.then(data=>{
        MapContainer.projection = d3.geoMercator()
            .translate([width / 2, height / 2])
            .center([-119.8356755, 0.122555])
            .scale(150000);
        MapContainer.path = d3.geoPath()
            .projection(MapContainer.projection)
        MapContainer.svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        MapContainer.geoRootMap = topojson.feature(data, data.objects.StHimark)

        MapContainer.regions = MapContainer.svg.selectAll("g")
            .data(MapContainer.geoRootMap.features)
            .enter()
            .append("g")
            .attr("class", ()=>{
                return 'regions';
            })

        MapContainer.paths = MapContainer.regions.append("path")
            .attr("class", d=>{
                return 'paths ' + d.properties.nbrhood.replace(" ", "");
            })
            .attr("fill", 'grey')
            .attr("d", MapContainer.path)
            .style("stroke-width", 3)
            .style("stroke", "white")

        MapContainer.coordProjection = function(d){
            return MapContainer.projection(d);
        }
    })

    let dataBridge = d3.json("./static/json/geoJson/bridges.json");
    dataBridge.then(data=>{
        MapContainer.bridgeGeoRoot = topojson.feature(data, data.objects.bridges);

        let boundary = topojson.mesh(data, data.objects.bridges);

        MapContainer.svg
            .append("path")
            .datum(boundary)
            .attr("fill", "none")
            .style("stroke", "black")
            .style("stroke-width", 3)
            .attr("d", MapContainer.path);
    })

    let dataPath = d3.json("./static/json/driver/MC2path.json")
    await dataPath.then(data=>{
        MapContainer.dataset = data;
    })

    return MapContainer
}