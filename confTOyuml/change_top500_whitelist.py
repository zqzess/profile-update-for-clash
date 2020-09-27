import re  # 引用re模块
import ruamel.yaml
import sys
import yaml
import json


DATA_URL = 'https://h2y.github.io/Shadowrocket-ADBlock-Rules/sr_top500_whitelist.conf'
tmp = DATA_URL.split("/")
title = tmp[len(tmp) - 1]
title = title.replace(".conf", "")
print(title)
out_fname = './' + title

lin1 = ""
lin2 = ""
bypass = ""
tip = ""
rules = ""
head = """\
# HTTP 端口
port: 7890

# SOCKS5 端口
socks-port: 7891

# Linux 及 macOS 的 redir 端口
# redir-port: 7892

allow-lan: false

# Only applicable when setting allow-lan to true
# "*": bind all IP addresses
# 192.168.122.11: bind a single IPv4 address
# "[aaaa::a8aa:ff:fe09:57d8]": bind a single IPv6 address
# bind-address: "*"

# Rule / Global/ Direct (默认为 Rule 模式)
mode: Rule

# 设置日志等级 (默认为 info)
# info / warning / error / debug / silent
log-level: info

# When set to false, resolver won't translate hostnames to IPv6 addresses
#{% if default(request.ipv6, "false") == "true" or default(request.6to4, "false") == "true" %}
#ipv6: true
#{% else %}
#ipv6: false
#{% endif %}

# RESTful API for clash
external-controller: 127.0.0.1:9090

# you can put the static web resource (such as clash-dashboard) to a directory, and clash would serve in `${API}/ui`
# input is a relative path to the configuration directory or an absolute path
# external-ui: folder

# RESTful API 的口令 (可选)
# secret: ""


# authentication of local SOCKS5/HTTP(S) server
# authentication:
#  - "user1:pass1"
#  - "user2:pass2"

# # experimental hosts, support wildcard (e.g. *.clash.dev Even *.foo.*.example.com)
# # static domain has a higher priority than wildcard domain (foo.example.com > *.example.com)
# hosts:
#   '*.clash.dev': 127.0.0.1
#   'alpha.clash.dev': '::1'

# DNS 设置
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: redir-host
  nameserver:
    - 114.114.114.114
    - 8.8.8.8
    - 119.29.29.29
    - 223.5.5.5
  fallback:
    - https://i.233py.com/dns-query
    
# Clash for Windows
cfw-bypass:
"""
proxy = """\
cfw-latency-timeout: 5000
# 代理节点
proxies:
# Trojan
- name: "trojan"
  type: trojan
  server: type.netctoout.top
  port: 443
  password: password0210
  alpn: 
      - h2
      - http/1.1
# 代理组策略
proxy-groups:

# 代理节点选择
- name: "PROXY"
  type: select
  proxies:
    - "trojan"
# 白名单模式 PROXY，黑名单模式 DIRECT
- name: "Final"
  type: select
  proxies:
    - "PROXY"
    - "DIRECT"
# Apple 服务代理
- name: "Apple"
  type: select
  proxies:
    - "DIRECT"
    - "PROXY"
# 国际流媒体服务
- name: "GlobalMedia"
  type: select
  proxies:
    - "PROXY"
# 直连
- name: "Direct"
  type: select
  proxies:
    - "DIRECT"
# 运营商及网站劫持，广告过滤
- name: "Reject"
  type: select
  proxies:
    - "REJECT"
    - "DIRECT"

# 规则
rules:
"""
endstr = """\
# GeoIP China
- GEOIP,CN,DIRECT

- MATCH,Final
"""
with open(out_fname+".conf", "r", encoding="utf-8") as f1:
    with open(out_fname+".yaml", "w", encoding="utf-8") as f2:
        for lineTmp in f1.readlines():
            if lineTmp.find('skip-proxy') == 0:
                lin1 = lineTmp
                # print(in1)
            elif lineTmp.find('bypass-tun') == 0:
                lin2 = lineTmp
            elif lineTmp.find('# top500 direct list update time') == 0:
                tip = lineTmp
        lin1 = lin1.replace("skip-proxy = ", "")
        lin2 = lin2.replace("bypass-tun = ", "")
        lin1 = lin1 + ","
        bypass = lin1+lin2
        bypass = bypass.strip('\n')
        data = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', bypass)
        # print(data)
        # f2.writelines(bypass)
        # f2.close()
        yaml = ruamel.yaml.YAML()
        code = yaml.load(head)
        proxies = yaml.load(proxy)
        yaml.dump(code, f2)
        yaml.dump(data, f2)
        yaml.dump(proxies, f2)
        f2.write(tip)
        f1.close()
        with open(out_fname+".conf", "r", encoding="utf-8") as f3:
            for searchTmp in f3.readlines():
                if searchTmp.find('DOMAIN-') == 0:
                    rules = "- "+searchTmp
                    f2.write(rules)
                elif searchTmp.find('IP-CIDR') == 0:
                    rules = "- " + searchTmp
                    f2.write(rules)
        endyaml = yaml.load(endstr)
        yaml.dump(endyaml, f2)
        f2.close()
