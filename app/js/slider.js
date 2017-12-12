
function sideBarchart(){
    // bar chart located on the right side inside the sidebar.
    // used to show the total number of tweets per month.
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
