# -*- coding: utf-8 -*-
# @Time : 2020/11/20 17:43
# @Author : ki9mu
# @File : request.py
# @Software: PyCharm
import requests
class Request():
    url    = ""
    method = ""
    cookie = {}
    headers = {}
    path = ""
    data = ""
    response = ""
    https = "False"
    follow_redirects = False
    def __init__(self,url,method="",cookie = {},headers={},path="",data=""):
        self.url    = url
        self.method = method
        self.path   = path
        self.data   = data
        self.headers = headers

        #如果cookie值不为空
        if cookie != {}:
            #如果header为空
            if headers == {}:
                self.header == self.cookie

            #如果header不为空
            else:
                #遍历cookie中的所有值，添加到headers中
                for cookie_key in cookie:
                    self.headers[cookie_key] = cookie[cookie_key]

        #print("url is {},method is {},path is {},data is {},cookie is {},header is {}".format(self.url,self.method,self.path,self.data,self.cookie,self.headers))


        #判断是否为正常格式
        if self.url[0:6] == "https:":
            self.https = "True"
        if self.url[0:5] == "http:":
            self.https = "False"
        else:
            self.https = "Unknow"


    #请求页面，返回响应内容
    def request(self):
        # 如果为https

        if self.https == "True":

            # 如果为GET请求
            if self.method == "GET":
                pass

            # 如果为POST请求
            if self.method == "POST":
                pass

            # 如果为PUT请求
            if self.method == "PUT":
                pass

            # 如果为HEAD请求
            if self.method == "HEAD":
                pass

        # 如果为http请求
        if self.https == "False":
            # 如果为GET请求
            if self.method == "GET":
                return requests.get(self.url+self.path+self.data,headers=self.headers).text

            # 如果为POST请求
            if self.method == "POST":
                return requests.post(self.url+self.path,self.data,headers=self.headers).text

            # 如果为PUT请求
            if self.method == "PUT":
                pass

            # 如果为HEAD请求
            if self.method == "HEAD":
                pass
