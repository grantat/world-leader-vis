
function sideBarchart(){
    // bar chart located on the right side inside the sidebar.
    // used to show the total number of tweets per month.
    var meta_margin = {top: 35, right: 0, bottom: 20, left: 0},
        meta_width = 260 - meta_margin.left - meta_margin.right,
        meta_height = 150 - meta_margin.top - meta_margin.bottom;

    var x = d3.scaleBand()
      .range([0, meta_width])
      .padding(0.15);

    var y = d3.scaleLinear()
        .rangeRound([meta_height, 0]);


    var svg = d3.select('#taVis').append("svg")
        .attr("width", meta_width + meta_margin.left + meta_margin.right)
        .attr("height", meta_height + meta_margin.top + meta_margin.bottom)
      .append("g")
        .attr("transform", "translate(" + meta_margin.left + "," + meta_margin.top + ")");

    var sidebar_chart = svg.append("g");

    // Horizontal grid
    sidebar_chart.append("g")
      .attr("class", "grid horizontal");

    var xAxis = d3.axisBottom(x)
        .tickSize(2, 0)
        // .tickFormat(formatDate);

    var yAxis = d3.axisLeft(y)
        .ticks(3)
        .tickFormat(function(d) { return "+" + d; });

    sidebar_chart.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(-8," + 0 + ")");

    // #848a8d
    var data = [];
    tweet_counts.forEach(function(val, i){
        data.push({"ind": i, "val": val});
    });

    // tweet_counts
    console.log(tweet_counts);
    x.domain(data.map(function(d) { return d.ind; }));
    y.domain([0, d3.max(data, function(d) { return d.val })]);

    // update axis
    sidebar_chart.select(".grid").call(d3.axisLeft(y)
      .tickSize(-(meta_width), 0, 0)
      .ticks(3)
      .tickFormat("")
    );
    sidebar_chart.select(".y.axis").call(yAxis);

    // select all bars and append an item per date
    var bars = sidebar_chart.selectAll(".bar")
                .data(data);

    // initial enter bar
    bars.enter()
      // .append("g")
      //   .attr("class", "bar")
      //   .attr("transform", function(d) { return "translate(" + x(d.ind) + ",0)"; })
      .append("rect")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d.ind) + ","+ (y(d.val) - meta_height) +")"; })
        .attr("width", x.bandwidth())
        .attr("x", 0)
        .attr("y", function(d) {  return y(d.val); })
        .attr("height", function(d) {  return y(d.val); })
        .style("fill", "#65aed6")
        .style("opacity", 1);

}

// Create a new date from a string, return as a timestamp.
function timestamp(str){
    return new Date(str).getTime();
}

function makeSlider(){
    // Created using UISlider - https://refreshless.com/nouislider/
    var sliderValMax = y.length - 1;
    var slider = document.getElementById('slider');
    noUiSlider.create(slider, {
    	start: sliderValMax,
    	step: 1,
    	connect: "lower",
    	format: wNumb({ decimals: 0 }),
    	range: { 'min': 0, 'max': sliderValMax },
        pips: {
    		mode: 'steps',
    		density: 3,
    		format: wNumb({
    			decimals: 2,
    			prefix: '$'
    		})
    	}
    });

    slider.noUiSlider.pips({
    	mode: 'values',
    	values: [0,12,24,36,48,60,72,84,94, 106],
    	format: wNumb({
    		encoder: function( a ){
        		return parseInt(y[parseInt(a)].substring(0,4));
    		}
    	}),
    	density: 4
    });

    slider.noUiSlider.on('slide', function(v, e){
        updateCurrentYear(v);
    });

    slider.noUiSlider.on('set', function(v, e){
	  // change year
	  updateCurrentYear(v);
	  // draw update
	  update();
    });
}

// Change the year on slide
function updateCurrentYear(s) {
    // update iter val for update menu
    iter = parseInt(s);
    console.log(iter);
	var currentMonth = y[iter].split("-");
	$('.currentYear').text(currentMonth[1]+ "/" + currentMonth[0]);
}
