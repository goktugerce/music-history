month_html = """
<html>
<head>
<style>
.ggl-tooltip {{
  border: 1px solid #E0E0E0;
  font-family: Arial, Helvetica;
  padding: 6px 6px 6px 6px;
}}

.ggl-tooltip span {{
  font-weight: bold;
}}
</style>
<meta charset="UTF-8">
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

    <script type="text/javascript">
        google.charts.load("current", {{packages: ["timeline"]}});
        google.charts.setOnLoadCallback(drawChart);
        function drawChart() {{

            var container = document.getElementById('example3.1');
            var chart = new google.visualization.Timeline(container);
            var dataTable = new google.visualization.DataTable();
            dataTable.addColumn({{type: 'string', id: 'Day'}});
            dataTable.addColumn({{type: 'string', id: 'Song'}});
            dataTable.addColumn({{type: 'date', id: 'Start'}});
            dataTable.addColumn({{type: 'date', id: 'End'}});
            dataTable.addRows([
            {}
            ]);

            dataTable.insertColumn(2, {{type: 'string', role: 'tooltip', p: {{html: true}}}});

            var dateFormat = new google.visualization.DateFormat({{
                pattern: 'h:mm a'
            }});

            for (var i = 0; i < dataTable.getNumberOfRows(); i++) {{
              var tooltip = '<div class="ggl-tooltip"><span>' +
                dataTable.getValue(i, 1) + '</span></div><div class="ggl-tooltip"><span>' +
                dataTable.getValue(i, 0) + '</span>: ' +
                dateFormat.formatValue(dataTable.getValue(i, 3)) + ' - ' +
                dateFormat.formatValue(dataTable.getValue(i, 4)) + '</div>';

              dataTable.setValue(i, 2, tooltip);
            }}


            var options = {{
             tooltip: {{isHtml: true}},
             timeline: {{ showBarLabels: false, colorByRowLabel: true}}
            }};

            chart.draw(dataTable, options);
        }}
    </script>

    <div id="example3.1" style="height: 600px;"></div>
</head>
<body>
<div id="timeline" style="height: 580px;"></div>
</body>
</html>
"""

html_top_artists = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>Top Artists</title>
</head>
<body>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load("current", {{packages: ['corechart']}});
    google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawPieChart);
    function drawChart() {{
        var data = google.visualization.arrayToDataTable([
            ['Artist', 'Play Count'],
            {}
        ]);
        var options = {{
            title: "Top Artists Listened",
            titlePosition: 'none',
            colors: ['#EA5455'],
            bar: {{groupWidth: '85%'}},
            legend: {{position: 'none'}},
            hAxis: {{
                title: "Artists"
            }},
            vAxis: {{
                title: "Number of Plays"
            }}
        }};
        var chart = new google.visualization.ColumnChart(document.getElementById('columnchart_plain'));
        chart.draw(data, options);
    }}

    function drawPieChart() {{

        var data = google.visualization.arrayToDataTable([
          ['Genre', 'Play Counts'],
          {}
        ]);

        var options = {{
          title: 'My Daily Activities',
          titlePosition: 'none'
        }};

        var piechart = new google.visualization.PieChart(document.getElementById('piechart'));

        piechart.draw(data, options);
      }}
</script>

<div class="container" style="text-align:center;">
    <h3 style="margin:0 auto; width:50%; text-align:center; font-family:Verdana">Top Artists</h3>
    <div id="columnchart_plain" style="width: 100%; display:inline-block; height: 600px;"></div>
    <h3 style="margin:0 auto; width:50%; text-align:center; font-family:Verdana; margin-top:50px">Top Genres</h3>
    <div id="piechart" style="display:inline-block; width:80%; height:500px;"></div>
