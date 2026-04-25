# bzlib - 八字排盘核心库

`bzlib` 是一个专注于八字排盘与命理分析的 Python 核心库。它提供了从公历、农历或直接从八字干支创建排盘对象的能力，并能输出详细的五行分数、神煞、格局、大运流年等结构化分析数据。

## 特性

- **独立性**：完全不依赖于原 CLI 工具，模块化设计，易于集成。
- **三种初始化方式**：支持公历、农历（含闰月）、直接八字输入。
- **结构化输出**：所有分析结果均可作为字典（Dict）或 JSON 字符串获取。
- **深度分析**：集成五行强度计算、神煞扫描、格局判断、脏腑健康、古籍（三命通会、穷通宝鉴）查询等。

## 安装依赖

本项目使用 `lunar-python` 作为历法转换基础。

```bash
pip install lunar-python bidict
```

## 快速开始

### 1. 从公历创建
```python
from bzlib.bazi import BaZi

# 1986年10月9日 13:00 男命
bazi = BaZi.from_solar("男", 1986, 10, 9, 13)

# 获取基础信息
print(bazi.basic_info())
```

### 2. 从农历创建
```python
# 1984年农历闰十月初一 10:00 女命
bazi = BaZi.from_lunar("女", 1984, 10, 1, 10, is_leap_month=True)
```

### 3. 从八字干支创建
```python
# 已知八字直接排盘
bazi = BaZi.from_bazi("男", "丙寅", "戊戌", "丙戌", "乙未")
```

## 核心方法

### 获取分析数据
- `bazi.basic_info()`: 获取性别、出生日期、八字干支等。
- `bazi.four_pillars()`: 获取四柱详情，包含天干十神、地支十神、藏干、纳音、建除十二神等。
- `bazi.wuxing_scores()`: 获取五行分数统计、身强身弱判断。
- `bazi.shensha()`: 获取各柱神煞（年支、月支、日主等）。
- `bazi.dayun()`: 获取大运列表及起运时间。
- `bazi.dayun_with_liunian()`: 获取包含每步大运下 10 年流年的详细列表。
- `bazi.geju()`: 获取格局、调候、金不换等命理判断。
- `bazi.reference_texts()`: 查询《三命通会》和《穷通宝鉴》中的相关论述。

### 序列化输出
```python
# 获取完整报告的字典
report = bazi.full_report()

# 获取特定部分的 JSON
json_data = bazi.to_json(section="wuxing")
```

## 开发与测试

在根目录下运行测试：

```bash
PYTHONPATH=. pytest test/test_bzlib.py
```

## 目录结构

- `bazi.py`: 库的门面类，负责对外接口。
- `calculator.py`: 核心计算引擎，负责基础干支与分数的计算。
- `analyzer.py`: 命理分析逻辑。
- `dayun.py`: 大运与流年计算。
- `shensha.py`: 神煞扫描逻辑。
- `data/`: 存放基础数据、古籍文本。
