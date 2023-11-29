
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from utils import root_dir
province=["北京","上海","天津","重庆","河北","山西","吉林","辽宁","黑龙江","江苏",
          "浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南",
          "四川","贵州","云南","陕西","甘肃","青海","台湾","宁夏","西藏","新疆",
          "广西","内蒙古","香港","澳门"]

for i,pro in enumerate(province):
    chinaDayData = pd.read_excel(r'{}\Big_Data_Work\provinceData.xlsx'.format(root_dir), sheet_name=pro) # 读取特定的sheet
    #print(chinaDayData.info())
    chinaDayData['日期'] = chinaDayData['日期'].map(str)
    #将"3.1"转换为"3.10" ......
    date = []
    for i in range(len(list(chinaDayData.日期))):
        s = list(chinaDayData.日期)[i]
        temp = list(chinaDayData.日期)[i].split('.')
        if i <= len(list(chinaDayData.日期))-2:
            temp1 = list(chinaDayData.日期)[i+1].split('.')
            if temp[1]=='1' and temp1[1][-1] == '1':
                s = '{}{}'.format(list(chinaDayData.日期)[i], '0')
            if temp[1] == '2' and temp1[1][-1] == '1':
                s = '{}{}'.format(list(chinaDayData.日期)[i], '0')
            if temp[1]=='3' and temp1[1][-1] == '1':
                s = '{}{}'.format(list(chinaDayData.日期)[i], '0')
        date.append(s)


    # 作出 关于新增确诊人数和新增无症状人数的折线图
    my_line1 = (
        Line(init_opts=opts.InitOpts(width='1200px',height='600px'))
        # x轴
        .add_xaxis(date)
        # y轴
        .add_yaxis('新增确诊人数',list(chinaDayData.新增确诊))
        .add_yaxis('新增无症状人数', list(chinaDayData.新增无症状))
        # 标题
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=pro+"新增确诊人数与新增无症状人数关于时间变化趋势"),
            tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis")
        )

    )

    # 作出关于 累计确诊、累计治愈与累计死亡人数的折线图
    my_line2 = (
        Line(init_opts=opts.InitOpts(width='1400px',height='600px'))
        # x轴
        .add_xaxis(date)
        # y轴
        .add_yaxis('累计确诊人数', list(chinaDayData.累计确诊))
        .add_yaxis('累计治愈人数', list(chinaDayData.累计治愈))
        .add_yaxis('累计死亡人数', list(chinaDayData.累计死亡))
        # 标题
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title=pro+"累计确诊人数、累计治愈人数\n与累计死亡人数关于时间变化趋势"),
                         tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis"))
    )
    # 两个折线图各自保存进html文件中
    i = Page(layout=Page.DraggablePageLayout)
    i.add(my_line1,my_line2)
    i.render_notebook()
    i.render(r"{}\Big_Data_Work\result\{}.html".format(root_dir,pro))
    i.save_resize_html(r"{}\Big_Data_Work\result\{}.html".format(root_dir,pro),cfg_file=r"{}\Big_Data_Work\result\chart_config.json".format(root_dir),
                          dest=r"{}\Big_Data_Work\result\{}.html".format(root_dir,pro))
