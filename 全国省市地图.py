from pyecharts.charts import Map,Tab,Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import datetime
from 地区表格 import table_base
from 微信公众号爬虫 import *

#全国疫情中高低风险地区数量地图
def china_map(mydata_pair,level):
    myMap = (
        Map(init_opts=opts.InitOpts(theme='dark', width='1600px', height='900px',chart_id=level+'map'),

        ).add(
        series_name="",
        data_pair=mydata_pair,
        maptype="china",
        label_opts=opts.LabelOpts(
            is_show=True,
            position='inside',
        ),
        is_map_symbol_show=False,
        is_roam=True,     # 不允许鼠标缩放和平移漫游
        layout_size= 0.8  # 地图的大小
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title="全国新冠疫情"+level+"地区情况地图",
            pos_left="center",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=24,
                font_family="Microsoft YaHei"),
            subtitle='数据获取时间截至'+str(datetime.datetime.now())[:19],
            subtitle_textstyle_opts=opts.TextStyleOpts(
                font_size=12, font_family="Microsoft YaHei"),
        ),
        tooltip_opts=opts.TooltipOpts(
            is_show=True,
            formatter="{b}:"+level+"地区{c}个"
        ),
        # 图例
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            dimension=0,
            pos_left="10",
            pos_bottom="20",
            # 设置分段值
            pieces=[
                {'max': 0, 'min': 0, 'label': '0', 'color': '#FFFFCC'},
                {'max': 29, 'min': 1, 'label': '1-29', 'color': '#FFC4B3'},
                {'max': 89, 'min': 30, 'label': '30-89', 'color': '#FF9985'},
                {'max': 199, 'min': 90, 'label': '90-199', 'color': '#F57567'},
                {'max': 399, 'min': 200, 'label': '200-399', 'color': '#E64546'},
                {'max': 699, 'min': 400, 'label': '400-699', 'color': '#B80909'},
                {'max': 10000, 'min': 700, 'label': '>=700', 'color': '#8A0808'},
            ]
        )
    ))
    return myMap,myMap.chart_id

# 各个省份地图
def province_map(data_frame,level):
    global province_map
    text = '河北、山西、辽宁、吉林、黑龙江、江苏、浙江、安徽、福建、江西、山东、河南、湖北、湖南、广东、海南、四川、贵州、云南、陕西、甘肃、青海、台湾、内蒙古、广西、西藏、宁夏、新疆、北京、天津、上海、重庆、香港、澳门'
    all_province_list = list(text.split('、'))
    pro_list = []
    for i in range(len(data_frame['pro'])):
        if data_frame['pro'][i] not in pro_list:
            pro_list.append((data_frame['pro'][i]))

    for pro in all_province_list:
        city_count = []

        for i in range(len(data_frame['pro'])):
            if data_frame.loc[i]['pro'] == pro:
                city_count.append((data_frame.loc[i]['city'],int(data_frame.loc[i]['count'])))
            else:
                city_count.append(('',''))
        #print(city_count)

        city_area =[]
        for i in range(len(data_frame['pro'])):
            if data_frame.loc[i]['pro'] == pro:
                city_area.append((data_frame.loc[i]['city'],data_frame.loc[i]['area']))


        if pro not in ["北京","天津","上海","重庆","香港","澳门"]:
            province_map = (
                Map(init_opts =opts.InitOpts(width='1500px',height='800px',theme=ThemeType.VINTAGE,chart_id=pro))
                .add(level+"地区数量",
                     data_pair=city_count,  # [('市名’，数量），...]
                     maptype=pro)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=pro+'Map')
                    ,visualmap_opts=opts.VisualMapOpts())
                #.render('./pro_map/'+level+'/'+pro+'Map.html')
            )

        else:
            city_count_area = []
            for i in range(len(data_frame['pro'])):
                    if data_frame.loc[i]['pro'] == pro:
                        city_count_area.append((data_frame.loc[i]['city'],
                                                int(data_frame.loc[i]['count']), data_frame.loc[i]['area']))

            # 每个城市
            for city in city_count_area:
                data_pair = []
                qu_count_dict = {}
                if city != ('', '', ''):
                    qu_list = city[2].replace('[', '').replace(']', '').split(', ')

                    for qu in qu_list:
                        if qu[1:4] not in qu_count_dict.keys():
                            qu_count_dict[qu[1:4]] = 1
                        else:
                            qu_count_dict[qu[1:4]] += 1

                data_pair = [(dist, qu_count_dict[dist]) for dist in qu_count_dict.keys()]
                #print(data_pair)

                province_map = (
                    Map(init_opts=opts.InitOpts(width='1500px', height='800px', theme=ThemeType.VINTAGE, chart_id=pro))
                    .add(level + "地区数量",
                         data_pair=data_pair,  # [('市名’，数量），...]
                         maptype=pro)
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title=pro + 'Map')
                        , visualmap_opts=opts.VisualMapOpts())
                    # .render('./pro_map/'+level+'/'+pro+'Map.html')
                )
        tab = Tab()
        tab.add(province_map, "地图")
        tab.add(table_base(city_area,pro,level), "风险地详细信息")
        tab.render('省、市地图、柱状图/pro_map/'+level+'/'+pro+'Map.html')


