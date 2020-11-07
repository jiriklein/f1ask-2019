$(document).ready(function(){
    function createGauge() {
        var opts = {
            angle: -0.2, // The span of the gauge arc
            lineWidth: 0.2, // The line thickness
            radiusScale: 1, // Relative radius
            pointer: {
                length: 0.6, // // Relative to gauge radius
                strokeWidth: 0.035, // The thickness
                color: '#000000' // Fill color
            },
            limitMax: false,     // If false, max value increases automatically if value > maxValue
            limitMin: false,     // If true, the min value of the gauge will be fixed
            colorStart: '#6F6EA0',   // Colors
            colorStop: '#C0C0DB',    // just experiment with them
            strokeColor: '#EEEEEE',  // to see which ones work best for you
            generateGradient: true,
            highDpiSupport: true,     // High resolution support
        };

        var target = document.getElementById('preview'); // your canvas element
        var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
        gauge.maxValue = 350; // set max gauge value
        gauge.minValue = 0;  // Prefer setter over gauge.minValue = 0
        gauge.animationSpeed = 32; // set animation speed (32 is default value)
        gauge.set(0);
        return gauge
    }

    function createGraph() {
        // create starting graph data + conf
        var graph_data = [{
            y: [0],
            mode: 'lines',
            line: {color: '#80caf6'}
        }]
        Plotly.plot('graph', graph_data);
    }

    // connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    gg = createGauge()
    createGraph()

    // var cnt = 0;

    // receive details from server
    socket.on('f1', function(msg) {
        // console.log("Received number" + msg.data);
        // maintain a list of a few numbers
        if (numbers_received.length >= 4){
            numbers_received.shift()
        }
        numbers_received.push(msg.data);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }

        // update the graph
        // var addView = {
        //   xaxis: {
        //     range: [0, ++cnt]
        //   }
        // };
        //
        // var update = {
        //   x:  [[cnt]],
        //   y: [[msg.data]]
        // };

        // apply changes
        // Plotly.relayout('graph', addView);
        // Plotly.extendTraces('graph', update, [0])
        Plotly.extendTraces('graph', {
            y: [[msg.data]]
        }, [0])

        $('#log').html(numbers_string);
        gg.set(msg.data);

    });
});