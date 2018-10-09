import requests
#from bs4 import BeautifulSoup
#import re
from datetime import datetime
import math
import os
import time
import traceback

def getHTMLText(url, data):
    try:
        r = requests.post(url, data)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.json()
        return html
    except:
        print("Post Error")
        traceback.print_exc()

def getHTMLText2(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        return r
    except:
        print("Get Error")
        traceback.print_exc()

def InfoProcess(dic):
    try:
        s = dic['announcements']
        for j in range(len(s)):
            secCode = s[j]['secCode']
            secName = s[j]['secName']
            #secName = secName.encode('utf-8')
            #print(secName)
            announcementTitle = s[j]['announcementTitle']
            #announcementId = s[j]['announcementId']
            #announcementTitle = announcementTitle.encode('utf-8')
            time = str(datetime.fromtimestamp(int(s[j]['announcementTime'])/1000))
            time2 =  str(s[j]['announcementTime'])
            surl = 'http://www.cninfo.com.cn/' + s[j]['adjunctUrl']
            ls = [secCode, secName, announcementTitle, time, surl]
            with open(r'F:\AnnouncementData\data.csv', 'a') as g:
                g.write('$'.join(ls) + '\n')
            #print("目录保存成功")
            path=root+secCode+'$'+announcementTitle+'$'+time2+'.'+surl.split('/')[-1].split('.')[-1]
            #print(path)
            if not os.path.exists(path):
                #print("step1")
                r = getHTMLText2(surl)
                #print("step2")
                #print(r.content)
                with open(path, 'wb') as w:
                    #print("step3")
                    for content in r.iter_content():
                        w.write(content)
                    #w.write(r.content)
                    #w.close()
                    #print("文件保存成功")
            else:
                print("文件已存在")
                traceback.print_exc()
    except:
        print("Save Error")
        traceback.print_exc()


def getStockInfo(list, url):
    dic = {}
    dic['pageSize'] = '30'
    dic['tabName'] = 'relation'
    dic['column'] = 'szse'
    dic['searchkey'] = ' '
    dic['secid'] = ' '
    dic['plate'] = 'sz'
    dic['category'] = ' '
    dic['seDate'] = '2013-01-01 ~ 2017-12-31'
    for i in range(len(list)):
        try:
            count = i + 1
            pro = count*100/len(list)
            print("\r完成进度:{:.3f}%".format(pro), end="")
            dic['pageNum'] = '1'
            dic['stock'] = list[i], 'gssz'+list[i]
            html = getHTMLText(url, data=dic)
            #print(len(html))
            total = html.get('totalAnnouncement', 0)
            page = math.ceil(int(total)/30)
            #print('error')
            InfoProcess(html)
            for p in range(2, page+1):
                dic['pageNum'] = p
                #print(dic['pageNum'])
                html = getHTMLText(url, data=dic)
                InfoProcess(html)
        except:
            print("Error")
            traceback.print_exc()
            continue

def main():
    global root
    root = "F://AnnouncementData//"
    url = 'http://three.cninfo.com.cn/new/hisAnnouncement/query'
    with open(r'F:\tone&analystdata\codelist.csv') as f:
        codelist = list(f.readlines())
    for i in range(len(codelist)):
        codelist[i] = codelist[i][2:8]
    #codelist = []
    #codelist.append('000786')
    #print(codelist)
    getStockInfo(codelist, url)

main()
