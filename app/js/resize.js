// window size
var w = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    x = w.innerWidth || e.clientWidth || g.clientWidth,
    y = w.innerHeight|| e.clientHeight|| g.clientHeight;

// sidebar_size static
var sidebar_width = 294;

// top_vis_width = screen_size - sidebar_vis_widths
var top_vis_width = w.x - 294;

$(".top-vis").width(top_vis_width);
// bottom left/right widths = 0.5 * top_vis_width
$(".bottom-left-vis, .bottom-right-vis").width(0.5 * top_vis_width);
