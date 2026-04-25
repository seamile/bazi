#!/usr/bin/env python3
# Author: 钉钉或微信pythontesting 钉钉群21734177
# CreateDate: 2019-2-21

import datas
import ganzhi


def check_gan(gan, gans):
    result = ''
    if ganzhi.ten_deities[gan]['合'] in gans:
        result += '合' + ganzhi.ten_deities[gan]['合']
    if ganzhi.ten_deities[gan]['冲'] in gans:
        result += '冲' + ganzhi.ten_deities[gan]['冲']
    return result


def yinyang(item):
    if item in ganzhi.Gan:
        return '＋' if ganzhi.Gan.index(item) % 2 == 0 else '－'
    else:
        return '＋' if ganzhi.Zhi.index(item) % 2 == 0 else '－'


def yinyangs(zhis):
    result = [yinyang(item) for item in zhis]
    if set(result) == set('＋'):
        print('四柱全阳')
    if set(result) == set('－'):
        print('四柱全阴')


def get_empty(zhu, zhi):
    empty = datas.empties[zhu]
    if zhi in empty:
        return '空'
    return ''


def get_zhi_detail(zhi, me, multi=1):
    out = ''
    for gan in ganzhi.zhi5[zhi]:
        out = out + f'{gan}{ganzhi.gan5[gan]}{ganzhi.zhi5[zhi][gan] * multi}{ganzhi.ten_deities[me][gan]} '
    return out


def check_gong(zhis, n1, n2, me, hes, desc='三合拱'):
    result = ''
    if zhis[n1] + zhis[n2] in hes:
        gong = hes[zhis[n1] + zhis[n2]]
        if gong not in zhis:
            result += f'\t{desc}：{zhis[n1]}{zhis[n2]}-{gong}[{get_zhi_detail(gong, me)}]'
    return result
