"""古籍查询模块 - 六十日用法口诀、穷通宝鉴、三命通会、十二时辰吉凶。"""

from __future__ import annotations

from .data_datas import chens, days60, jianchus
from .data_ganzhi import Zhi
from .data_sizi import summarys
from .data_yue import months


class ReferenceTexts:
    """古籍文本查询器。"""

    def __init__(self, me: str, zhis: tuple, zhus: list):
        self.me = me
        self.zhis = zhis
        self.zhus = zhus

    def get_all(self) -> dict:
        """获取所有古籍查询结果。"""
        return {
            '六十日用法口诀': self.get_days60(),
            '穷通宝鉴': self.get_qiongtong(),
            '三命通会': self.get_sanming(),
            '十二时辰吉凶': self.get_shichen(),
        }

    def get_days60(self) -> str:
        """六十日用法口诀。"""
        key = self.me + self.zhis[2]
        return days60.get(key, '')

    def get_qiongtong(self) -> str:
        """穷通宝鉴。"""
        key = self.me + self.zhis[1]
        return months.get(key, '')

    def get_sanming(self) -> str:
        """三命通会。"""
        key = ''.join([self.me, '日', *self.zhus[3]])
        return summarys.get(key, '')

    def get_shichen(self) -> str:
        """十二时辰（初中末）出生吉凶。"""
        return chens.get(self.zhis[3], '')

    def get_jianchu(self) -> dict:
        """建除。"""
        seq = 12 - Zhi.index(self.zhis[1])
        idx = (Zhi.index(self.zhis[2]) + seq) % 12
        name, desc = jianchus[idx]
        return {'name': name, 'desc': desc}
