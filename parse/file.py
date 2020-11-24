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

