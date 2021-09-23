#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
# Created on 2021-08-18 19:00
# @author: helix
# Warning 
'''

import io
import sys
import hmac
import json
import time
import base64
import pycurl
import random
import certifi
import hashlib
from urllib import request 
from urllib import parse

WORD_FILE='/usr/lib/zabbix/alertscripts/WORDS/DaoDeJing'
secret = 'SEC~~~~~~~~~~~~~~~~~~~~d'
url = """https://yach-oapi.zhiyinlou.com/robot/send?access_token=O_This_Is_The_Token_String&timestamp=%s&sign=%s"""

def GetUrl():
    timestamp = int(round(time.time() * 1000))
    secret_enc = bytes(secret.encode('utf-8'))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign.encode('utf-8'))
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = request.quote(base64.b64encode(hmac_code))
    return url%(timestamp,sign)


def fortunedao():
    WORD_FILE='/usr/lib/zabbix/alertscripts/WORDS/DaoDeJing'
    a=[]
    with open(WORD_FILE,'r') as f:
        for i in f:
            a.append(i)
    return random.choice(a)

def SendToYach(msg,url):
    full_text = "%s %s" % (time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())), msg)
    response = io.BytesIO()
    send_body = {"msgtype": "text", "text": {"content": str(full_text)}}
    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(c.URL,url)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.setopt(c.HTTPHEADER,
             ['Content-Type: application/json', 'Accept-Charset: UTF-8'])
    c.setopt(c.POSTFIELDS, json.dumps(send_body))
    c.perform()
    c.close()
    response.close()


if __name__ == "__main__":
    geturl = GetUrl()
    text = sys.argv[1]
    textdao = fortunedao()
    outmsg = "\n%s \n  %s"%(text,textdao)
    SendToYach(outmsg,geturl)
