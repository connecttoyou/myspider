# coding:utf-8
import time
import asyncio
from bs4 import BeautifulSoup  as bs
from urllib.request import urlopen
import requests
import os, re
import bs4
import aiohttp

URL="http://www.t66y.com/thread0806.php?fid=16"

class GetUrl():
    '''获取需要下载的url
    url：需要分析的页面网址
    proxis：代理地址
    '''
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gb2312,utf-8',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection':'Keep-alive'}
    proxies = {'http': '192.168.30.110:42326'}

    def __init__(self):
        pass

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    def getdata(self):
        try:
            urllist = []
            html = requests.post(self.__url, headers=self.headers, proxies=self.proxies)
            html.encoding = 'gb18030'
            bsObj = bs(html.text, 'html.parser')
            alinks = bsObj.find_all("input", {"data-src": re.compile("[0-9]*\.jpg")})

            if len(alinks) == 0:
                alinks = bsObj.find_all("input", {"data-src": re.compile("[0-9]*\.JPG")})
            name = bsObj.find_all("h4")
            for al in alinks:
                urllist.append(al["data-src"])
            return name, urllist
        except Exception as e:
            print(e)


class GetPage(GetUrl):
    #获取每个帖子的地址
    # __headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    # __proxies={'http':'192.168.1.100:42326'}

    def __getdata(self):
       pass

    def getdata(self):
        try:
            urllist = []
            #html = requests.post(self.__url,headers=super()._geturl__headers,proxies=super()._geturl__proxies)
            html = requests.post(super().url, headers=super().headers,proxies=super().proxies)
            html.encoding='gb18030'
            bsObj = bs(html.text, 'html.parser')
            alinks = bsObj.find_all("a", {"href": re.compile("[0-9]*\.html")}, id='')
            for al in alinks:
                temp="http://www.t66y.com/" + al["href"]
                if temp not in urllist:
                    urllist.append(temp)
        except Exception as e:
            print(e)
        return urllist


getpag=GetPage()
getpag.url=URL
urllist=getpag.getdata()[8:]
geturl=GetUrl()
for ul in urllist:
    geturl.url=ul
    name, urllist=geturl.getdata()
