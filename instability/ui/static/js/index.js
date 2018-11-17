window.onload = function() {
    var data = document.getElementById("data")
    var latencies = JSON.parse(data.dataset.latencies);
    var speeds = JSON.parse(data.dataset.speeds);
    var targets = data.dataset.targets.split(",");
    var period_start = data.dataset.start;
    var period_end = data.dataset.end

    var params = new URLSearchParams(window.location.search);

    var graph_max_latency = params.get("max_latency") || 100;

    var speed_chart = render_speed_graph(speeds)

    var period_control = flatpickr("#period-range", {
        enableTime: true,
        mode: "range",
        time_24hr: true,
        dateFormat: "Y-m-d H:i:S",
        defaultDate: [period_start, period_end]
    });

    var max_latency_control = document.getElementById("max-latency");
    max_latency_control.value = graph_max_latency;

    var update_report_button = document.getElementById("update-report-button");
    update_report_button.onclick = function() {
        var selectedDates = period_control.selectedDates;
        var start = selectedDates[0];
        var end = selectedDates[1];

        update_report_query(start, end, max_latency_control.value);
    };

    var charts = targets.map(target => {
        var chart = render_latency_graph(target, latencies[target], graph_max_latency);
        return chart;
    });
}

function update_report_query(start, end, max_latency) {
    if(start != null && end != null && max_latency != null) {
        var baseUrl = `${location.protocol}//${location.host}${location.pathname}`;
        var newUrl = `${baseUrl}?start=${start.toISOString()}&end=${end.toISOString()}&max_latency=${max_latency}`;

        location.href = newUrl;
    }
}

function render_speed_graph(speeds) {
    return new AmCharts.makeChart("speed", {
        "type": "serial",
        "dataProvider": speeds,
        "graphs": [
            {
                "id": "download",
                "balloonText": "Download: <b>[[value]]</b> Mbps",
                "title": "Download",
                "lineColor": "green",
                "valueField": "_download",
                "connect": false
            },
            {
                "id": "upload",
                "balloonText": "Upload: <b>[[value]]</b> Mbps",
                "title": "Upload",
                "lineColor": "blue",
                "valueField": "_upload",
                "connect": false
            }
        ],
        "categoryField": "_timestamp",
        "chartCursor": {
            "categoryBalloonDateFormat": "JJ:NN:SS, DD MMM",
            "cursorPosition": "mouse"
        },
        "legend": {
            "useGraphSettings": true
        },
        "categoryAxis": {
            "parseDates": true,
            "minPeriod": "hh"
        },
        "chartScrollbar": {
            "graph": "download",
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
        "valueAxes": [
            {
                "position": "left",
                "title": "Speed (Mbps)",
                "minimum": 0,
                "maximum": 300,
                "guides": [
                    {
                        "dashLength": 3,
                        "inside": true,
                        "lineColor": "green",
                        "label": "Down / Max",
                        "lineAlpha": 0.6,
                        "value": 200
                    },
                    {
                        "dashLength": 3,
                        "inside": true,
                        "lineColor": "blue",
                        "label": "Up / Max",
                        "lineAlpha": 0.6,
                        "value": 20
                    }
                ]
            }
        ]
    });
}

function render_latency_graph(target, latencies, graph_max_latency) {
    return new AmCharts.makeChart("target-" + target, {
        "type": "stock",
        "theme": "light",
        "categoryAxesSettings": {
            "minPeriod": "mm"
        },
        "dataSets": [
            {
                "fieldMappings": [
                    {
                        "fromField": "_average",
                        "toField": "average"
                    },
                    {
                        "fromField": "_maximum",
                        "toField": "maximum"
                    },
                    {
                        "fromField": "_minimum",
                        "toField": "minimum"
                    },
                    {
                        "fromField": "_loss",
                        "toField": "loss"
                    }
                ],
                "dataProvider": latencies,
                "categoryField": "_timestamp"
            }
        ],
        "panels": [
            {
                "title": "Latency",
                "percentHeight": 80,
                "stockGraphs": [
                    {
                        "id": "maximum",
                        "valueField": "maximum",
                        "fillAlphas": 0.4,
                        "hidden": true,
                        "balloonText": "<div>Maximum: <b>[[value]]</b> ms</div>",
                        "useDataSetColors": false,
                        "connect": false
                    },
                    {
                        "id": "average",
                        "valueField": "average",
                        "fillAlphas": 0.4,
                        "balloonText": "<div>Average: <b>[[value]]</b> ms</div>",
                        "useDataSetColors": false,
                        "connect": false
                    },
                    {
                        "id": "minimum",
                        "valueField": "minimum",
                        "fillAlphas": 0.4,
                        "hidden": true,
                        "balloonText": "<div>Minimum: <b>[[value]]</b> ms</div>",
                        "useDataSetColors": false,
                        "connect": false
                    }
                ],
                "stockLegend": {
                    "periodValueTextComparing": "[[percents.value.close]]%",
                    "periodValueTextRegular": "[[value.close]]"
                }
            },
            {
                "title": "Loss",
                "percentHeight": 20,
                "stockGraphs": [
                    {
                        "id": "loss",
                        "valueField": "loss",
                        "fillAlphas": 0.4,
                        "balloonText": "<div>Loss: <b>[[value]]</b>%</div>",
                        "useDataSetColors": false,
                        "connect": false
                    }
                ]
            }
        ],
        "chartScrollbarSettings": {
            "graph": "average",
            "usePeriod": "mm",
            "position": "top"
        },

        "chartCursorSettings": {
            "valueBalloonsEnabled": true
        },
        "periodSelector": {
            "position": "bottom",
            "dateFormat": "YYYY-MM-DD JJ:NN",
            "inputFieldWidth": 150,
            "periods": [
                {
                    "period": "hh",
                    "count": 1,
                    "label": "1 hour"
                },
                {
                    "period": "hh",
                    "count": 2,
                    "label": "2 hours"
                },
                {
                    "period": "hh",
                    "count": 5,
                    "label": "5 hour"
                },
                {
                    "period": "hh",
                    "count": 12,
                    "selected": true,
                    "label": "12 hours"
                },
                {
                    "period": "hh",
                    "count": 24,
                    "label": "24 hours"
                },
                {
                    "period": "MAX",
                    "label": "MAX"
                }
            ]
        },
        "panelsSettings": {
          "usePrefixes": true
        },
        "valueAxesSettings": {
            "minimum": 0,
            "maximum": graph_max_latency
        }
    });
}
