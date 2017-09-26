#-*- encoding:utf-8 -*-

import requests
import re
import base64,rsa,binascii

def Get_cookies(username,password):
    # url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.15)%'+username
    url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.19)%'+username
    html = requests.get(url).content

    servertime = re.findall('"servertime":(.*?),',html,re.S)[0]
    nonce = re.findall('"nonce":"(.*?)"',html,re.S)[0]
    pubkey = re.findall('"pubkey":"(.*?)"',html,re.S)[0]
    rsakv = re.findall('"rsakv":"(.*?)"',html,re.S)[0]

    username = base64.b64encode(username)

    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    passwd = rsa.encrypt(message, key)
    passwd = binascii.b2a_hex(passwd)

    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
    data = {'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '30',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': username,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': passwd,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv' : rsakv,
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }
    html = requests.post(login_url,data=data).content
    # print html
    urlnew = re.findall('location.replace\(\'(.*?)\'',html,re.S)[0]
    # print urlnew
    # html = requests.get(urlnew)
    html = requests.get(urlnew)
    cookies = html.cookies
    lists = str(cookies).split(' ')
    newStr = ""
    for list in lists:
        if re.findall("=",list):
            newStr += list + '; '
    s = open('C:\Users\DarkSnake\Desktop\cookie.txt', 'w')
    s.write(newStr)
    print cookies
    return cookies

cookies = Get_cookies("18814122672","nba520131400000")
