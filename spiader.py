# coding:utf-8
import time
import asyncio
from bs4 import BeautifulSoup  as bs
from urllib.request import urlopen
import requests
import os, re
import aiohttp
import sys,io
import tqdm
from core import *

URL="https://cl.330f.tk/thread0806.php?fid=16"
UHD='https://cl.330f.tk/'

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
    #proxies = {'http': '192.168.30.110:42326'}

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
            # html = requests.post(self.__url, headers=self.headers, proxies=self.proxies)
            html = requests.post(self.__url, headers=self.headers)
            html.encoding = 'gb18030'
            bsObj = bs(html.text, 'lxml')
            alinks = bsObj.find_all("img", {"data-src": re.compile("[0-9]*\.jpg")})
            if len(alinks) == 0:
                alinks = bsObj.find_all("img", {"data-src": re.compile("[0-9]*\.JPG")})
            name = bsObj.find_all("h4")
            for al in alinks:
                urllist.append(al["data-src"])
            return name[0].text, urllist
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
            #html = requests.post(super().url, headers=super().headers,proxies=super().proxies)
            html = requests.post(super().url, headers=super().headers)
            html.encoding='gb18030'
            bsObj = bs(html.text, 'html.parser')
            alinks = bsObj.find_all("a", {"href": re.compile("[0-9]*\.html")}, id='')
            for al in alinks:
                temp=  UHD + al["href"]
                if temp not in urllist:
                    urllist.append(temp)
        except Exception as e:
            print(e)
        return urllist

class DownLoad(object):
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def savepath(self):
        return self._savepath

    @savepath.setter
    def savepath(self, value):
        self._savepath = value

    # FLAGS = ('CN IN US ID BR PK NG BD RU JP '
    #      'MX PH VN ET EG DE IR TR CD FR').split()

    def _save_file_(self,fd:io.BufferedWriter,chunk):
        fd.write(chunk)


    async def _fetch_(self,session:aiohttp.ClientSession):
        print(' 开始下载')
        async with session.get(self.url) as resp:
           with open(self.savepath,'wb') as fd:
                while 1:
                    chunk = await resp.content.read(8192)
                    if not chunk:
                        break
                    lp = asyncio.get_event_loop()
                    lp.run_in_executor(None,self._save_file_,fd,chunk)
                    # fd.write(chunk)
                # fd.close()

    # async def __fetch__(session:aiohttp.ClientSession,url:str,path:str,flag:str):
    #     print(flag, ' 开始下载')
    #     async with session.get(url) as resp:
    #         with open(path,'wb') as fd:
    #             while 1:
    #                 chunk = await resp.content.read(1024)    #每次获取1024字节
    #                 if not chunk:
    #                     break
    #                 fd.write(chunk)
    #     return flag

    async def _begin_download_(self,sem,session:aiohttp.ClientSession):    #控制协程并发数量
        async with sem:
            return await self._fetch_(session)

    async def _download_(self,sem:asyncio.Semaphore):
        tasks = []
        try:
            async with aiohttp.ClientSession() as session:
                # for flag in self.FLAGS:            #创建路径以及url
                #    path = os.path.join(self.savepath, flag.lower() + '.gif')
                #    url = '{}/{cc}/{cc}.gif'.format(self.url, cc=flag.lower())
                   #构造一个协程列表
                   tasks.append(asyncio.ensure_future(self._begin_download_(sem,session)))
                   #等待返回结果
                   tasks_iter = asyncio.as_completed(tasks)
                   #创建一个进度条
                   # fk_task_iter = tqdm.tqdm(tasks_iter,total=len(self.FLAGS))
                   fk_task_iter = tqdm.tqdm(tasks_iter)
                   for coroutine in fk_task_iter:
                        #获取结果
                        res = await coroutine
                        print(res, '下载完成')
        except:
            with Exception as ex:
                print(ex)

    def run(self):
        #创建目录
        os.makedirs(self.savepath,exist_ok=True)
        #获取事件循环
        lp = asyncio.get_event_loop()
        start = time.time()
         #创建一个信号量以防止DDos
        sem = asyncio.Semaphore(4)
        lp.run_until_complete(self._download_(sem))
        end = time.time()
        lp.close()
        print('耗时:',end-start)




getpag=GetPage()
getpag.url=URL
urllist=getpag.getdata()[10:]
geturl=GetUrl()
for ul in urllist:
    geturl.url=ul
    name, ulist=geturl.getdata()
    manrun(ulist,name)
