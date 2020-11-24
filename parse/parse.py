# -*- coding: utf-8 -*-
# @Time : 2020/11/18 13:35
# @Author : ki9mu
# @File : parse.py.py
# @Software: PyCharm

import yaml
import os
import random


def read_poc_file():
    path = './poc'
    dirs = os.listdir(path)
    return dirs


# 生成一个指定长度的随机字符串
def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


class Parse():
    # poc的yaml位置
    poc_filepath = ""
    poc_name = ""
    poc_rules = {}
    poc_set = {}
    poc_data = {}
    set_string = ""
    set_list = []

    def __init__(self, poc_filepath):
        self.poc_filepath = poc_filepath
        self.yaml_parse()
        self.set_parse()

    # 解析yaml文件
    def yaml_parse(self):
        with open(self.poc_filepath, encoding='utf-8') as poc_yaml:
            self.poc_data = yaml.safe_load(poc_yaml)
        self.poc_name = self.poc_data['name']
        self.poc_rules = self.poc_data['rules']
        if 'set' in self.poc_data:
            self.poc_set = self.poc_data['set']

    def set_parse(self):
        # 读取yaml配置文件
        with open('config.yaml', encoding='utf-8') as vary_config:
            vary_translate = yaml.safe_load(vary_config)

        # 遍历变量
        for vary_key, vary_value in self.poc_set.items():

            # 遍历config文件所有变量
            for config_key,config_value in vary_translate.items():

                # 如果set变量的value存在于config文件的key中，替换value中的config_key为config_value
                if config_key in vary_value:
                    self.poc_set[vary_key] = vary_value.replace(config_key,config_value)

        set_string = ""
        for set_key in self.poc_set:
            set_string = set_string + ",self.{}".format(set_key)
        #删除第一个逗号
        set_string = set_string[1:]
        self.set_string = ".format({})".format(set_string)

        set_list = []
        for set_key in self.poc_set:
            set_list.append("{{" + set_key + "}}")
        self.set_list = set_list

    #生成py文件
    def gent_py(self):
        #读取file.py的内容
        file_py = open("file.py","r")
        #写文件
        poc_file = open("./pocpy/" + self.poc_name + ".py","a+")
        poc_file.write(file_py.read())

        #生成类
        poc_file.write("class {}():\n".format(self.poc_name.replace("-","_")))

        #生成类中初始元素
        poc_file.write("    url = \"\"\n")
        #生成类中初始set
        for vary in self.poc_set:
            poc_file.write("    {} = \"\"\n".format(vary))

        #生成构造函数
        poc_file.write("    def __init__(self,url):\n"
                       "        self.url = url\n\n")
        #构造函数写set
        for vary in self.poc_set:
            poc_file.write("        self.{} = {}\n\n".format(vary,self.poc_set[vary]))

        # 遍历每次请求，通常为1次
        i = 0
        for request_i in self.poc_rules:

            # if request_i["follow_redirects"] == True:
            #     poc_file.write("exit(0)\n")
            #     continue
            i = i + 1
            poc_file.write("    def request_{}(self):\n".format(i))
            #写method
            poc_file.write("        method = \"{}\"\n".format(request_i["method"]))
            #写path
            if "path" in request_i:
                poc_file.write("        path = \"{}\"".format(request_i["path"]) + "\n")

                for set_key in self.set_list:
                    if set_key in request_i["path"]:
                        path_temp = "        path = " + request_i["path"].replace(set_key,"{}")
                        path_temp = (str(path_temp)+".format({})".format(set_key[2:-2]))
                        #写入set
                        poc_file.write(path_temp + "\n")

            #写headers
            if "headers" in request_i:
                poc_file.write("        headers = {}\n".format(request_i["headers"]))
                for set_key in self.set_list:
                    if set_key in str(request_i["headers"]):
                        headers_temp = str(request_i["headers"]).replace(set_key,"{}")
                        headers_temp = ("        headers = " + "\'\'\'{"+str(headers_temp) +"}\'\'\'" + ".format({})".format("self."+set_key[2:-2]))
                        #print(headers_temp)
                        poc_file.write(headers_temp + "\n")
            else:
                poc_file.write("        headers = {}\n")

            # #写data
            if "body" in request_i:
                print(request_i["body"])
                print(type(request_i["body"]))
                poc_file.write("        data = \"{}\"\n".format(request_i["body"]))
                for set_key in self.set_list:
                    if set_key in request_i["body"]:
                        data_temp = "        data = \"" + request_i["body"].replace(set_key,"{}") +"\""
                        data_temp = (str(data_temp) + ".format(self.{})".format(set_key[2:-2]))
                        poc_file.write(data_temp + "\n")

            else:
                poc_file.write("        data = \"\"\n")

            # #写请求
            poc_file.write("        connection = request.Request(self.url,method,{},headers,path,data)\n")
            poc_file.write("        responses = connection.request()\n")
            poc_file.write("        print(responses)\n")



if __name__ == '__main__':
    path_list = read_poc_file()
    for i in path_list:
        temp = Parse("./poc/" + i)
        #if temp.poc_rules[0]["follow_redirects"] == False:
        temp.gent_py()
    # temp = Parse("./poc/typecho-rce.yml")
    # temp.gent_py()