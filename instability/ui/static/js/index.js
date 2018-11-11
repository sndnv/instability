window.onload = function() {
    var data = document.getElementById("data")
    var latencies = JSON.parse(data.dataset.latencies);
    var targets = data.dataset.targets.split(",");
    var graph_max_latency = 100; // TODO

    var charts = targets.map(target => {
        var chart = render_latency_graph(target, latencies[target], graph_max_latency);
        chart.addListener("zoomed", syncZoom);
        chart.addListener("changed", syncCursor);
        return chart;
    });

    function syncZoom(event) {
        for (x in charts) {
            if (charts[x].ignoreZoom) {
                charts[x].ignoreZoom = false;
            }
            if (event.chart != charts[x]) {
                charts[x].ignoreZoom = true;
                charts[x].zoomToDates(event.startDate, event.endDate);
            }
        }
    }

    function syncCursor(event) {
        if (!isNaN(event.index)) {
            for (x in charts) {
                charts[x].chartCursor.showCursorAt(charts[x].chartData[event.index].time);
            }
        } else {
            for (x in charts) {
                  charts[x].chartCursor.forceShow = false;
                  charts[x].chartCursor.hideCursor(false);
            }
        }
    }
}

function render_latency_graph(target, latencies, graph_max_latency) {
    return new AmCharts.makeChart("target-" + target, {
        "type": "serial",
        "titles": [
            {
                "text": target,
                "size": 15
            }
        ],
        "dataDateFormat": "YYYY-MM-DD JJ:NN:SS",
        "dataProvider": latencies,
        "graphs": [
            {
                "id": "minimum",
                "title": "Minimum",
                "hidden": true,
                "valueAxis": "latency",
                "fillAlphas": 0.4,
                "valueField": "_minimum",
                "balloonText": "<div style='margin:5px;'>Minimum: <b>[[value]]</b> ms</div>"
            },
            {
                "id": "maximum",
                "title": "Maximum",
                "hidden": true,
                "valueAxis": "latency",
                "fillAlphas": 0.4,
                "valueField": "_maximum",
                "balloonText": "<div style='margin:5px;'>Maximum: <b>[[value]]</b> ms</div>"
            },
            {
                "id": "average",
                "title": "Average",
                "valueAxis": "latency",
                "fillAlphas": 0.4,
                "valueField": "_average",
                "balloonText": "<div style='margin:5px;'>Average: <b>[[value]]</b> ms</div>"
            },
            {
                "id": "loss",
                "title": "Loss",
                "valueAxis": "loss",
                "lineColor": "#FF6600",
                "valueField": "_loss",
                "balloonText": "<div style='margin:5px;'>Loss: <b>[[value]]</b>%</div>"
            }
        ],
        "chartScrollbar": {
            "graph": "average",
            "scrollbarHeight": 40,
            "backgroundAlpha": 0,
            "selectedBackgroundAlpha": 0.1,
            "selectedBackgroundColor": "#888888",
            "graphFillAlpha": 0,
            "graphLineAlpha": 0.5,
            "selectedGraphFillAlpha": 0,
            "selectedGraphLineAlpha": 1,
            "autoGridCount": true,
            "color": "#AAAAAA"
        },
        "categoryField": "_timestamp",
        "chartCursor": {
            "categoryBalloonDateFormat": "JJ:NN:SS, DD MMM",
            "cursorPosition": "mouse"
        },
        "valueAxes": [
            {
                "id": "latency",
                "position": "left",
                "title": "Latency (ms)",
                "minimum": 0,
                "maximum": graph_max_latency
            },
            {
                "id": "loss",
                "position": "right",
                "title": "Loss (%)",
                "minimum": 0,
                "maximum": 100
            }
        ],
        "legend": {
            "useGraphSettings": true
        },
        "categoryAxis": {
            "parseDates": true,
            "minPeriod": "ss"
        },
        "pathToImages": "static/libs/amcharts/images/"
    });
}
