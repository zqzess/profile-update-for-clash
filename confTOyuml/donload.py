# -*- coding: utf-8 -*-

import wget
import tarfile
import os
import time

# 网络地址
DATA_URL = 'https://raw.githubusercontent.com/h2y/Shadowrocket-ADBlock-Rules/master/sr_top500_whitelist_ad.conf'
# 本地硬盘文件
# DATA_URL = 'C://code//python//gitUpdateYuml//base.yaml'
tmp = DATA_URL.split("/")
title = tmp[len(tmp) - 1]
# print("文件名:"+title)
out_fname = './' + title
if os.path.exists(out_fname):
    os.remove(out_fname)
    print("文件存在，已执行删除")
wget.download(DATA_URL, out=out_fname)
with open("./sr_top500_whitelist_ad.conf", "r", encoding="utf-8") as f1:
    content = f1.read()
    f1.close()
    with open("./sr_top500_whitelist_ad.conf", "w", encoding="utf-8") as f2:
        content = content.replace("Proxy", "PROXY")
        f2.write(content)
        f2.close()
os.system('python ./yumlChange.py')
print("白名单去广告完成")
os.remove(out_fname)
os.system('python ./DL_top500_banlist.py')
print("黑名单完成")
os.system('python ./DL_top500_whitelist.py')
print("白名单完成")
