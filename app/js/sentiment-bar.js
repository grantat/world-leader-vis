// 'use strict'; // Variable declaration

function sentimentBarChart(filename){
    var margin = {
        top: 20,
        bottom: 40,
        right: 100,
        left: 100
    };
    var height = $(".bottom-left-vis").height() - margin.top - margin.bottom;
    var width = $(".bottom-left-vis").width() - margin.left - margin.right;

    // reset section/char
    $(".bottom-left-vis").html("");

    // Add svg to
    var svg = d3.select('.bottom-left-vis').
    append('svg').
    attr('width', width + margin.left + margin.right).
    attr('height', height + margin.top + margin.bottom).
    append('g').
    attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // X scale
    var x = d3.scaleLinear().
    range([0, width]);
    var y = d3.scaleBand().
    rangeRound([height, 0]);

    var xAxis = d3.axisTop(x);
    var yAxis = d3.axisLeft(y).
    tickSize(6, 0);

    d3.json(filename, function(error, data) {
        if (error) throw error;

        var newdata = {}, finaldata = [];
        data.forEach(function(val) {
            if(!newdata[val.username]){
                newdata[val.username] = {
                    "sentiment_vals": [],
                    "profile_pic": val.profile_pic
                }
            }
            newdata[val.username].sentiment_vals.push(parseFloat(val.sentiment));
        });

        for(var p in newdata){
            finaldata.push({"username": p, "profile_pic": newdata[p].profile_pic, "sentiment": (newdata[p].sentiment_vals.reduce(add, 0) / newdata[p].sentiment_vals.length)})
        }
        
        addProfileImages(finaldata)
        data = finaldata;

        x.domain(d3.extent(data, function(d) {
            return d.sentiment;
        })).nice();
        y.domain(data.map(function(d) {
            return d.username;
        }));

        svg.selectAll('.bar').
        data(data).
        enter().append('rect').
        attr('class', function(d) {
            return "bar bar--" + (d.sentiment < 0 ? "negative" : "positive");
        }).
        attr('x', function(d) {
            return x(Math.min(0, d.sentiment));
        }).
        attr('y', function(d) {
            return y(d.username);
        }).
        attr('width', function(d) {
            return Math.abs(x(d.sentiment) - x(0));
        }).
        attr('height', 6);

        svg.append('g').
        attr('class', 'x axis').
        attr('transform', 'translate(0,' + height + ')').
        call(xAxis);

        var tickNegative = svg.append('g').
        attr('class', 'y axis').
        attr('transform', 'translate(' + x(0) + ',0)').
        call(yAxis).
        selectAll('.tick').
        filter(function(d, i) {
            return data[i].sentiment < 0;
        });

        tickNegative.select('line').
        attr('x2', 6);

        tickNegative.select('text').
        attr('x', 9).
        style('text-anchor', 'start');
    });
}

function type(d) {
    d.sentiment = +d.sentiment;
    return d;
}

function add(a, b) {
    return a + b;
}

function imgError(image) {
    image.onerror = "";
    image.src = "assets/imgs/default_img.jpg";
    return true;
}

function addProfileImages(data){
    var html = "";

    for(user in data){
        html += '<a target="_blank" href="https://twitter.com/'+data[user].username+'">';
        html += '<img id="user-'+data[user].username+'" class="profile-img" src="'+data[user].profile_pic+'" onerror="imgError(this)">';
        html += '</a>';
    }
    $("#mCSB_1").html(html);
}

// call

// sentimentBarChart("../../data/chunks/2017-10.json");
