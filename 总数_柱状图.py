from pyecharts import options as opts
from pyecharts.charts import Bar
import pandas as pd
import os

def count_bar(time_list,high_count_list,mid_count_list,low_count_list):
    l1 = time_list
    l2 = high_count_list
    l3 = mid_count_list
    l4 = low_count_list
    bar = (
        Bar(init_opts=opts.InitOpts(chart_id='barid'))
        .add_xaxis(l1)
        .add_yaxis("高风险地区数量", l2)#color='#FFFF00'
        .add_yaxis("中风险地区数量", l3)
        .add_yaxis('低风险地区数量',l4)
        .set_global_opts(title_opts=opts.TitleOpts(title="全国中高低风险地总数趋势图", subtitle="数据来源：本地宝"),
                         datazoom_opts=opts.DataZoomOpts(type_="inside"),   #可缩放
                         toolbox_opts=opts.ToolboxOpts(),                   #显示工具栏
                         legend_opts=opts.LegendOpts(is_show=True),
                         xaxis_opts=opts.AxisOpts(name="日期"),
                         )
    )
    #bar.render('总数_柱状图.html')
    return bar

#获取文件夹中所有csv文件路径的方法
def list_dir(file_path):
    dir_list = os.listdir(file_path)
    list_csv=[]
    for file in dir_list:
        path = os.path.join(file_path,file)
        #判断是否存在.csv文件，如果存在则获取路径信息写入到list_csv中
        if os.path.splitext(path)[1] == '.csv':
            csv_file = os.path.join(file_path,file)
            list_csv.append(csv_file)
    return list_csv

#获取一个文件夹中每个csv文件的地区总数
def get_count_list(paths):
    paths = paths
    list_csv = list_dir(file_path=paths)
    #print(list_csv)
    count_list = []
    for csv_path in list_csv:
        data = pd.read_csv(csv_path, names=['pro_city', 'count', 'area'], skiprows=[0])
        count_list.append(int(data['count'].sum()))
    return count_list






