import pygame
from sys import exit
import time
import requests
import json

pygame.init()

# 设置窗口
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Muzing 的天气时钟")
WHITE = (255, 250, 250)


def tq():
    # 整理 json 文件
    url = 'http://t.weather.sojson.com/api/weather/city/101010100'
    res = requests.get(url)
    tq_txt = res.text
    tq_json = json.loads(tq_txt)
    city = tq_json["cityInfo"]["city"]
    air_quality = tq_json["data"]["quality"]
    wendu = str(tq_json["data"]["wendu"])
    shidu = str(tq_json["data"]["shidu"])
    pm25 = str(tq_json["data"]["pm25"])
    typ = tq_json["data"]["forecast"][0]["type"]
    sunrise = tq_json["data"]["forecast"][0]["sunrise"]
    sunset = tq_json["data"]["forecast"][0]["sunset"]
    fx = tq_json["data"]["forecast"][0]["fx"]
    fl = tq_json["data"]["forecast"][0]["fl"]

    # 对日出日落时间取整，便于设置清晨、傍晚 时间段
    if int(sunrise[3]) >= 3:
        sunrise_h = int(sunrise[:2:]) + 1
    else:
        sunrise_h = int(sunrise[:2:])
    if int(sunset[3]) >= 3:
        sunset_h = int(sunset[:2:]) + 1
    else:
        sunset_h = int(sunset[:2:])
    return city, air_quality, wendu, shidu, pm25, typ, sunrise_h, sunset_h, fx, fl


def print_tianqi_txt(city, wendu, fx, fl, typ):
    # 文本
    font1 = pygame.font.Font('王漢宗中行書繁.ttf', 60)
    font4 = pygame.font.Font('4108_方正魏碑_GBK.ttf', 30)

    tianqi_txt = "{}  {} °C    {} {} ".format(typ, wendu, fx, fl)
    tq_city_txt = font1.render(city, 1, WHITE)
    tianqitxt = font4.render(tianqi_txt, 1, WHITE)

    screen.blit(tianqitxt, (74, 120))
    screen.blit(tq_city_txt, (70, 50))


def print_time_txt():
    # 当前日期
    year = time.strftime("%Y", time.localtime(time.time()))  # 当前年数
    mon = time.strftime("%m", time.localtime(time.time()))  # 当前月数
    dat = time.strftime("%d", time.localtime(time.time()))  # 当前日数
    h = time.strftime("%H", time.localtime(time.time()))
    m = time.strftime("%M", time.localtime(time.time()))
    s = time.strftime("%S", time.localtime(time.time()))

    font2 = pygame.font.Font('王漢宗中行書繁.ttf', 30)
    font3 = pygame.font.Font('王漢宗中行書繁.ttf', 110)
    date_txt = year + "年" + mon + "月" + dat + "日"
    time_now = ("{}:{}:{}".format(h, m, s))
    datetxt = font2.render(date_txt, 1, WHITE)
    timetxt = font3.render(time_now, 1, WHITE)
    screen.blit(timetxt, (520, 450))
    screen.blit(datetxt, (650, 560))


tianqi = tq()
# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    m = int(time.strftime("%M", time.localtime(time.time())))
    h = int(time.strftime("%H", time.localtime(time.time())))

    # 整点和半点刷新天气数据
    if m == 0 or m == 30:
        tianqi = tq()
        time.sleep(1)

    # 判断早中晚
    if tianqi[6] == h:
        stage = 1
    elif tianqi[7] == h:
        stage = 2
    else:
        if 6 <= h < 12:
            stage = 3
        elif 12 <= h < 15:
            stage = 4
        elif 15 <= h < 19:
            stage = 5
        elif 19 <= h < 23:
            stage = 6
        else:
            stage = 7

    # 早中晚切换不同背景
    bg_n = "bg{}.jpg".format(stage)
    bg = pygame.image.load(bg_n)

    # 显示
    screen.blit(bg, (0, 0))
    print_time_txt()
    print_tianqi_txt(tianqi[0], tianqi[2], tianqi[8], tianqi[9], tianqi[5])
    pygame.display.flip()
