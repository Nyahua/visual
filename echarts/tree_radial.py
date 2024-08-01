from echarts import echarts_html
import json


def jscode(js_code):
    js_placeholder = "--x_x--0_0--"
    return f"{js_placeholder}{js_code}{js_placeholder}"


html_output = "output/tree_radial.html"
data = json.load(open("data/flare.json", "r", encoding="utf-8"))
options = {
    "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
    "series": [
        {
            "type": "tree",
            "data": [data],
            "top": "18%",
            "bottom": "14%",
            "layout": "radial",
            "symbol": "emptyCircle",
            "symbolSize": 7,
            "initialTreeDepth": 3,
            "animationDurationUpdate": 750,
            "emphasis": {"focus": "descendant"},
        }
    ],
}

if __name__ == "__main__":

    html = echarts_html(options=options, title="radial tree")
    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html)

    print("html generated:\n", html)
