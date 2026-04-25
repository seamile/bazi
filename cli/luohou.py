#!/usr/bin/env python3
# Author: 钉钉或微信pythontesting 钉钉群21734177 技术支持qq群：630011153 144081101
# 代码地址 https://github.com/china-testing/python-api-tesing/blob/master/bazi/luohou.py
# 鸣谢 https://github.com/yuangu/sxtwl_cpp/tree/master/python
# CreateDate: 2019-2-21

import argparse
import collections
import datetime

import sxtwl
from colorama import init
from ganzhi import Gan, Zhi, datouxiu, get_jizhu, jis, xiaotouxiu, zhi_atts, zhi_time
from lunar_python import Lunar


def get_hou(d, xiazhi, dongzhi):  # noqa: C901
    cal_day = sxtwl.fromSolar(d.year, d.month, d.day)
    lunar = Lunar.fromYmd(cal_day.getLunarYear(), cal_day.getLunarMonth(), cal_day.getLunarDay())
    # ba = lunar.getEightChar()
    # yun = ba.getYun(1)

    # 计算甲干相合
    # gz = cal_day.getHourGZ(10)
    y_tg = cal_day.getYearGZ()
    m_tg = cal_day.getMonthGZ()
    d_tg = cal_day.getDayGZ()

    gans = Gans(year=Gan[y_tg.tg], month=Gan[m_tg.tg], day=Gan[d_tg.tg])
    zhis = Zhis(year=Zhi[y_tg.dz], month=Zhi[m_tg.dz], day=Zhi[d_tg.dz])

    print('公历:', end='')
    print(f'{d.year}年{d.month}月{d.day}日', end='')

    lleap = '闰' if cal_day.isLunarLeap() else ''
    print('\t农:', end='')
    print(f'{cal_day.getLunarYear()}年{lleap}{cal_day.getLunarMonth()}月{cal_day.getLunarDay()}日  ', end='')
    print(' ', end='')
    print(''.join([''.join(item) for item in zip(gans, zhis, strict=False)]), end='')

    print('\t杀:', end='')
    for item in shi_hous[zhis[2]]:
        print(item + zhi_time[item], end='')

    day_ganzhi = gans[2] + zhis[2]

    if day_ganzhi == year_hous[zhis[0]]:
        print(f' 年猴:{zhis[0]}年{day_ganzhi}日', end=' ')

    if zhis[2] == yue_hous[cal_day.getLunarMonth()]:
        print(f' 月罗:{zhis[2]}日', end=' ')

    if day_ganzhi in tuple(ji_hous.values()):
        birthday = d
        for _ in range(30):
            day_ = sxtwl.fromSolar(birthday.year, birthday.month, birthday.day)
            if day_.hasJieQi():
                ji = jis[(day_.getJieQi() + 3) // 6]
                break
            birthday += datetime.timedelta(days=-1)

        if day_ganzhi == ji_hous[ji]:
            print(f' \t季猴:{ji}季{ji_hous[ji]}日', end=' ')

    if d >= xiazhi and d < dongzhi:
        items = shi_feixings2[Zhi[d_tg.dz]]
    else:
        items = shi_feixings1[Zhi[d_tg.dz]]
    print()
    print(' ' * 90, lunar.getDayNineStar(), end='')
    for item in Zhi:
        print(f' {item}{items[item]}', end='')
    print()
    zeri = ''
    if zhis.day == zhi_atts[zhis.year]['冲']:
        zeri += '\t岁破，大事不宜'
    elif zhis.day == zhi_atts[zhis.month]['冲']:
        zeri += '\t月破，大事不宜'
    # print(gans.day + zhis.day)
    if gans.day + zhis.day in datouxiu:
        zeri += '\t大偷休'
    elif gans.day + zhis.day in xiaotouxiu:
        zeri += '\t小偷休'
    print(zeri)


init(autoreset=True)

jiuxings_dsp = """
    一白水星 —— + 贪狼：事业、人缘与桃花
    二黑土星 —— x 巨门：病符
    三碧木星 —— x 禄存：口舌是非、诉讼官非
    四绿木星 —— + 文曲：智慧，学业
    五黄土星 —— x 廉贞：招灾惹祸甚至病痛；
    六白金星 —— + 武曲：权力、事业、驿马
    七赤金星 —— x 破军：盗贼、小人
    八白土星 —— + 左辅：财星 钱财
    九紫火星 —— + 右弼：婚姻喜庆"""

mountains = {
    '甲': '',
    '卯': '',
    '乙': '',
    '辰': '',
    '巽': '',
    '巳': '',
    '丙': '',
    '午': '',
    '丁': '',
    '未': '',
    '坤': '',
    '申': '',
    '庚': '',
    '酉': '',
    '辛': '',
    '戌': '',
    '乾': '',
    '亥': '',
    '壬': '',
    '子': '',
    '癸': '',
    '丑': '',
    '艮': '',
    '寅': '',
}


year_hous = {
    '子': '癸酉',
    '丑': '甲戌',
    '寅': '丁亥',
    '卯': '甲子',
    '辰': '乙丑',
    '巳': '甲寅',
    '午': '丁卯',
    '未': '甲辰',
    '申': '己巳',
    '酉': '甲午',
    '戌': '丁未',
    '亥': '甲申',
}

ji_hous = {'春': '乙卯', '夏': '丙午', '秋': '庚申', '冬': '辛酉'}
yue_hous = {
    1: '亥',
    2: '子',
    3: '丑',
    4: '寅',
    5: '卯',
    6: '辰',
    7: '巳',
    8: '午',
    9: '未',
    10: '申',
    11: '酉',
    12: '戌',
}
shi_hous = {
    '子': '丑午',
    '丑': '巳亥',
    '寅': '寅午',
    '卯': '辰戌',
    '辰': '巳丑',
    '巳': '辰戌',
    '午': '卯申',
    '未': '午辰',
    '申': '戌丑',
    '酉': '子午',
    '戌': '卯午',
    '亥': '辰卯',
}
fangweis = [
    '九紫火',
    '一白水',
    '二黑土',
    '三碧木',
    '四绿木',
    '五黄土',
    '六白金',
    '七赤金',
    '八白土',
]
zheng_jiuxings = {
    1: '八白土',
    2: '七赤金',
    3: '六白金',
    4: '五黄土',
    5: '四绿木',
    6: '三碧木',
    7: '二黑土',
    8: '一白水',
    9: '九紫火',
    10: '八白土',
    11: '七赤金',
    12: '六白金',
}
sheng_jiuxings = {
    1: '二黑土',
    2: '一白水',
    3: '九紫火',
    4: '八白土',
    5: '七赤金',
    6: '六白金',
    7: '五黄土',
    8: '四绿木',
    9: '三碧木',
    10: '二黑土',
    11: '一白水',
    12: '九紫火',
}
ku_jiuxings = {
    1: '五黄土',
    2: '四绿木',
    3: '三碧木',
    4: '二黑土',
    5: '一白水',
    6: '九紫火',
    7: '八白土',
    8: '七赤金',
    9: '六白金',
    10: '五黄土',
    11: '四绿木',
    12: '三碧木',
}

zheng_jiuxings_shi = {
    '子': 1,
    '丑': 2,
    '寅': 3,
    '卯': 4,
    '辰': 5,
    '巳': 6,
    '午': 7,
    '未': 8,
    '申': 9,
    '酉': 1,
    '戌': 2,
    '亥': 3,
}
ku_jiuxings_shi = {
    '子': 4,
    '丑': 5,
    '寅': 6,
    '卯': 7,
    '辰': 8,
    '巳': 9,
    '午': 1,
    '未': 2,
    '申': 3,
    '酉': 4,
    '戌': 5,
    '亥': 6,
}
sheng_jiuxings_shi = {
    '子': 7,
    '丑': 8,
    '寅': 9,
    '卯': 1,
    '辰': 2,
    '巳': 3,
    '午': 4,
    '未': 5,
    '申': 6,
    '酉': 7,
    '戌': 8,
    '亥': 9,
}

zheng_jiuxings_shi2 = {
    '子': 9,
    '丑': 8,
    '寅': 7,
    '卯': 6,
    '辰': 5,
    '巳': 4,
    '午': 3,
    '未': 2,
    '申': 1,
    '酉': 9,
    '戌': 8,
    '亥': 7,
}
ku_jiuxings_shi2 = {
    '子': 6,
    '丑': 5,
    '寅': 4,
    '卯': 3,
    '辰': 2,
    '巳': 1,
    '午': 9,
    '未': 8,
    '申': 7,
    '酉': 6,
    '戌': 5,
    '亥': 4,
}
sheng_jiuxings_shi2 = {
    '子': 3,
    '丑': 2,
    '寅': 1,
    '卯': 9,
    '辰': 8,
    '巳': 7,
    '午': 6,
    '未': 5,
    '申': 4,
    '酉': 3,
    '戌': 2,
    '亥': 1,
}

month_feixings = {
    '子': zheng_jiuxings,
    '丑': ku_jiuxings,
    '寅': sheng_jiuxings,
    '卯': zheng_jiuxings,
    '辰': ku_jiuxings,
    '巳': sheng_jiuxings,
    '午': zheng_jiuxings,
    '未': ku_jiuxings,
    '申': sheng_jiuxings,
    '酉': zheng_jiuxings,
    '戌': ku_jiuxings,
    '亥': sheng_jiuxings,
}

shi_feixings1 = {
    '子': zheng_jiuxings_shi,
    '丑': ku_jiuxings_shi,
    '寅': sheng_jiuxings_shi,
    '卯': zheng_jiuxings_shi,
    '辰': ku_jiuxings_shi,
    '巳': sheng_jiuxings_shi,
    '午': zheng_jiuxings_shi,
    '未': ku_jiuxings_shi,
    '申': sheng_jiuxings_shi,
    '酉': zheng_jiuxings_shi,
    '戌': ku_jiuxings_shi,
    '亥': sheng_jiuxings_shi,
}

shi_feixings2 = {
    '子': zheng_jiuxings_shi2,
    '丑': ku_jiuxings_shi2,
    '寅': sheng_jiuxings_shi2,
    '卯': zheng_jiuxings_shi2,
    '辰': ku_jiuxings_shi2,
    '巳': sheng_jiuxings_shi2,
    '午': zheng_jiuxings_shi2,
    '未': ku_jiuxings_shi2,
    '申': sheng_jiuxings_shi2,
    '酉': zheng_jiuxings_shi2,
    '戌': ku_jiuxings_shi2,
    '亥': sheng_jiuxings_shi2,
}

Gans = collections.namedtuple('Gans', 'year month day')
Zhis = collections.namedtuple('Zhis', 'year month day')
JiuFeiXing = collections.namedtuple('JiuFeiXing', '中 西北 西 东北 南 北 西南 东 东南')


description = """
# 年罗猴日
$ python luohou.py -d "2019 6 16"

"""

parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-d', action='store', help='year', default='')
parser.add_argument('-n', action='store', help='days', default=32, type=int)
parser.add_argument('--version', action='version', version='%(prog)s 0.1 Rongzhong xu 2019 05 05')
options = parser.parse_args()

Gans = collections.namedtuple('Gans', 'year month day')
Zhis = collections.namedtuple('Zhis', 'year month day')

if options.d:
    year, month, day = options.d.split()
    d = datetime.datetime(int(year), int(month), int(day))
else:
    d = datetime.datetime.today()

cal_day = sxtwl.fromSolar(d.year, d.month, d.day)
y_tg = cal_day.getYearGZ()
m_tg = cal_day.getMonthGZ()
d_tg = cal_day.getDayGZ()


gans = Gans(year=Gan[y_tg.tg], month=Gan[m_tg.tg], day=Gan[d_tg.tg])
zhis = Zhis(year=Zhi[y_tg.dz], month=Zhi[m_tg.dz], day=Zhi[d_tg.dz])
mountains[zhis.year] += ' 太岁'
mountains[zhi_atts[zhis.year]['冲']] += ' 岁破'


# 计算中央位
year = d.year
index = year % 10 + year // 10 % 10
index = index - 9 if index > 9 else index
index = 9 - index
# print(index)
jius = JiuFeiXing(*fangweis[index:], *fangweis[0:index])
# print(jius)

print(jiuxings_dsp)
print('-' * 120)
print(f'{year}年九宫飞星')
print('-' * 120)
print(
    '\033[1;36;40m{1:{0}<25s}{2:{0}<25s}{3:{0}<25s}\033[0m'.format(
        chr(12288),
        f'巽 东南：{jius.东南}',
        f'离   南：{jius.南}',
        f'坤 西南：{jius.西南}',
    )
)
print(
    '\033[1;36;40m{1:{0}<25s}{2:{0}<25s}{3:{0}<25s}\033[0m'.format(
        chr(12288),
        f'震   东：{jius.东}',
        f'  中   央：{jius.中}',
        f'    兑   西：{jius.西}',
    )
)
print(
    '\033[1;36;40m{1:{0}<25s}{2:{0}<25s}{3:{0}<25s}\033[0m'.format(
        chr(12288),
        f'艮 东北：{jius.东北}',
        f'坎   北：{jius.北}',
        f'乾 西北：{jius.西北}',
    )
)
print('-' * 120)

print('月份九宫飞星', end=' ')
items = month_feixings[Zhi[y_tg.dz]]
for i in range(1, 13):
    print(i, items[i], end=' ')
print()
year_yas = get_jizhu(Gan[y_tg.tg], Zhi[y_tg.dz])
print('太岁压祭主', year_yas)
day_yas = get_jizhu(Gan[d_tg.tg], Zhi[d_tg.dz])
print('日压祭主', day_yas)
print('-' * 120)

# 计算夏至日、冬至日
lunar = Lunar.fromYmd(d.year, d.month, d.day)
jieqis = lunar.getJieQiTable()
# start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
# print("去年冬至", jieqis['冬至'].toFullString())
# print("雨水", jieqis['雨水'].toFullString())
# print("谷雨", jieqis['谷雨'].toFullString())
# print("夏至", jieqis['夏至'].toFullString())
# print("处暑", jieqis['处暑'].toFullString())
# print("霜降", jieqis['霜降'].toFullString())
# print("今年冬至", jieqis['DONG_ZHI'].toFullString())
xiazhi = datetime.datetime.strptime(' '.join(jieqis['夏至'].toFullString().split(' ')[:2]), '%Y-%m-%d %H:%M:%S')
dongzhi = datetime.datetime.strptime(' '.join(jieqis['DONG_ZHI'].toFullString().split(' ')[:2]), '%Y-%m-%d %H:%M:%S')


get_hou(d, xiazhi, dongzhi)

for i in range(1, options.n):
    d_ = d + datetime.timedelta(days=i)
    get_hou(d_, xiazhi, dongzhi)
