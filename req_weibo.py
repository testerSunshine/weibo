# -*- coding: utf-8 -*-
import random
from Queue import Queue
import threading

from agency_tools import proxy
from db import DB
import re
import requests
import time


def r_get(url):
    cookie_num = random.randint(0, 100000)
    cookies = {"Cookie": "SINAGLOBAL=6652408980066.204.1501{}; SCF=AlKzIm9-tDQgT2Q2lWqdTqGdPfnGEdBiwOO7RcEmgaBD8CDyneJL0IkZYiDUfoZ_h1sOhE5dFANU6pxk5LkbNP0.; SUHB=0P1MuJuKSXIfOa; ALF=1535706873; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; SUB=_2AkMu9ZsRdcPxrAZUkfAXxGPqbYpH-jydIPLnAn7uJhIyOhgv7kYXqSVLgKgtc54gRueiBO1dxcLja7tplA..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFZLx_046ao7yGuungapxi95JpX5KMhUgL.Fo-f1KnE1hnReKM2dJLoIpjLxKqL1KqL1hMLxKnLBoBLBKBLxK-LBo.LBoet; login_sid_t=a4907a4afc1fc10d5cadd7ca20fe44f3; cross_origin_proto=SSL; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; _s_tentry=passport.weibo.com; UOR=,,www.baidu.com; Apache=1506461520797.3774.1504252940079; ULV=1504252940087:2:1:1:1506461520797.3774.1504252940079:1503545508560; YF-Page-G0=c6cf9d248b30287d0e884a20bac2c5ff; wb_cusLike_undefined=N".format(str(cookie_num)),
               "User-Agent": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
               "Referer": "https://weibo.com/",
               "Host": "s.weibo.com",
               "Connection": "keep-alive",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Accept-Encoding": "gzip, deflate, b0r",
    }
    p = proxy()
    address = p.get_filter_proxy()
    proxies = {"http": address[random.randint(0, len(address))-1]}
    print("当前使用http代理为：" + str(proxies))
    results = requests.get(url=url, cookies=cookies, proxies=proxies)
    print(results.text)
    # s = requests.session()
    time.sleep(3)
    # s.keep_alive = False
    if results.status_code is 200:
        return results.text

    else:
        return False


class scrapy(threading.Thread):
    def __init__(self, threadname, queue):
        threading.Thread.__init__(self, name=threadname)
        self.data = queue
        self.threadname = threadname
        print "Scrapy" + threadname + 'start.....'

    def run(self):
        number = 1000000016575
        while 1:
            number += 1
            url = "https://weibo.com/p/100{}/home?is_hot=1".format(str(number))
            # url = "https://weibo.com/u/5598288817/home?topnav=1&wvr=6"
            # url = "https://weibo.com/"
            self.data.put(url,)
            print("url: {} 加入队列".format(url))


class Consumer_even(threading.Thread):
    def __init__(self, threadname, queue):
        threading.Thread.__init__(self, name=threadname)
        self.data = queue
        self.threadname = threadname
        print "Consumer " + threadname + ' start.....'

    def run(self):
        while 1:
            time.sleep(0.1)
            url = self.data.get(1, 5)  # get(self, block=True, timeout=None) ,1就是阻塞等待,5是超时5秒
            print("当前队列大小： {}".format(self.data.qsize()))
            print("{} 取得url: {} ".format(self.threadname, url))
            data = r_get(url)
            if requests is not False:
                process_data(data)
                self.data.task_done()


def process_data(data):
    try:
        pattern_weobo_level = re.compile(r'<a\s+class=\W"W_icon_level icon_level_c\d+\W"\s+title=\W+(\d+)')  # 微博等级
        weobo_level = re.search(pattern_weobo_level, data).group(1)

        pattern_weibo_name = re.compile(r"\WCONFIG\W+onick\W+=\W(\S+)")
        weibo_name = re.search(pattern_weibo_name, data).group(0).split("=")[1].strip("'").strip(";").strip("'")  # 微博昵称

        pattern_synopsis = re.compile(r'<meta\W+content=\W(\S+)\W+name=\Wdescription')   # 微博简介
        synopsis = re.search(pattern_synopsis, data).group(1).strip('"')

        pattern_attention =re.compile(ur"\W(\d+)\W+strong\W+span\W+class\W+S_txt2\W+\S+\W+span\W+")   # 关注
        attention = re.search(pattern_attention, data).group(1)

        pattern_fans = re.compile(ur"\W(\d+)\W+strong\W+span\W+class=\W+S_txt2\W+\u7c89\u4e1d")  # 粉丝
        fans = re.search(pattern_fans, data).group(1)

        pattern_wei_bo = re.compile(ur"\W(\d+)\W+strong\W+span\W+class=\W+S_txt2\W+\u5fae\u535a")  # 微博
        wei_bo = re.search(pattern_wei_bo, data).group(1)

        pattern_sex = re.compile(r'W_icon\W+icon_pf_(\S+)\W+"\W+\W')   # 性别
        sex = re.search(pattern_sex, data).group(1)
        print("爬取成功，数据====>微博等级: {}, 微博昵称: {}, 微博简介: {}, 关注: {}, 粉丝: {}, 微博: {}, 性别： {}".format(str(weobo_level),
                                                                                    str(weibo_name), str(synopsis),
                                                                                    str(attention), str(fans),
                                                                                    str(wei_bo), str(sex)))
        d = DB()
        d.ex(weobo_level, weibo_name, synopsis, attention, fans, wei_bo, sex)
    except (AttributeError, TypeError):
        print("无效的用户地址")


def main():
    queue = Queue(maxsize=10)
    threadList = ["消费者-1", "消费者-2", "消费者-3",  "消费者-4",  "消费者-5", "消费者-6", "消费者-7", "消费者-8", "消费者-9", "消费者-10"]
    threads = []
    s = scrapy("生产者", queue)
    for tName in threadList:
        thread = Consumer_even(tName, queue)
        thread.start()
        threads.append(thread)
    s.start()
    s.join()


if __name__ == '__main__':
    main()