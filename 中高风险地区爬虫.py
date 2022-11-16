from lxml import etree
import requests
import csv
import datetime
import os
import json
#-----------高风险-----------
#源代码爬取到本地
def high_getData():
    url = 'http://m.bj.bendibao.com/news/gelizhengce/fengxianmingdan.php?src=baidu#bj'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Cookie': 'Hm_lvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663587950; Hm_lvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663588110; Hm_lpvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663588110; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663588110'
        }

    response = requests.get(url=url,headers=headers)
    page_text = response.text
    response.close()

    if not os.path.exists('others/highRisk'):
        os.mkdir('others/highRisk')
    f = open('./highRisk/'+str(datetime.date.today())+'highRiskZone.txt','w',encoding='utf-8')
    f.write(page_text)
    f.close()
    print("高风险地区源代码爬取完成")

def get_tilltime():
    etree1 = etree.parse('./highRisk/'+str(datetime.date.today())+'highRiskZone.txt',parser=etree.HTMLParser())
    till_time = etree1.xpath('//div[@class="city-time-wrap"]/p[@class="time"]/text()')[0]
    return till_time
#解析数据
def high_analysisData():
    etree1 = etree.parse('./highRisk/'+str(datetime.date.today())+'highRiskZone.txt',parser=etree.HTMLParser())
    #etree1 = etree.parse('./highRisk/2022-09-21highRiskZone.txt',parser=etree.HTMLParser())

    till_time = get_tilltime().replace(':', '_')
    print(till_time[2:])

    info_list = etree1.xpath('//div[@class="info"]/div[@class="height info-item"]/div[@class="info-list"]')
    total_count = etree1.xpath('//div[@class="fengx-number flex-between"]/div[@class="fx-item high-fx bold"]/div[1]/span/text()')[0]

    if not os.path.exists('疫情历史数据/highRecordData'):
        os.mkdir('疫情历史数据/highRecordData')
    fp = open('./highRecordData/high'+ till_time[2:] + '.csv', mode='w', encoding='utf-8')
    #fp = open('./highRecordData/high2022-09-21.csv', mode='w', encoding='utf-8')
    csvwriter = csv.writer(fp)
    fp.write('今日中风险地区数量：'+total_count+'\n')

    for info in info_list:
        div_list = info.xpath('./div[@class="shi flex-between"]')
        ul_list = info.xpath('./ul[@class="info-detail"]')
        dic = dict(zip(div_list,ul_list))

        for div, ul in dic.items():
            cityName = div.xpath('./div[@class="flex-between bold"]/p/span/text()')
            all_area = []
            li_list =ul.xpath('./li')

            for li in li_list:
                areName = li.xpath('./span/text()')[0].strip()
                all_area.append(areName)

            dictionary ={'city':str(cityName),'count':len(li_list),'area':str(all_area)}
            csvwriter.writerow(dictionary.values())

    print("高风险地区数据解析完成")


#-----------中风险-----------
def mid_getData():
    url = 'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%B8%AD%E9%A3%8E%E9%99%A9&keywords=&qu='
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Cookie': 'Hm_lvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663587950; Hm_lvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663588110; Hm_lpvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663588110; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663588110'
        }
    params = {
        'level': '中风险',
        'keywords': '',
        'qu': ''
    }

    response = requests.get(url=url,headers=headers,params=params)
    page_json = response.json()
    response.close()

    if not os.path.exists('others/midRisk'):
        os.mkdir('others/midRisk')
    fp = open('./midRisk/'+str(datetime.date.today())+'midRiskZone.json','w',encoding='utf-8')
    json.dump(page_json, fp=fp, ensure_ascii=False)
    fp.close()

    print("中风险地区源代码爬取完成")

    mid_analysisData(page_json)

#解析数据
def mid_analysisData(page_json):

    if not os.path.exists('疫情历史数据/midRecordData'):
        os.mkdir('疫情历史数据/midRecordData')
    till_time = get_tilltime().replace(':', '_')
    fp = open('./midRecordData/mid'+till_time[2:]+'.csv', mode='w', encoding='utf-8')
    csvwriter = csv.writer(fp)

    count = page_json['count']
    fp.write('今日中风险地区数量：'+str(count)+'\n')

    data_list = page_json['data']
    for object in data_list:
        province = object['province']
        cityname = object['cityname']
        qu_list = object['qu']
        area_list = []
        count_qu = len(qu_list)

        for qu in qu_list:
            areaname = qu['qu']
            area_list.append(areaname)

        dict = {'pro':province,'city':cityname,'count':count_qu,'area':str(area_list)}
        csvwriter.writerow(dict.values())

    fp.close()

    print("中风险地区数据解析完成")


#-----------低风险-----------
#源代码爬取
def low_getData():
    url = 'http://m.bj.bendibao.com/news/gelizhengce/fxmd_data.php?level=%E4%BD%8E%E9%A3%8E%E9%99%A9&keywords=&qu='
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Cookie': 'Hm_lvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663587950; Hm_lvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587950; Hm_lvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663587988; Hm_lpvt_b6435b4f11e7bb5bdd837339bd80f2dc=1663588110; Hm_lpvt_bc6ddf5d14fb4470bf7c23e9ee036ae2=1663588110; Hm_lpvt_d7c7037093938390bc160fc28becc542=1663588110'
        }
    params = {
        'level': '低风险',
        'keywords': '',
        'qu': ''
    }

    response = requests.get(url=url,headers=headers,params=params)
    page_json = response.json()
    response.close()

    if not os.path.exists('others/lowRisk'):
        os.mkdir('others/lowRisk')
    fp = open('./lowRisk/'+str(datetime.date.today())+'lowRiskZone.json','w',encoding='utf-8')
    json.dump(page_json, fp=fp, ensure_ascii=False)
    fp.close()

    print("低风险地区源代码爬取完成")

    low_analysisData(page_json)

#解析数据
def low_analysisData(page_json):
    till_time = get_tilltime().replace(':', '_')

    if not os.path.exists('疫情历史数据/lowRecordData'):
        os.mkdir('疫情历史数据/lowRecordData')
    fp = open('./lowRecordData/low'+till_time[2:]+'.csv', mode='w', encoding='utf-8')
    csvwriter = csv.writer(fp)

    count = page_json['count']
    fp.write('今日低风险地区数量：'+str(count)+'\n')

    data_list = page_json['data']
    for object in data_list:
        province = object['province']
        cityname = object['cityname']
        qu_list = object['qu']
        area_list = []
        count_qu = len(qu_list)

        for qu in qu_list:
            areaname = qu['qu']
            area_list.append(areaname)

        dict = {'pro':province,'city':cityname,'count':count_qu,'area':str(area_list)}
        csvwriter.writerow(dict.values())

    fp.close()

    print("低风险地区数据解析完成")

#每天16：00调用
def get_alldata():
    high_getData()
    high_analysisData()
    mid_getData()
    low_getData()

get_alldata()
