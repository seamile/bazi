import json

import pytest
from bzlib.bazi import BaZi


def test_from_solar_comprehensive():
    """综合测试公历创建及所有分析方法"""
    # 1986-10-9 13:00 男 -> 丙寅 戊戌 丙戌 乙未
    bazi = BaZi.from_solar('男', 1986, 10, 9, 13)

    # 1. 基础信息
    info = bazi.basic_info()
    assert info['four_ganzhi'] == ['丙寅', '戊戌', '丙戌', '乙未']
    assert info['day_master'] == '丙'
    assert info['sex'] == '男'

    # 2. 四柱详情 (验证十神、藏干)
    pillars = bazi.four_pillars()
    assert len(pillars['pillars']) == 4
    # 年柱 丙寅: 丙见丙为比肩
    assert pillars['pillars'][0]['gan_shishen'] == '比'
    assert 'jianchu' in pillars

    # 3. 五行分数
    scores = bazi.wuxing_scores()
    assert all(k in scores['scores'] for k in ['金', '木', '水', '火', '土'])
    assert scores['scores']['火'] > 0

    # 4. 神煞
    shens = bazi.shensha()
    # 实际返回结构是按类别分的，如 '年支神煞', '日主神煞' 等
    assert '年支神煞' in shens or '日主神煞' in shens
    # 检查是否有内容
    assert any(len(v) > 0 for v in shens.values() if isinstance(v, list))

    # 5. 六亲
    liuqin = bazi.liuqin()
    # 查找是否存在 "父亲"
    found_father = any(v['liuqin'] == '父亲' for v in liuqin.values())
    assert found_father

    # 6. 脏腑
    zangfu = bazi.zangfu()
    # 结果是统计字典，检查是否包含核心器官
    assert '肝' in zangfu
    assert '肾' in zangfu
    assert zangfu['小肠'] >= 0

    # 7. 格局
    geju = bazi.geju()
    assert '格' in geju
    assert '成格' in geju

    # 8. 命理分析
    analysis = bazi.analysis()
    assert '十神分析' in analysis

    # 9. 特殊星宿
    stars = bazi.special_stars()
    assert isinstance(stars, dict)

    # 10. 古籍查询 (验证 SiZi 和 Yue 数据)
    ref = bazi.reference_texts()
    assert '三命通会' in ref
    assert '穷通宝鉴' in ref
    assert len(ref['三命通会']) > 0


def test_from_lunar_leap_month():
    """测试农历创建，包括闰月"""
    # 1984年闰十月，1984-11-23 10:00 (公历) 是 农历闰十月初一
    # 1984-10-23 是农历十月初一
    # 我们测试一个农历输入
    bazi = BaZi.from_lunar('女', 1984, 10, 1, 10, is_leap_month=True)
    _info = bazi.basic_info()
    # 1984 闰十月 初一 巳时 -> 甲子 乙亥 庚辰 辛巳 (大约)
    # 验证是否成功创建且没有抛错
    # lunar-python 中闰月用负数表示
    assert bazi.basic_info()['lunar']['month'] == -10


def test_dayun_with_liunian():
    """测试大运及流年数据结构"""
    bazi = BaZi.from_solar('男', 1986, 10, 9, 13)
    dayuns = bazi.dayun_with_liunian()

    assert len(dayuns) > 0
    first_dayun = dayuns[0]
    assert 'ganzhi' in first_dayun
    assert 'liunian' in first_dayun
    assert len(first_dayun['liunian']) == 10  # 每步大运10年


def test_serialization():
    """测试各种序列化输出"""
    bazi = BaZi.from_solar('男', 1986, 10, 9, 13)

    # 测试 to_dict 分段
    basic_dict = bazi.to_dict('basic')
    assert basic_dict['day_master'] == '丙'

    # 测试 to_json
    json_output = bazi.to_json(section='wuxing')
    data = json.loads(json_output)
    assert 'scores' in data


def test_invalid_input():
    """测试非法输入"""
    with pytest.raises(ValueError):
        # 非法 section
        bazi = BaZi.from_solar('男', 1986, 10, 9, 13)
        bazi.to_dict('invalid_section')


def test_bazi_gender_logic():
    """测试男女命大运流向逻辑差异"""
    # 丙寅年，阳年。男命顺行，女命逆行。
    male_bazi = BaZi.from_solar('男', 1986, 10, 9, 13)
    female_bazi = BaZi.from_solar('女', 1986, 10, 9, 13)

    # 月柱戊戌
    # 男命第一步大运：己亥 (顺)
    # 女命第一步大运：丁酉 (逆)
    assert male_bazi.dayun()[0]['ganzhi'] == '己亥'
    assert female_bazi.dayun()[0]['ganzhi'] == '丁酉'