</div>
</body>
</html>
"""


html_top_albums_and_tracks = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>Top {}</title>
</head>
<body>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load("current", {{packages: ['corechart', 'bar']}});
    google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawPieChart);
    function drawChart() {{
        var data = google.visualization.arrayToDataTable([
            [{}, 'Play Count'],
            {}
        ]);
        var options = {{
            titlePosition: 'none',
            colors: ['{}'],
            bar: {{groupWidth: '85%'}},
            legend: {{position: 'none'}},
            hAxis: {{
                title: "{}"
            }},
            vAxis: {{
                title: "Number of Plays",
                format: '0'
            }}
        }};
        var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }}

    function drawPieChart() {{

        var data = google.visualization.arrayToDataTable([
          ['Genre', 'Play Counts'],
          {}
        ]);

        var options = {{
          titlePosition: 'none'
        }};

        var piechart = new google.visualization.PieChart(document.getElementById('piechart'));

        piechart.draw(data, options);
      }}
</script>

<div class="container" style="text-align:center;">
    <h3 style="margin:0 auto; width:50%; text-align:center; font-family:Verdana">Top {}</h3>
    <div id="chart_div" style="height:600px; display:inline-block; width: 70%"></div>
    <h3 style="margin:0 auto; width:50%; text-align:center; font-family:Verdana; margin-top:50px">Top Genres</h3>
    <div id="piechart" style="display:inline-block; width:80%; height:500px;"></div>
</div>
</body>
</html>
"""

html_line_chart = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>{}</title>
</head>
<body>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load("current", {{packages: ['corechart', 'line']}});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {{
        var data = google.visualization.arrayToDataTable([
            ['{}', 'Play Count'],
            {}
        ]);
        var options = {{
            titlePosition: 'none',
            colors: ['{}'],
            legend: {{position: 'none'}},
            hAxis: {{
                title: "{}"
            }},
            vAxis: {{
                title: "Number of Plays",
                gridlines: {{color: '#ccc', count: 6}}
            }}
        }};
        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }}

</script>

<div class="container" style="text-align:center;">
    <h3 style="margin:0 auto; width:50%; text-align:center; font-family:Verdana">{}</h3>
    <div id="chart_div" style="width: 100%; display:inline-block; height: 600px;"></div>
</div>
</body>
</html>
"""

html_column_chart = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>{}</title>
</head>
<body>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load("current", {{packages: ['corechart', 'bar']}});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {{
        var data = google.visualization.arrayToDataTable([
            ['{}', 'Play Count'],
            {}
        ]);
        var options = {{
            titlePosition: 'none',
            colors: ['{}'],
            legend: {{position: 'none'}},
            hAxis: {{
                title: "{}"
            }},
            vAxis: {{
                title: "Number of Plays",
                gridlines: {{color: '#ccc', count: 6}},
                viewWindow: {{
                    min:0
                }}
            }}
        }};
        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }}

</script>

<div class="container" style="text-align:center;">
    <h3 style="margin:0 auto; width:50%; text-align:center; font-family:Verdana">{}</h3>
    <div id="chart_div" style="width: 100%; display:inline-block; height: 600px;"></div>
</div>
</body>
</html>
"""

html_calendar_chart = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
    <title>Daily Music Listening History</title>
</head>
<body>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load("current", {{packages: ['calendar']}});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {{
        var dataTable = new google.visualization.DataTable();
       dataTable.addColumn({{ type: 'date', id: 'Date' }});
       dataTable.addColumn({{ type: 'number', id: 'Play Count' }});
       dataTable.addRows([
            {}
        ]);

       var chart = new google.visualization.Calendar(document.getElementById('calendar_basic'));

       var options = {{
         title: "Daily Play Counts",
         height: 600,
       }};

       chart.draw(dataTable, options);
    }}

</script>

<div class="container" style="text-align:center;">
    <div id="calendar_basic" style="width: 100%; display:inline-block; height: 600px;"></div>
</div>
</body>
</html>
"""

html_map_marker = """
<html>
  <head>
  <meta charset="UTF-8">
    <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type='text/javascript'>
     google.charts.load('current', {{'packages': ['geochart']}});
     google.charts.setOnLoadCallback(drawMarkersMap);

      function drawMarkersMap() {{
      var data = new google.visualization.DataTable();
      data.addColumn("number", "LATITUDE");
      data.addColumn("number", "LONGITUDE");
      data.addColumn("string", "DESCRIPTION");
      data.addColumn('number', 'Value:', 'value');
      data.addColumn({{type: "string", role:"tooltip"}});

      {}

      var options = {{
        region: '{}',
        displayMode: 'markers',
        colorAxis: {{colors: ['#ABEDD8', '#46CDCF', "#3D84A8", "#48466D"]}}
      }};

      var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }};
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 1600px; height: 900px;"></div>
  </body>
</html>
"""