import pandas as pd
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
from pyecharts.charts import Timeline
import BigData.provinceDataGet
import datetime

areas = BigData.provinceDataGet.areas

# 疫情地图所用颜色
pieces = [
    {'min': 10000, 'color': '#540d0d'},
    {'max': 9999, 'min': 1000, 'color': '#9c1414'},
    {'max': 999, 'min': 500, 'color': '#d92727'},
    {'max': 499, 'min': 100, 'color': '#ed3232'},
    {'max': 99, 'min': 10, 'color': '#f27777'},
    {'max': 9, 'min': 1, 'color': '#f7adad'},
    {'max': 0, 'color': '#f7e4e4'},
]

def getDataFromExcel():
    confirmListAll = []
    dateList = []
    today = datetime.date.today()  # 获得今天的日期
    yesterday = today - datetime.timedelta(days=1)
    textY = yesterday.strftime('%m.%d')
    textY = textY[1:]
    # print(textY)
    for area in areas:
        data = pd.read_excel(r'D:\pycharmCode\BigData\result\provinceData.xlsx', sheet_name=area, usecols='A,H')
        datalist = list(data.现有确诊)
        dateList = list(data.日期)
        if area != '台湾' and area != '香港' and area != '澳门':
            datalist = datalist[13:]
        if str(dateList[-1]) == textY:
            dateList = dateList[:-1]
            datalist = datalist[:-1]
        confirmListAll.append(datalist)
        # print(area, len(datalist), dateList[-1])
    # print(confirmListAll)
    dateList = dateList[13:]
    # print(len(dateList))
    confirmList = []
    for i in range(len(confirmListAll[0])):
        confirmNeed = []
        for j in range(len(confirmListAll)):
            confirmNeed.append(confirmListAll[j][i])
        confirmList.append(confirmNeed)
    # print(confirmList)
    return confirmList, dateList


if __name__ == '__main__':

    confirmList, dateList = getDataFromExcel()
    # 时间线
    t = Timeline()

    i = 0
    # 将数据转换为二元的列表并绘制地图
    for seq in confirmList:
        ret = list(zip(areas, seq))
        print(ret)
        c = (
            Map()
                .add("现有确诊", ret, "china")
                .set_global_opts(
                title_opts=opts.TitleOpts(title="中国疫情地图"),
                visualmap_opts=opts.VisualMapOpts(pieces=pieces, is_piecewise=True)
            )
        )
        t.add(c, dateList[i])
        i = i+1
    t.render(r'D:\pycharmCode\BigData\result\map.html')
