# -*- coding: utf-8 -*-
# @Time : 2020/10/22 17:57
# @Author : ki9mu
# @File : shot.py
# @Software: PyCharm

from selenium import webdriver
from time import sleep
import csv

def main():
    #读文件
    f = open("DVR_Login_test.csv")
    reader = csv.reader(f)
    count = 0
    #循环
    for i in reader:
        count = count + 1
        # if i[0]=="url":
        #     continue
        # 访问url
        print(i)
        b = webdriver.Chrome()
        print(type(i[0]))
        b.get(i[0])
        # 输入账号密码
        elem_user = b.find_element_by_id('username')
        elem_pass = b.find_element_by_name('userpwd')
        elem_user.send_keys(i[1])
        elem_pass.send_keys(i[2])
        try:
            button = b.find_element_by_class_name("div_right_thire png")
        except:
            try:
                button = b.find_element_by_class_name("divLoginOne_loginbutton_normal")
            except:
                print(i)
        button.click()
        sleep(3)
        # 截图
        b.get_screenshot_as_file(str(count)+".png")
        # 关闭页面
        sleep(3)
        b.close()

if __name__ == '__main__':
    main()
