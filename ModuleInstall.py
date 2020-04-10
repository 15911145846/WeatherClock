# 用于检测并自动安装需要的第三方模块

try:
    import pygame
except ModuleNotFoundError:
    print("检测到未安装 pygame 模块，开始自动安装")
    import os
    os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pygame")


try:
    import requests
except ModuleNotFoundError:
    print("检测到未安装requests模块，开始自动安装")
    import os
    os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests")