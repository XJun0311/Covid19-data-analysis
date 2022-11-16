import schedule
import time
import datetime
from pyecharts.charts import Page
from 爬虫_持续 import *
from 总数_柱状图 import *
def work():
    #中国地图需要的参数
    level_h = '高风险'
    url_h = 'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%B8%AD%E9%A3%8E%E9%99%A9&keywords=&qu='
    level_m = '中风险'
    url_m = 'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%B8%AD%E9%A3%8E%E9%99%A9&keywords=&qu='
    level_l = '低风险'
    url_l = 'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%BD%8E%E9%A3%8E%E9%99%A9&keywords=&qu='

    high_data_frame = getData(url_h,level_h)
    mid_data_frame = getData(url_m,level_m)
    low_data_frame = getData(url_l,level_l)

    # 获得中国、省、市的地图
    high_china_map, char_id = china_map(get_data_pair(high_data_frame), level_h)
    mid_china_map, char_id = china_map(get_data_pair(mid_data_frame), level_m)
    low_china_map, char_id = china_map(get_data_pair(low_data_frame), level_l)
    # 这些存储到本地了
    province_map(high_data_frame, level_h)
    province_map(mid_data_frame, level_m)
    province_map(low_data_frame, level_l)
    print('各省份地图储存完成')
    city_map(high_data_frame, level_h)
    city_map(mid_data_frame, level_m)
    city_map(low_data_frame, level_l)
    print('各市地图储存完成')

    # 在每个省地图的html文件后面加上市地图
    pro_city_dict = get_pro_city_dict()
    for pro in pro_city_dict.keys():
        for level in ['高风险','中风险','低风险']:
            pro_add_link(pro,level,pro_city_dict[pro])
    print('在各省地图后面加上jsCode完成')

    high_char_id = high_china_map.chart_id
    mid_char_id = mid_china_map.chart_id
    low_char_id = low_china_map.chart_id

    #柱状图需要的参数
    high_count_list = get_count_list('疫情历史数据/highRecordData')
    mid_count_list = get_count_list('疫情历史数据/midRecordData')
    low_count_list = get_count_list('疫情历史数据/lowRecordData')
    time_list = [time[26:36] for time in list_dir('疫情历史数据/highRecordData')]

    page = Page(layout=Page.DraggablePageLayout)  #创建一个page放所有的图
    page.add(high_china_map, mid_china_map, low_china_map,
             count_bar(time_list, high_count_list, mid_count_list, low_count_list))
    page.render('my_page.html')
    add_link('my_page.html',high_char_id,'高风险')
    add_link('my_page.html',mid_char_id,'中风险')
    add_link('my_page.html',low_char_id,'低风险')
    Page.save_resize_html('my_page.html', cfg_file='chart_config.json', dest='final_page.html')

    print(datetime.datetime.now())

work()
schedule.every(3).minutes.do(work)

while True:
    schedule.run_pending()  #检测是否执行
    time.sleep(1)
