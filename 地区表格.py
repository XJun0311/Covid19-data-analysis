import datetime

from pyecharts.components import Table
from pyecharts import options as opts

#各个省份详细地区表格：
def table_base(city_area,pro,level):
    table = Table()
    #print(city_area)
    headers = ["城市/区", level+"详细地点"]
    rows = city_area
    table.add(headers, rows).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title=pro+level+"地详情",
                                           subtitle='截至时间：'+str(datetime.datetime.now())[:19])
    )
    #table.render('pro_table/'+level+'/'+pro+'.html')
    return table