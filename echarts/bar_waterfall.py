from echarts import echarts_html
import json

def jscode(js_code):
    js_placeholder = "--x_x--0_0--"
    return  f"{js_placeholder}{js_code}{js_placeholder}"

html_output = "output/bar_waterfall.html"
options = {
    "title": {
        "text": "阶梯瀑布图",
        "subtext": "From ExcelHome",
        "sublink": "http://e.weibo.com/1341556070/Aj1J2x5a5",
        "padding": [15, 10],
    },
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "formatter": jscode("function(params){var tar;if(params[1].value!=='-'){tar=params[1]}else{tar=params[0]}return tar.name+'<br/>'+tar.seriesName+' : '+tar.value}"),
    },
    "legend": {"data": ["支出", "收入"], 'top': "10%", 'right': "5%"},
    "grid": {'top': "15%", "left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
    "xAxis": {
        "type": "category",
        "splitLine": {"show": False},
        "data": [f"11月 {i} 日" for i in range(1, 12)],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "辅助",
            "type": "bar",
            "stack": "总量",
            "itemStyle": {
                "barBorderColor": "rgba(0,0,0,0)",
                "color": "rgba(0,0,0,0)",
            },
            "emphasis": {
                "itemStyle": {
                    "barBorderColor": "rgba(0,0,0,0)",
                    "color": "rgba(0,0,0,0)",
                }
            },
            "data": [0, 900, 1245, 1530, 1376, 1376, 1511, 1689, 1856, 1495, 1292],
        },
        {
            "name": "收入",
            "type": "bar",
            "stack": "总量",
            "label": {"show": True, "position": "top"},
            "data": [900, 345, 393, "-", "-", 135, 178, 286, "-", "-", "-"],
        },
        {
            "name": "支出",
            "type": "bar",
            "stack": "总量",
            "label": {"show": True, "position": "bottom"},
            "data": ["-", "-", "-", 108, 154, "-", "-", "-", 119, 361, 203],
        },
    ],
}

if __name__ == "__main__":

    html = echarts_html(options=options, title="waterfall")
    with open(html_output, "w", encoding="utf-8") as f:
        f.write(html)

    print("html generated:\n", html)
