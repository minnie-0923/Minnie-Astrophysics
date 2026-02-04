"""
音频文件生成模块
"""

import numpy as np
from scipy.io.wavfile import write

def signal_to_audio(time_data, amplitude_data, event_time, time_window=1.5):
    """
    将信号数据转换为音频数据
    
    参数:
        time_data: 时间数组
        amplitude_data: 振幅数组
        event_time: 事件时间
        time_window: 时间窗口(秒)
    
    返回:
        tuple: (采样率, 音频数据)
    """
    # 提取事件附近的数据
    mask = (time_data < (event_time + time_window)) & (time_data > (event_time - time_window))
    y = amplitude_data[mask]
    
    # 信号归一化处理
    y = y / np.max(np.abs(y))
    
    # 计算实际采样率
    time_diff = np.diff(time_data[mask])
    fs = int(1 / np.median(time_diff))
    
    # 转换为16位整数格式
    amplitude = np.iinfo(np.int16).max
    audio_data = (np.array(y) * amplitude).astype(np.int16)
    
    return fs, audio_data

def generate_gravitational_wave_audio(time_data, amplitude_data, event_time, 
                                    filename=None, event_name="GW"):
    """
    生成引力波音频文件
    
    参数:
        time_data: 时间数组
        amplitude_data: 振幅数组
        event_time: 事件时间
        filename: 输出文件名
        event_name: 事件名称
    """
    if filename is None:
        filename = f"gravitational_wave_{event_name}.wav"
    
    # 转换为音频数据
    fs, audio_data = signal_to_audio(time_data, amplitude_data, event_time)
    
    # 生成WAV文件
    write(filename, fs, audio_data)
    
    print(f"音频文件已生成: {filename}")
    print(f"采样率: {fs} Hz")
    print(f"音频长度: {len(audio_data)/fs:.2f} 秒")
    
    return filename, fs, audio_data