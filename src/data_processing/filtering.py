"""
信号滤波模块
"""

from gwpy.signal import filter_design

def design_filters(sample_rate):
    """
    设计滤波器组
    
    参数:
        sample_rate: 采样率
    
    返回:
        tuple: (带通滤波器, 陷波滤波器列表, 合并滤波器)
    """
    # 设计带通滤波器 (50-250Hz)
    bp = filter_design.bandpass(50, 250, sample_rate)
    
    # 设计陷波滤波器消除电源线干扰
    notches = [filter_design.notch(line, sample_rate) for line in (60, 120, 180)]
    
    # 合并滤波器
    zpk = filter_design.concatenate_zpks(bp, *notches)
    
    return bp, notches, zpk

def apply_filters(data, zpk, crop_edges=True):
    """
    应用滤波器到数据
    
    参数:
        data: 输入数据
        zpk: 滤波器
        crop_edges: 是否裁剪边界
    
    返回:
        TimeSeries: 滤波后数据
    """
    # 应用滤波器
    filtered_data = data.filter(zpk, filtfilt=True)
    
    # 裁剪数据边界以避免边缘效应
    if crop_edges:
        data = data.crop(*data.span.contract(1))
        filtered_data = filtered_data.crop(*filtered_data.span.contract(1))
    
    return filtered_data

def process_signal(data):
    """
    完整的信号处理流程
    
    参数:
        data: 原始数据
    
    返回:
        tuple: (滤波后数据, 滤波器)
    """
    # 设计滤波器
    bp, notches, zpk = design_filters(data.sample_rate)
    
    # 应用滤波器
    filtered_data = apply_filters(data, zpk)
    
    return filtered_data, zpk