import pandas as pd
from jinja2 import Template

template = Template(
    """
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
"""
)


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



# data preparation
orders = pd.read_excel('data/FY23Order.xlsx', engine='calamine', skiprows=3)

cols = ['Company Name (CN)', 'Buyer Name (CN)', 'OR Value']
relations = orders.loc[
    orders['Assign Valid'].str.contains('Y')
    & orders['Buyer CNOC'].notna(), cols
].groupby(cols[:-1])[cols[-1]].sum().reset_index()

names = pd.DataFrame(
    relations['Company Name (CN)'].tolist() + relations['Buyer Name (CN)'].tolist(),
    columns = ['name']
).drop_duplicates().reset_index(drop=True)
names_map = {name:idx for idx, name in enumerate(names['name'])}
relations['target'] = relations['Company Name (CN)'].map(names_map)
relations['source'] = relations['Buyer Name (CN)'].map(names_map)

names['target_value'] = names.index.map(relations.groupby('target')['OR Value'].sum()).fillna(0)
names['sourcce_value'] = names.index.map(relations.groupby('source')['OR Value'].sum()).fillna(0)

names['value'] = names['target_value'] + names['sourcce_value']
def scale(value, min_value=names['value'].min(), max_value=names['value'].max(), min_scale=0, max_scale=50):
    return (value - min_value) / (max_value - min_value) * (max_scale - min_scale) + min_scale
names['size'] = names['value'].apply(scale)

names = names.loc[names['value']>1000]
names = names.reset_index(drop=True)
names_map = {name:idx for idx, name in enumerate(names['name'])}
relations['target'] = relations['Company Name (CN)'].map(names_map)
relations['source'] = relations['Buyer Name (CN)'].map(names_map)
relations = relations.loc[relations.source.isin(names.index) & relations.target.isin(names.index)]

length = len(relations)
width = int(length**0.5) + 1
coords = []
for x in range(width):
    for y in range(width):
        coords += [[x, y]]

nodes = [
    {
        'id': str(id),
        'name': names.at[id, 'name'],
        "symbolSize": names.at[id, 'size'],
        'size': names.at[id, 'sourcce_value'] + names.at[id, 'target_value'],
        'x': coords[id][0],
        'y': coords[id][1]
    }
    for id in names.index 
]
links = [
    {'source': str(int(source)), 'target':str(int(target))} 
    for source, target in relations[['source', 'target']].values
]

options = {
    "title": {
        "text": "Les Miserables",
        "subtext": "Default layout",
        "top": "bottom",
        "left": "right",
    },
    "tooltip": {},
    "animationDuration": 1500,
    "animationEasingUpdate": "quinticInOut",
    "series": [
        {
            "name": "Les Miserables",
            "type": "graph",
            "legendHoverLink": False,
            "layout": "none",
            "data": nodes,
            "links": links,
            # 'categories': {'name': 'A',},
            "roam": True,
            "label": {"position": "right", "formatter": "{b}"},
            "lineStyle": {"color": "source", "curveness": 0.3},
            "emphasis": {"focus": "adjacency", "lineStyle": {"width": 10}},
        }
    ],
}

html = echarts_html(options=options, height="1024px")
with open("output/graph.html", "w", encoding="utf-8") as f:
    f.write(html)

print("html generated:\n", html)
