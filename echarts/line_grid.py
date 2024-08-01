import pandas as pd
from jinja2 import Template

template = Template("""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="{{ js_url }}"></script>
</head>

<body>
    <div id="main" style="width: {{ width }}; height:{{ height }};"></div>
    <script type="text/javascript">
        var myChart = echarts.init(document.getElementById('main'));
        var option =  {{ options|tojson }} ;
        myChart.setOption(option);
    </script>
</body>

</html>
""")
def echarts_html(
    options: dict = {},
    title: str = "echarts",
    width: str = "100%",
    height: str = "600px",
    js_url: str = "https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js",
    ):
    return template.render(
        options=options, title=title, js_url=js_url, height=height, width=width
    )

data =  pd.read_csv("data/rainfall.csv", index_col=0, parse_dates=True)
time_data = [s.strftime('%m/%d %H:%M') for s in data.index]
evaporation = data.evaporation.to_list()
rainfall = data.rainfall.to_list()

options = {
    "title": {"text": "Rainfall vs Evaporation", "left": "center"},
    "tooltip": {"trigger": "axis", "axisPointer": {"animation": False}},
    "legend": {"data": ["Evaporation", "Rainfall"], "left": 10},
    "toolbox": {
        "feature": {
            "dataZoom": {"yAxisIndex": "none"},
            "restore": {},
            "saveAsImage": {},
        }
    },
    "axisPointer": {"link": [{"xAxisIndex": "all"}]},
    "dataZoom": [
        {"show": True, "realtime": True, "start": 10, "end": 90, "xAxisIndex": [0, 1]},
        {
            "type": "inside",
            "realtime": True,
            "start": 30,
            "end": 70,
            "xAxisIndex": [0, 1],
        },
    ],
    "grid": [
        {"left": 60, "right": 50, "height": "35%"},
        {"left": 60, "right": 50, "top": "55%", "height": "35%"},
    ],
    "xAxis": [
        {
            "type": "category",
            "boundaryGap": False,
            "axisLine": {"onZero": True},
            "data": time_data,
        },
        {
            "gridIndex": 1,
            "type": "category",
            "boundaryGap": False,
            "axisLine": {"onZero": True},
            "data": time_data,
            "position": "top",
        },
    ],
    "yAxis": [
        {"name": "Evaporation(m³/s)", "type": "value", "max": 500},
        {"gridIndex": 1, "name": "Rainfall(mm)", "type": "value", "inverse": True},
    ],
    "series": [
        {"name": "Evaporation", "type": "line", "symbolSize": 8, "data": evaporation},
        {
            "name": "Rainfall",
            "type": "line",
            "xAxisIndex": 1,
            "yAxisIndex": 1,
            "symbolSize": 8,
            "data": rainfall,
        },
    ],
}

html = echarts_html(options=options, height="1024px")
with open("output/line_grids.html", "w", encoding="utf-8") as f:
    f.write(html)

print("html generated:\n", html)