# -*- coding: utf-8 -*-
from time import sleep

import requests
import re

headers = {"Cookie": "SINAGLOBAL=6652408980066.204.1503545508516; SCF=AlKzIm9-tDQgT2Q2lWqdTqGdPfnGEdBiwOO7RcEmgaBD8CDyneJL0IkZYiDUfoZ_h1sOhE5dFANU6pxk5LkbNP0.; SUHB=0P1MuJuKSXIfOA; ALF=1535706873; YF-Ugrow-G0=5b31332af1361e117ff29bb32e4d8439; SUB=_2AkMu9ZsRdcPxrAZUkfAXxGPqbYpH-jydIPLnAn7uJhIyOhgv7kYXqSVLgKgtc54gRueiBO1dxcLja7tplA..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFZLx_046ao7yGuungapxi95JpX5KMhUgL.Fo-f1KnE1hnReKM2dJLoIpjLxKqL1KqL1hMLxKnLBoBLBKBLxK-LBo.LBoet; login_sid_t=a4907a4afc1fc10d5cadd7ca20fe44f3; cross_origin_proto=SSL; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; _s_tentry=passport.weibo.com; UOR=,,www.baidu.com; Apache=1506461520797.3774.1504252940079; ULV=1504252940087:2:1:1:1506461520797.3774.1504252940079:1503545508560; YF-Page-G0=c6cf9d248b30287d0e884a20bac2c5ff; wb_cusLike_undefined=N"}
url = "https://weibo.com/p/1005055179617625/home?is_hot=1"

results = requests.get(url, cookies=headers)
# print results.status_code
# pattern = re.compile(r'<a\s+class=\W"W_icon_level icon_level_c\d+\W"\s+title=\W+(\d+)')  # 微博等级
# print(re.search(pattern, results.text)).group(1)

# pattern = re.compile(r"\WCONFIG\W+onick\W+=\W(\S+)")
# # print pattern.findall(results.text)
# print(re.search(pattern, results.text)).group(0).split("=")[1].strip("'").strip(";").strip("'")  # 微博昵称


# pattern = re.compile(r'<meta\W+content=\W(\S+)\W+name=\Wdescription')   # 微博简介
# print(re.search(pattern, results.text)).group(1)

# pattern =re.compile(ur"\W(\d+)\W+strong\W+span\W+class\W+S_txt2\W+\S+\W+span\W+")   # 关注
# print(re.search(pattern, results.text)).group(1)

# pattern = re.compile(ur"\W(\d+)\W+strong\W+span\W+class=\W+S_txt2\W+\u7c89\u4e1d")  # 粉丝
# print(re.search(pattern, results.text)).group(1)

# pattern = re.compile(ur"\W(\d+)\W+strong\W+span\W+class=\W+S_txt2\W+\u5fae\u535a")  # 微博
# print(re.search(pattern, results.text)).group(1)

pattern = re.compile(r'W_icon\W+icon_pf_(\S+)\W+"\W+\W')  # 性别
print(re.search(pattern, results.text)).group(1)

