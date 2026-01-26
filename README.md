# Minnie-Astrophysics
learn something about astrophysics!

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![GWPy](https://img.shields.io/badge/GWPy-3.0%2B-orange)](https://gwpy.github.io/)

一个用于分析LIGO引力波数据的Python项目，包含信号处理、可视化和宇宙事件的音频转换功能。

## 项目概述

本项目处理和分析来自重大宇宙事件的引力波信：

- **GW150914**: 首次直接探测到的双黑洞合并引力波事件
- **GW170817**: 具有电磁对应体的历史性双中子星合并事件

## 功能特性

- **数据获取**: 直接从LIGO开放科学中心(GWOSC)获取数据
- **频谱分析**: 振幅谱密度(ASD)计算
- **信号滤波**: 带通滤波和电源线噪声消除
- **时频分析**: Q变换用于啁啾信号可视化
- **多探测器对比**: 汉福德与利文斯顿数据关联分析
- **音频转换**: 将引力波信号转换为可听WAV文件

## 项目结构

```py
引力波分析项目/
├── src/                     # 源代码
│   ├── data_processing/     # 数据处理模块
│   ├── visualization/       # 绘图和图表
│   ├── audio_generation/    # WAV文件转换
│   └── utils/               # 工具函数
├── notebooks/               # Jupyter笔记本
│   ├── GW150914_Analysis.ipynb
│   └── GW170817_Analysis.ipynb
├── audio/                   # 生成的音频文件
├── results/                 # 分析结果
│   ├── plots/               # 生成的图表
│   └── comparisons/         # 多探测器研究
├── requirements.txt
└── README.md
```

## 快速开始

### 安装步骤

1. **克隆仓库**

   ```bash
   git clone https://github.com/minnie-0923/Minnie-Astrophysics.git
   cd Minnie-Astrophysics
   ```

2. **安装依赖**

   ```bash
   pip install -r requirement.txt
   ```

### 基本使用

运行主分析笔记本：

```python
# 打开Jupyter笔记本
jupyter notebook notebooks/GW150914_Analysis.ipynb
```

## 分析流程

### 1. 数据获取

从GWOSC获取汉福德(H1)和利文斯顿(L1)观测站的应变数据

### 2. 频谱分析

- 计算振幅谱密度(ASD)
- 识别60Hz、120Hz、180Hz电源线干扰
- 分析噪声特性

### 3. 信号滤波

- 50-250Hz带通滤波器保留引力波特征频段
- 陷波滤波器消除电源线干扰
- 零相位滤波避免信号失真

### 4. 时域分析

- 滤波前后信号对比
- 应变振幅随时间变化
- 事件附近信号细节

### 5. 时频分析

- Q变换显示频率随时间变化
- 啁啾信号特征可视化
- 能量分布分析

### 6. 多站关联

- 汉福德与利文斯顿数据对比
- 时间延迟补偿(6.9ms)
- 相位调整和信号相关性分析

### 7. 音频生成

- 信号归一化处理
- WAV文件格式转换
- 可听化引力波信号

## 技术细节

### 主要依赖库

- **GWPy**: 专业引力波数据分析
- **NumPy/SciPy**: 科学计算和信号处理
- **Matplotlib**: 数据可视化

### 滤波器设计

```python
# 带通滤波器：50-250Hz
bp = filter_design.bandpass(50, 250, hdata.sample_rate)

# 陷波滤波器：消除电源线干扰
notches = [filter_design.notch(line, hdata.sample_rate) for line in (60, 120, 180)]
```

## 结果示例

项目生成多种分析结果：

- 振幅谱密度图
- 滤波前后信号对比
- Q变换时频图
- 多探测器数据关联
- 引力波音频文件

## 物理背景

基于广义相对论，引力波是时空弯曲的涟漪：

- 双黑洞并合产生强烈引力波
- 信号特征：旋近、合并、铃荡三个阶段
- 频率啁啾和振幅增长特性

## 贡献

欢迎提交Issue和Pull Request来改进项目

## 致谢

- LIGO科学合作组织提供开放数据
- GWPy开发团队提供专业分析工具
- 所有为引力波探测做出贡献的科学家
