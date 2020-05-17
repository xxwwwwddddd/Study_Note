#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Yunrui Zhou
# FILE: C:\Users\d1286\Desktop\机密文件\PYTHON\大作业\爬虫练习\豆瓣电影基础信息爬取（requests+json+lxml）.py
# DATE: 2020/05/12 周二
# TIME: 16:40:17

# DESCRIPTION:爬取豆瓣电影界面的电影简介.打印出来，后续可以写到文件里
#技术路线就是 requests--json---lxml 当然不止这条路线。
#这里用面向对象，也可也不用。。。直接用函数也行
import requests
from lxml import etree
import json
from selenium import webdriver

class SpiderMoiveSummary():
    '''
    
    '''
    #初始化
    #self是面向对象里的一个形参，必须得有，当然不用面向对象的时候，就不用这个参数
    def __init__(self,num):
        #这个url是得到该网页的json数据 num对应一个页面的电影数,如何获得这个url,就是到原网页,f12--network--里面找,对找,一般容易找到
        self.url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit={}&page_start=".format(num) 
        #设定headers 简单地反爬虫，如何获取呢，也是在爬取的页面F12--network，随便点一个，然后点击headers就可以看到
        self.headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Referer': 'https://movie.douban.com/explore'
        }
        #每个电影具体网站的通用格式{}内填电影的id
        self.basic_url = 'https://movie.douban.com/subject/{}/'
        #简介所在的路径
        self.summary_path = '//span[@property= "v:summary"]/text()'
    #获取请求
    def get_requests(self,url):
        try:
            response = requests.get(url, headers =self.headers)
            response.raise_for_status
            return response
        except:
            return ''
    #得到电影的id号码和电影的名字
    def get_movie(self):
        movie_id_List = []
        movie_name_list = []
        responses = self.get_requests(self.url)
        content  = responses.content.decode()
        all_info = json.loads(content)['subjects']#json.loads(json数据)函数是将json数据变成python的字典
        for i in range(len(all_info)):
            movie_id = all_info[i]['id']
            movie_name = all_info[i]['title']
            movie_rate = all_info[i]['rate']
            movie_name_list.append([movie_name,movie_rate])
            movie_id_List.append(movie_id)
        return movie_id_List,movie_name_list
    #获取电影的简介并存储到字典中
    def movie_summary(self):
        movieIdList,movieNameList = self.get_movie()
        summary_list = []
        movieName_Summary_dict = {}
        #Moviecomment ={}
        print("START".center(150,'-'))
        for num in movieIdList:
            responses = self.get_requests(self.basic_url.format(num))
            data = responses.content
            element = etree.HTML(data)#将页面内容作为一个element元素
            summary = element.xpath(self.summary_path)#定位到简介所在的路径,返回一个简介列表
            summary_list.append(summary[0])#因为该列表只有一个值,所以用0索引拿出来
            #driver = webdriver.Firefox()
            #driver.get(self.basic_url.format(num))
            #comment = []
            #element_key = driver.find_elements_by_id("hot-comments")
            #eles = element_key[0].find_elements_by_tag_name('p')
            #for ele in eles:
            #    comment.append(ele)
            
        #接下来是整理数据,将电影名字,评分,简介都放到一个字典里,我的方法有点捞,可以想想有米有其他的
        for i in range(len(summary_list)):
            movieName_Summary_dict[movieNameList[i][0]+ ' rates: '+movieNameList[i][1]]=summary_list[i]
        return movieName_Summary_dict
    
    def loadFile(self):
        movie = self.movie_summary()
        f = open("movie.txt", 'w', encoding='utf-8')
        json.dump(movie,f,indent = 4,ensure_ascii=False)
        f.close()

    def print_movieAndsummary(self):
        """将电影名字和简介打印出来"""
        movie = self.movie_summary()
        for k,v in movie.items():
            print('movie :  {} '.format(k)+'\n'+'summary: {}'.format(v)+'\n')

sp =SpiderMoiveSummary(20)
sp.loadFile()
#之前的self就是这里的sp，sp是这个对象的实例化。
