import wget
import tarfile
import os
import time

# 网络地址
DATA_URL = 'https://h2y.github.io/Shadowrocket-ADBlock-Rules/sr_top500_whitelist.conf'
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
with open(out_fname, "r", encoding="utf-8") as f1:
    content = f1.read()
    f1.close()
    with open(out_fname, "w", encoding="utf-8") as f2:
        content = content.replace("Proxy", "PROXY")
        f2.write(content)
        f2.close()
os.system('python ./change_top500_whitelist.py')
os.remove(out_fname)