# 各个城市地图
def city_map(data_frame, level):
    # 全国所有省
    text = '河北、山西、辽宁、吉林、黑龙江、江苏、浙江、安徽、福建、江西、山东、河南、湖北、湖南、广东、海南、四川、贵州、云南、陕西、甘肃、青海、台湾、内蒙古、广西、西藏、宁夏、新疆、北京、天津、上海、重庆、香港、澳门'
    all_province_list = list(text.split('、'))

    # 对于每个省的每个城市名+count
    for pro in all_province_list:
        city_count_area = []
        for i in range(len(data_frame['pro'])):
            if data_frame.loc[i]['pro'] == pro:
                city_count_area.append((data_frame.loc[i]['city'],
                                        int(data_frame.loc[i]['count']), data_frame.loc[i]['area']))
            else:
                city_count_area.append(('', '', ''))

        # 每个城市
        for city in city_count_area:
            if city != ('', '', ''):
                qu_count_dict = {}
                data_pair = []

                qu_list = city[2].replace('[', '').replace(']', '').split(', ')

                for qu in qu_list:
                    if qu[1:4] not in qu_count_dict.keys():
                        qu_count_dict[qu[1:4]] = 1
                    else:
                        qu_count_dict[qu[1:4]] += 1

                data_pair = [[dist,qu_count_dict[dist]] for dist in qu_count_dict.keys()]

                city_map = (
                    Map()
                    .add(level+"地区数量",data_pair=data_pair, maptype=city[0].replace('市',''))
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title=city[0][:-1]+"地图"), visualmap_opts=opts.VisualMapOpts()
                    )
                    #.render("city_map/"+level+"/"+city[0][:-1]+"Map.html")
                )

                area = []  #(area,detail)
                qu_detail_dict = {}
                for qu in qu_list:
                    if qu[1:4] not in qu_detail_dict.keys():
                        qu_detail_dict[qu[1:4]] = qu
                    else:
                        qu_detail_dict[qu[1:4]] += '\n'+str(qu)
                area = [(qu,qu_detail_dict[qu]) for qu in qu_detail_dict.keys()]
                page = Page()
                page.add(city_map,table_base(area,pro,level))
                page.render("省、市地图、柱状图/city_map/"+level+"/"+city[0][:-1]+"Map.html")


def get_pro_city_dict():
    pro_city = {}
    with open('城市名.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line != None or '\n':
                line = line.replace('。\n', '')
                pro_city_list = line.split('：')
                if len(pro_city_list) == 1:
                    pro_city[pro_city_list[0]] = pro_city_list[0]
                else:
                    pro_city[pro_city_list[0]] = pro_city_list[1].split('、')
    #print(pro_city)
    return pro_city

#每个省地图里面插入这个jsCode
def pro_jsCode(pro,level,city_list):
    char_id = pro

    jsCode1 = '''
            <!--
                以下为js代码，已设置省地图的char_id为固定值(省名)，嵌入此代码中。
                当在身份地图上点击市名的时候，会捕获到该市的标签名，传入js中判断打开哪个网页
            -->
            <script>
                chart_''' + char_id + '''.on('click', function (param){
                    var selected = param.name;
                        if (selected) {
                            switch(selected){   
            '''
    jsCode2 = '''
                                default:break;
                            }
                        }
                    });
            </script>    
            '''
    for city in city_list:
        jsCode1 += '''                                case \'''' +city+ '''市':location.href = "../../city_map/''' + level + '''/'''+city+'''Map.html";break;'''+'\n'

    jsCode = jsCode1+jsCode2

    return jsCode

def pro_add_link(pro,level,city_list):
    path = '省、市地图、柱状图/pro_map/'+level+'/'+pro+'Map.html'
    with open(path, 'a', encoding="utf-8") as f:
        f.write(pro_jsCode(pro,level,city_list))
