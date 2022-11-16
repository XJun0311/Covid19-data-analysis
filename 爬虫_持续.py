import datetime

import requests
import pandas as pd
from 全国省市地图 import *


#高风险url:'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E9%AB%98%E9%A3%8E%E9%99%A9&keywords=&qu='
#中风险url:'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%B8%AD%E9%A3%8E%E9%99%A9&keywords=&qu='
#低风险url:'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%BD%8E%E9%A3%8E%E9%99%A9&keywords=&qu='

#-----------数据爬取-----------
#源代码爬取
def getData(url,level):
    url = url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Cookie': 'Hm_lvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663587950; Hm_lvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663588110; Hm_lpvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663588110; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663588110'
        }
    params = {
        'level': str(level),
        'keywords': '',
        'qu': ''
    }

    response = requests.get(url=url,headers=headers,params=params)
    page_json = response.json()
    response.close()

    print(level+"地区源代码爬取完成")

    return analysisData(page_json,level)

#解析数据
def analysisData(page_json,level):
    count = page_json['count']

    data_list = page_json['data']
    dataframe = pd.DataFrame({},columns=['pro','city','count','area'],dtype=str)
    i=-1
    for object in data_list:
        i+=1
        province = object['province']
        cityname = object['cityname']+'市'
        qu_list = object['qu']
        area_list = []
        count_qu = len(qu_list)

        for qu in qu_list:
            areaname = qu['qu']
            area_list.append(areaname)
        dataframe.loc[i]=[province, cityname, count_qu, str(area_list)]

    print(level+"地区数据解析完成")
    return dataframe

def get_alldata():
    dataframe1 = getData('http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?'
                         'level=%E9%AB%98%E9%A3%8E%E9%99%A9&keywords=&qu=','高风险')
    dataframe2 = getData('http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?'
                         'level=%E4%B8%AD%E9%A3%8E%E9%99%A9&keywords=&qu=','中风险')
    dataframe3 = getData('http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?'
                         'level=%E4%BD%8E%E9%A3%8E%E9%99%A9&keywords=&qu=','低风险')
    return dataframe1,dataframe2,dataframe3

#通过上面得到的dataframe，获得data_pair
def get_data_pair(df):
    text = '河北、山西、辽宁、吉林、黑龙江、江苏、浙江、安徽、福建、江西、山东、河南、湖北、湖南、广东、海南、四川、贵州、云南、陕西、甘肃、青海、台湾、内蒙古、广西、西藏、宁夏、新疆、北京、天津、上海、重庆、香港、澳门'
    all_province = list(text.split('、'))
    province_list = []
    for i in range(len(df['pro'])):
        if df['pro'][i] not in province_list:
            province_list.append(df['pro'][i])
    other = set(all_province).difference(set(province_list))
    province_list += other
    data_dic={}
    for i in range(len(df['pro'])):
        if df['pro'][i] not in data_dic.keys():
            data_dic[df['pro'][i]] = int(df.iloc[i]['count'])
        else:
            data_dic.setdefault(df['pro'][i],0)
            data_dic[df['pro'][i]] += int(df.iloc[i]['count'])
    data_list = list(data_dic.values())
    data_list_fill = data_list + [0] * (34-len(data_list))
    #print(province_list)
    data_pair = [x for x in zip(province_list, data_list_fill)]
    #print(data_pair)
    return data_pair

def js(char_id,level):
    jsCode = '''
        <!--
            以下为js代码，使用pyecharts获取的中国地图网页的地图id，嵌入此代码中。
            当在中国地图上点击省份的时候，会捕获到该省份的标签名，传入js中判断打开哪个网页
        -->
        <script>
            chart_'''+ char_id +'''.on('click', function (param){
                var selected = param.name;
                    if (selected) {
                        switch(selected){
                            case '北京':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/北京Map.html";break;
                            case '上海':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/上海Map.html";break;
                            case '天津':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/天津Map.html";break;
                            case '四川':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/四川Map.html";break;
                            case '安徽':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/安徽Map.html";break;
                            case '山东':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/山东Map.html";break;
                            case '江苏':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/江苏Map.html";break;
                            case '江西':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/江西Map.html";break;
                            case '河北':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/河北Map.html";break;
                            case '浙江':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/浙江Map.html";break;
                            case '海南':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/海南Map.html";break;
                            case '湖北':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/湖北Map.html";break;
                            case '湖南':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/湖南Map.html";break;
                            case '广东':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/广东Map.html";break;
                            case '福建':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/福建Map.html";break;
                            case '甘肃':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/甘肃Map.html";break;
                            case '广西':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/广西Map.html";break;
                            case '贵州':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/贵州Map.html";break;
                            case '河南':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/河南Map.html";break;
                            case '黑龙江':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/黑龙江Map.html";break;
                            case '内蒙古':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/内蒙古Map.html";break;
                            case '吉林':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/吉林Map.html";break;
                            case '辽宁':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/辽宁Map.html";break;
                            case '宁夏':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/宁夏Map.html";break;
                            case '青海':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/青海Map.html";break;
                            case '山西':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/山西Map.html";break;
                            case '陕西':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/陕西Map.html";break;
                            case '台湾':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/台湾Map.html";break;
                            case '西藏':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/西藏Map.html";break;
                            case '新疆':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/新疆Map.html";break;
                            case '云南':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/云南Map.html";break;
                            case '重庆':location.href = "./省、市地图、柱状图/pro_map/'''+level+'''/重庆Map.html";break;
                            default:break;
                        }
                    }
                });
        </script>    
        '''
    return jsCode

def add_link(path,char_id,level):
    with open(path, 'a', encoding="utf-8") as f:
        f.write(js(char_id,level))
 # 将地图的charid设置成固定值，然后以追加的形式写入当前文件夹下中的map文件夹下的“中国地图.html”文件中


if __name__ == '__main__':
    print(str(datetime.datetime.now())[:19])
    level = '高风险'
    url = 'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E9%AB%98%E9%A3%8E%E9%99%A9&keywords=&qu='
    data_frame = getData(url,level)
    china_map, char_id = china_map(get_data_pair(data_frame), level)
    china_map.render('中国疫情地图.html')
    province_map(data_frame,level)
    # 给生成好的中国地图加上跳转的js代码
    add_link('中国疫情地图.html',char_id,level)



