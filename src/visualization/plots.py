"""
绘图模块 - 引力波数据可视化
"""

import matplotlib.pyplot as plt
from gwpy.plot import Plot

def plot_spectral_density(data, title=None, show_power_lines=True):
    """
    绘制振幅谱密度图
    
    参数:
        data: 应变数据
        title: 图表标题
        show_power_lines: 是否显示电源线干扰
    """
    asd = data.asd()
    
    plt.figure(figsize=[10, 6])
    plt.plot(asd.frequencies, asd, color='blue', linewidth=1)
    plt.xlim(10, 2000)
    plt.ylim(1e-24, 1e-19)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('频率 [Hz]')
    plt.ylabel('振幅谱密度 [strain/√Hz]')
    
    if title:
        plt.title(title)
    
    plt.grid(True, alpha=0.3)
    
    # 标记电源线干扰
    if show_power_lines:
        for freq in [60, 120, 180]:
            plt.axvline(freq, linestyle="--", color="red", alpha=0.5)
    
    plt.tight_layout()
    return plt.gcf()

def plot_time_series(original_data, filtered_data, title=None):
    """
    绘制时域信号对比图
    
    参数:
        original_data: 原始数据
        filtered_data: 滤波后数据
        title: 图表标题
    """
    plot = Plot(
        original_data,
        filtered_data,
        figsize=[12, 6],
        separate=True,
        sharex=True,
        color='black'
    )
    
    ax1, ax2 = plot.axes
    
    if title:
        ax1.set_title(title)
    
    ax1.text(1.0, 1.01, '未滤波数据', transform=ax1.transAxes, ha='right')
    ax1.set_ylabel('振幅 [strain]', y=-0.2)
    
    ax2.set_ylabel('')
    ax2.text(1.0, 1.01, '50-250 Hz带通滤波, 60/120/180 Hz陷波',
             transform=ax2.transAxes, ha='right')
    
    return plot

def plot_filter_comparison(original_data, filtered_data, title=None):
    """
    绘制滤波前后频谱对比图
    """
    plt.figure(figsize=[12, 8])
    
    # 原始数据ASD
    asd_original = original_data.asd()
    plt.plot(asd_original.frequencies, asd_original,
             label='原始数据', color='red', alpha=0.7, linewidth=1.5)
    
    # 滤波后数据ASD
    asd_filtered = filtered_data.asd()
    plt.plot(asd_filtered.frequencies, asd_filtered,
             label='滤波后数据', color='blue', alpha=0.7, linewidth=1.5)
    
    plt.xlim(10, 2000)
    plt.ylim(1e-24, 1e-19)
    plt.xlabel('频率 [Hz]')
    plt.ylabel('振幅谱密度 [strain/√Hz]')
    
    # 标记滤波器范围
    plt.axvspan(50, 250, alpha=0.1, color='green', label='带通区域 (50-250 Hz)')
    
    # 标记陷波频率
    for freq in [60, 120, 180]:
        plt.axvline(freq, linestyle="--", color="orange", alpha=0.7)
    
    plt.legend(loc='upper right')
    
    if title:
        plt.title(title)
    
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    
    return plt.gcf()

def plot_q_transform(data, event_time, time_window=0.2):
    """
    绘制Q变换时频图
    
    参数:
        data: 滤波后数据
        event_time: 事件时间
        time_window: 时间窗口(秒)
    """
    hq = data.q_transform(outseg=(event_time-time_window, event_time+time_window/2))
    plot = hq.plot()
    ax = plot.gca()
    plot.colorbar(label="归一化能量")
    ax.grid(False)
    ax.set_yscale('log')
    
    return plot

def plot_detector_comparison(hfilt, lfilt, event_time, event_name):
    """
    绘制双探测器数据对比图
    """
    plot = Plot(figsize=[12, 4])
    ax = plot.gca()
    ax.plot(hfilt, label='LIGO-Hanford', color='black')
    ax.plot(lfilt, label='LIGO-Livingston', color='gray')
    
    ax.set_title(f'LIGO应变数据 ({event_name})')
    ax.set_xlim(event_time-0.3, event_time+0.3)
    ax.set_xscale('seconds', epoch=event_time)
    ax.set_ylabel('振幅 [strain]')
    ax.set_ylim(-1e-21, 1e-21)
    ax.legend()
    
    return plot