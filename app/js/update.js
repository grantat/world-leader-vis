
// init reused vars - y is (%Y-%m) list
var y = [],
    tweet_counts = [],
    current_month = "",
    iter = 0,
    refreshIntervalId = 0,
    slider = document.getElementById('slider');;

function drawGraphs(){
    // update sentiment-bar, heatmap, clusters, sidebar items
    heatmapChart("../data/heatmap/"+y[iter]+".csv");
    sentimentBarChart("../data/chunks/"+y[iter]+".json");
    // bubble chart
    d3.json("../data/clusters/"+y[iter]+".json", display);
    // set tweet counts
    $("#showCurrent .num").html(tweet_counts[iter]);
}

// get data
$.get( "../data/date-ranges.json", function( data ) {
	for(year in data){
		for(range in data[year]){
			y.push(data[year][range].title);
			tweet_counts.push(data[year][range].count);
		}
	}
    console.log(data);
    // start last entry
    iter = y.length - 1;
    current_month = y[iter];
    drawGraphs();
    // draw slider and side barchart
    sideBarchart();
    makeSlider();
});

function update(){
    drawGraphs();
    var month = y[iter].split("-");
    $(".currentYear").html(month[1]+ "/" + month[0]);
}

function autoUpdate(){
    // For the play button interval function
    // go left with index
    iter -= 1;
    if ( y[iter] === void 0 ) {
        iter = y.length - 1;
    }

    // use on `set` call for nouUislider to update
    slider.noUiSlider.set(iter);
}

// step functions - prev/next buttons
$("#prev, #next").click(function(){
    if(this.id == "prev"){
        // go left with index
        iter -= 1;
        if ( y[iter] === void 0 ) {
            iter = y.length - 1;
        }
    }else{
        // go right with index
        iter += 1;
        if ( y[iter] === void 0 ) {
            iter = 0;
        }
    }
    // if the play button is active, restart interval of playing
    if ($("#play").hasClass("play")){
        clearInterval(refreshIntervalId);
        refreshIntervalId = setInterval(autoUpdate, 3000);
    }
    // use on `set` call for nouUislider to update
    slider.noUiSlider.set(iter);
});


// play button
$("#play").click(function(){
    if (!$("#play").hasClass("play")){
        refreshIntervalId = setInterval(autoUpdate, 3000);
        $("#play span").addClass("icon-pause");
        $("#play span").removeClass("icon-play");
    }else{
        clearInterval(refreshIntervalId);
        $("#play span").addClass("icon-play");
        $("#play span").removeClass("icon-pause");
    }
    $("#play").toggleClass("play");
});
