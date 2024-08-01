from jinja2 import Template
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, "tpl_echarts.html")

# read template from file
template = Template(open(template_path).read())


def echarts_html(
    options: dict = {},
    title: str = "echarts",
    width: str = "100%",
    height: str = "600px",
    js_url: str = "https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js",
):
    html = template.render(
        options=options, title=title, js_url=js_url, height=height, width=width
    )
    return html
