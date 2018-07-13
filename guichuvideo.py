"""
2018年每月B站鬼畜视频爬虫
按照热度排行
"""
import requests
import time
import csv
from jsonpath import jsonpath
class GuichuVideo:
    def __init__(self,date1,date2):
        self.date1 = date1
        self.date2 = date2
        self.headers = {
            'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
    def start(self):
        page = 1
        params = {
            'search_type':'video',
            'view_type':'hot_rank',
            'cate_id':'22', #视频分类,鬼畜的是22
            'page':str(page),
            'pagesize':'20',
            'time_from':self.date1,
            'time_to':self.date2
        }
        url = 'https://s.search.bilibili.com/cate/search?'
        item_list = []
        response = requests.get(url, params=params, headers=self.headers).json()
        #总页数
        page_num = int(jsonpath(response, "$..numPages")[0])
        #总视频数
        video_num = int(jsonpath(response,"$..numResults")[0])
        page = page_num
        print('开始获取' + self.date1 + '---'+ self.date2)
        num = 0
        for i in range(1,page+1):
            params['page'] = str(i)
            response = requests.get(url,params=params,headers=self.headers).json()
            video = jsonpath(response,"$..result")[0]
            for video_detail in video:
                item = {}
                item['鬼畜名称'] = video_detail['title']
                item['播放数'] = video_detail['play']
                item['弹幕数'] = video_detail['video_review']
                item['视频地址'] = video_detail['arcurl']
                item['发布时间'] = video_detail['pubdate']
                item['作者'] = video_detail['author']
                item_list.append(item)
                print(self.date1 + '---'+ self.date2 + '完成度......' + str(num/video_num*100) + '%')
                num += 1
        csv_header = item_list[0].keys()
        csv_data = [item_values.values() for item_values in item_list]
        with open('2018年鬼畜热度排行'+ self.date1 +'-'+ self.date2 +  '.csv','w',encoding='utf-8',newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(csv_header)
            csv_writer.writerows(csv_data)
def main():
    #日期计算
    for monnum in range(1,time.localtime().tm_mon+1):
        if monnum < 10:
            mon = '0' + str(monnum)
        else:
            mon = monnum
        date1 = '2018%s01' % mon
        if monnum == time.localtime().tm_mon:
            if time.localtime().tm_mday < 10:
                day = '0' + str(time.localtime().tm_mday)
            else:
                day = time.localtime().tm_mday
            date2 = '2018%s%s' % (mon, day)
        else:
            if mon in ['01','03','05','07','08','10','12']:
                date2 = '2018%s31' % mon
            elif mon in ['02']:
                date2 = '2018%s28' % mon
            else:
                date2 = '2018%s30' % mon
        guichuvideo = GuichuVideo(date1,date2)
        guichuvideo.start()
if __name__ == '__main__':
    main()
