"""通用工具函数模块。"""

from __future__ import annotations

from .data_datas import empties
from .data_ganzhi import (
    Gan,
    Zhi,
    gan5,
    gan_hes,
    gong_he,
    ten_deities,
    zhi5,
)


def yinyang(item: str) -> str:
    """判断天干/地支的阴阳。"""
    if item in Gan:
        return '＋' if Gan.index(item) % 2 == 0 else '－'
    return '＋' if Zhi.index(item) % 2 == 0 else '－'


def is_yang_gan(gan: str) -> bool:
    """判断天干是否为阳干。"""
    return Gan.index(gan) % 2 == 0


def check_gan(gan: str, gans: tuple | list) -> str:
    """检查天干的合冲关系。"""
    result = ''
    if ten_deities[gan]['合'] in gans:
        result += '合' + ten_deities[gan]['合']
    if ten_deities[gan]['冲'] in gans:
        result += '冲' + ten_deities[gan]['冲']
    return result


def get_empty(day_zhu: tuple, zhi: str) -> str:
    """检查空亡。"""
    empty = empties[day_zhu]
    if zhi in empty:
        return '空'
    return ''


def is_kong_wang(day_zhu: tuple, zhi: str) -> bool:
    """检查是否空亡（返回 bool）。"""
    return zhi in empties[day_zhu]


def get_gen(gan: str, zhis: tuple | list) -> dict:  # noqa: C901
    """计算天干在地支中的根。

    返回 {"强": [...], "中": [...], "弱": [...], "text": "..."} 或 {"无根": True}
    """
    from .data_ganzhi import zhi5_list

    zhus = []
    zhongs = []
    weis = []

    for item in zhis:
        zhu = zhi5_list[item][0]
        if ten_deities[gan]['本'] == ten_deities[zhu]['本']:
            zhus.append(item)

    for item in zhis:
        if len(zhi5_list[item]) == 1:
            continue
        zhong = zhi5_list[item][1]
        if ten_deities[gan]['本'] == ten_deities[zhong]['本']:
            zhongs.append(item)

    for item in zhis:
        if len(zhi5_list[item]) < 3:
            continue
        wei = zhi5_list[item][2]
        if ten_deities[gan]['本'] == ten_deities[wei]['本']:
            weis.append(item)

    if not (zhus or zhongs or weis):
        return {'无根': True, 'text': '无根'}

    parts = []
    if zhus:
        parts.append(f'强：{"".join(zhus)}')
    if zhongs:
        parts.append(f'中：{"".join(zhongs)}')
    if weis:
        parts.append(f'弱：{"".join(weis)}')
    return {
        '强': zhus,
        '中': zhongs,
        '弱': weis,
        '无根': False,
        'text': '　'.join(parts),
    }


def gan_zhi_he(gan: str, zhi: str) -> bool:
    """检查天干地支是否暗合（天干的合在地支藏干中）。"""
    return ten_deities[gan]['合'] in zhi5[zhi]


def get_gong(gans: tuple | list, zhis: tuple | list) -> list:
    """计算地支拱合。"""
    result = []
    for i in range(3):
        if gans[i] != gans[i + 1]:
            continue
        zhi1 = zhis[i]
        zhi2 = zhis[i + 1]
        if abs(Zhi.index(zhi1) - Zhi.index(zhi2)) == 2:
            value = Zhi[(Zhi.index(zhi1) + Zhi.index(zhi2)) // 2]
            result.append(value)
        if (zhi1 + zhi2 in gong_he) and (gong_he[zhi1 + zhi2] not in zhis):
            result.append(gong_he[zhi1 + zhi2])
    return result


def check_gong(
    zhis: tuple | list,
    n1: int,
    n2: int,
    me: str,
    hes: dict,
    desc: str = '三合拱',
) -> str:
    """检查三合/三会的拱合。"""
    result = ''
    key = zhis[n1] + zhis[n2]
    if key in hes:
        gong = hes[key]
        if gong not in zhis:
            detail = get_zhi_detail(gong, me)
            result += f'\t{desc}：{zhis[n1]}{zhis[n2]}-{gong}[{detail}]'
    return result


def get_zhi_detail(zhi: str, me: str, multi: int = 1) -> str:
    """获取地支藏干详细信息。"""
    out = ''
    for gan in zhi5[zhi]:
        out += f'{gan}{gan5[gan]}{zhi5[zhi][gan] * multi}{ten_deities[me][gan]} '
    return out.rstrip()


def is_ku(zhi: str) -> bool:
    """判断地支是否为库。"""
    return zhi in '辰戌丑未'


def zhi_ku(zhi: str, items: tuple) -> bool:
    """判断地支是否为某些天干的库。"""
    return is_ku(zhi) and min(zhi5[zhi], key=zhi5[zhi].get) in items


def gan_ke(gan1: str, gan2: str) -> bool:
    """判断两个天干是否存在相克关系。"""
    return ten_deities[gan1]['克'] == ten_deities[gan2]['本'] or ten_deities[gan2]['克'] == ten_deities[gan1]['本']


def jin_jiao(first: str, second: str) -> bool:
    """判断是否进角。"""
    return Zhi.index(second) - Zhi.index(first) == 1


def calc_direction(year_gan: str, is_female: bool) -> int:
    """计算大运方向。

    返回 1 (顺行) 或 -1 (逆行)。
    """
    seq = Gan.index(year_gan)
    if is_female:
        return -1 if seq % 2 == 0 else 1
    return 1 if seq % 2 == 0 else -1


def calc_dayun_ganzhi(
    month_gan: str,
    month_zhi: str,
    direction: int,
    count: int = 12,
) -> list[str]:
    """计算大运干支序列。"""
    dayuns = []
    gan_seq = Gan.index(month_gan)
    zhi_seq = Zhi.index(month_zhi)
    for _ in range(count):
        gan_seq += direction
        zhi_seq += direction
        dayuns.append(Gan[gan_seq % 10] + Zhi[zhi_seq % 12])
    return dayuns


def calc_gan_he_list(gans: tuple | list) -> list[bool]:
    """计算天干合（相邻才算）。"""
    result = [False, False, False, False]
    for i in range(3):
        if (gans[i], gans[i + 1]) in set(gan_hes) or (gans[i + 1], gans[i]) in set(gan_hes):
            result[i] = result[i + 1] = True
    return result


def calc_zhi_6he(zhis: tuple | list) -> list[bool]:
    """计算地支六合（相邻才算）。"""
    from .data_ganzhi import zhi_atts

    result = [False, False, False, False]
    for i in range(3):
        if zhi_atts[zhis[i]]['六'] == zhis[i + 1]:
            result[i] = result[i + 1] = True
    return result


def calc_zhi_6chong(zhis: tuple | list) -> list[bool]:
    """计算地支六冲（相邻才算）。"""
    from .data_ganzhi import zhi_atts

    result = [False, False, False, False]
    for i in range(3):
        if zhi_atts[zhis[i]]['冲'] == zhis[i + 1]:
            result[i] = result[i + 1] = True
    return result


def calc_zhi_xing(zhis: tuple | list) -> list[bool]:
    """计算地支刑（相邻才算）。"""
    from .data_ganzhi import zhi_atts

    result = [False, False, False, False]
    for i in range(3):
        if zhi_atts[zhis[i]]['刑'] == zhis[i + 1] or zhi_atts[zhis[i + 1]]['刑'] == zhis[i]:
            result[i] = result[i + 1] = True
    return result
