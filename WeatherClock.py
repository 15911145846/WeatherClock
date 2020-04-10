# 一个可以显示天气情况的时钟
# by muzing

# 检测并自动安装第三方库
import ModuleInstall
import pygame, requests
from sys import exit
import time
import json


pygame.init()

# 设置窗口
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Muzing 的天气时钟")
WHITE = (255, 250, 250)


def tq():
    # 调用API，获得并整理 json 文件
    url = 'http://t.weather.sojson.com/api/weather/city/101080101'
    res = requests.get(url)
    tq_txt = res.text
    tq_json = json.loads(tq_txt)
    city = tq_json["cityInfo"]["city"]
    wendu = str(tq_json["data"]["wendu"])
    typ = tq_json["data"]["forecast"][0]["type"]
    sunrise = tq_json["data"]["forecast"][0]["sunrise"]
    sunset = tq_json["data"]["forecast"][0]["sunset"]
    fx = tq_json["data"]["forecast"][0]["fx"]
    fl = tq_json["data"]["forecast"][0]["fl"]
    # air_quality = tq_json["data"]["quality"]
    # shidu = str(tq_json["data"]["shidu"])
    # pm25 = str(tq_json["data"]["pm25"])

    # 对日出日落时间取整，便于设置日出、日落时间段
    if int(sunrise[3]) >= 3:
        sunrise_h = int(sunrise[:2:]) + 1
    else:
        sunrise_h = int(sunrise[:2:])
    if int(sunset[3]) >= 3:
        sunset_h = int(sunset[:2:]) + 1
    else:
        sunset_h = int(sunset[:2:])

    return city, wendu, fx, fl, typ, sunrise_h, sunset_h


def print_tianqi_txt(city, wendu, fx, fl, typ, sunrise_h, sunset_h):
    # 显示天气文本
    font1 = pygame.font.Font('王漢宗中行書繁.ttf', 60)
    font4 = pygame.font.Font('4108_方正魏碑_GBK.ttf', 30)
    tianqi_txt = "{}  {} °C    {} {} ".format(typ, wendu, fx, fl)
    tq_city_txt = font1.render(city, 1, WHITE)
    tianqitxt = font4.render(tianqi_txt, 1, WHITE)
    screen.blit(tianqitxt, (74, 120))
    screen.blit(tq_city_txt, (70, 50))


def print_time_txt(year, mon, dat, h, m, s):
    # 显示时间文本
    font2 = pygame.font.Font('王漢宗中行書繁.ttf', 30)
    font3 = pygame.font.Font('王漢宗中行書繁.ttf', 110)
    date_txt = year + "年" + mon + "月" + dat + "日"
    time_now = ("{}:{}:{}".format(h, m, s))
    datetxt = font2.render(date_txt, 1, WHITE)
    timetxt = font3.render(time_now, 1, WHITE)
    screen.blit(timetxt, (520, 450))
    screen.blit(datetxt, (650, 560))


try:
    tianqi = tq()  # 先获取一次天气信息

# 处理因为请求次数过多API被禁用的异常
except KeyError:
    tianqi = ('Error', '请求次数过多', '', '', '可能是因为', '', '')
    print("错误，可能是因为请求次数过多")

# 处理因为网络未连接的异常
except Exception:
    tianqi = ('Error', '未连接至互联网', '', '', '可能是因为', '', '')
    print("错误，可能是因为网络未连接")


# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # 获得当前日期、时间
    year = time.strftime("%Y", time.localtime(time.time()))  # 当前年数
    mon = time.strftime("%m", time.localtime(time.time()))  # 当前月数
    dat = time.strftime("%d", time.localtime(time.time()))
    m = time.strftime("%M", time.localtime(time.time()))
    h = time.strftime("%H", time.localtime(time.time()))
    s = time.strftime("%S", time.localtime(time.time()))
    inth = int(h)

    # 判断早中晚（stage）
    if tianqi[5] == inth:
        stage = 1
    elif tianqi[6] == inth:
        stage = 2
    else:
        if 6 <= inth < 12:
            stage = 3
        elif 12 <= inth < 15:
            stage = 4
        elif 15 <= inth < 19:
            stage = 5
        elif 19 <= inth < 23:
            stage = 6
        else:
            stage = 7

    # 早中晚切换不同背景
    bg_n = "bg{}.jpg".format(stage)
    bg = pygame.image.load(bg_n)

    # 显示
    screen.blit(bg, (0, 0))  # 背景
    print_time_txt(year, mon, dat, h, m, s)
    print_tianqi_txt(*tianqi)
    pygame.display.flip()
