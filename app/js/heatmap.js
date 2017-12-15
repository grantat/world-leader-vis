
var margin = {
        top: 50,
        right: 0,
        bottom: 40,
        left: 30
    },
    width = $(".bottom-right-vis").width() - margin.left - margin.right,
    height = $(".bottom-right-vis").height() - margin.top - margin.bottom,
    // width = 860 - margin.left - margin.right,
    // height = 430 - margin.top - margin.bottom,
    gridSize = Math.floor(width / 24),
    legendElementWidth = gridSize * 2,
    buckets = 9,
    colors = ["#ffffd9", "#edf8b1", "#c7e9b4", "#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8", "#253494", "#081d58"],
    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
    times = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"];

var svg = d3.select(".bottom-right-vis svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("text")
      .attr("class", "title")
      .attr("x", width/2)
      .attr("y", 0 - (margin.top / 2) - 8)
      .attr("text-anchor", "middle")
      .attr("style", "")
      .text("Tweet Times Heatmap");

var dayLabels = svg.selectAll(".dayLabel")
    .data(days)
    .enter().append("text")
    .text(function(d) {
        return d;
    })
    .attr("x", 0)
    .attr("y", (d, i) => i * gridSize)
    .style("text-anchor", "end")
    .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
    .attr("class", (d, i) => ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"));

var timeLabels = svg.selectAll(".timeLabel")
    .data(times)
    .enter().append("text")
    .text((d) => d)
    .attr("x", (d, i) => i * gridSize)
    .attr("y", 0)
    .style("text-anchor", "middle")
    .attr("transform", "translate(" + gridSize / 2 + ", -6)")
    .attr("class", (d, i) => ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"));

var type = (d) => {
    return {
        day: +d.day,
        hour: +d.hour,
        value: +d.value
    };
};

var heatmapChart = function(csvFile) {
    d3.csv(csvFile, type, (error, data) => {
        var colorScale = d3.scaleQuantile()
            .domain([0, buckets - 1, d3.max(data, (d) => d.value)])
            .range(colors);

        var cards = svg.selectAll(".hour")
            .data(data, (d) => d.day + ':' + d.hour);

        cards.append("title");

        cards.enter().append("rect")
            .attr("x", (d) => (d.hour) * gridSize)
            .attr("y", (d) => (d.day - 1) * gridSize)
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("class", "hour bordered")
            .attr("width", gridSize)
            .attr("height", gridSize)
            .style("fill", colors[0])
            .merge(cards)
            .on('mouseover', rectMouseover)
            .on('mouseout', rectHideMouseover)
            .transition()
            .duration(1000)
            .style("fill", (d) => colorScale(d.value));

        cards.select("title").text((d) => d.value);

        cards.exit().remove();

        var legend = svg.selectAll(".legend")
            .data([0].concat(colorScale.quantiles()), (d) => d);

        var legend_g = legend.enter().append("g")
            .attr("class", "legend");

        legend_g.append("rect")
            .attr("x", (d, i) => legendElementWidth * i)
            .attr("y", gridSize * 7 + 30)
            .attr("width", legendElementWidth)
            .attr("height", gridSize / 2)
            .style("fill", (d, i) => colors[i]);

        legend_g.append("text")
            .attr("class", "mono")
            .text((d) => "≥ " + Math.round(d))
            .attr("x", (d, i) => legendElementWidth * i)
            .attr("y", gridSize * 8 + 30);

        legend.exit().remove();
    });
};

function rectMouseover(d){
    // change outline to indicate hover state.
    d3.select(this).attr('stroke', 'black');
    var pics = '';

    var content = '<span class="name">Count: </span><span class="value">' +
                  d.value +
                  '</span><br/>';

    tp.showTooltip(content, d3.event);
}

function rectHideMouseover(d) {
  // reset outline
  tp.hideTooltip();
}


// heatmapChart("../../data/heatmap/2017-10.csv");
