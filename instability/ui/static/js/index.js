window.onload = function() {
    var data = document.getElementById("data")
    var latencies = JSON.parse(data.dataset.latencies);
    var targets = data.dataset.targets.split(",");
    var graph_max_latency = 100; // TODO

    var charts = targets.map(target => {
        var chart = render_latency_graph(target, latencies[target], graph_max_latency);
        return chart;
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
                        "useDataSetColors": false
                    },
                    {
                        "id": "average",
                        "valueField": "average",
                        "fillAlphas": 0.4,
                        "balloonText": "<div>Average: <b>[[value]]</b> ms</div>",
                        "useDataSetColors": false
                    },
                    {
                        "id": "minimum",
                        "valueField": "minimum",
                        "fillAlphas": 0.4,
                        "hidden": true,
                        "balloonText": "<div>Minimum: <b>[[value]]</b> ms</div>",
                        "useDataSetColors": false
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
                        "useDataSetColors": false
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
