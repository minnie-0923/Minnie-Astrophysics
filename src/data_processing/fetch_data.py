"""
数据获取模块 - 从GWOSC获取LIGO数据
"""

from gwpy.timeseries import TimeSeries

def fetch_ligo_data(detector, start_time, end_time, cache=False):
    """
    从GWOSC获取LIGO应变数据
    
    参数:
        detector: 探测器 ('H1' 或 'L1')
        start_time: 开始时间 (GPS时间)
        end_time: 结束时间 (GPS时间)
        cache: 是否缓存数据
    
    返回:
        TimeSeries: 应变数据
    """
    print(f"从GWOSC获取 {detector} 数据: {start_time} 到 {end_time}")
    
    try:
        data = TimeSeries.fetch_open_data(detector, start_time, end_time, cache=cache)
        print(f"成功获取 {detector} 数据: {len(data)} 个数据点")
        return data
    except Exception as e:
        print(f"获取数据失败: {e}")
        raise

def fetch_event_data(event_name, detector='H1'):
    """
    获取特定事件的数据
    
    参数:
        event_name: 事件名称 ('GW150914' 或 'GW170817')
        detector: 探测器
    
    返回:
        tuple: (数据, 事件时间, 开始时间, 结束时间)
    """
    from ..utils.constants import EVENT_PARAMS
    
    if event_name not in EVENT_PARAMS:
        raise ValueError(f"未知事件: {event_name}")
    
    params = EVENT_PARAMS[event_name]
    data = fetch_ligo_data(detector, params['start_time'], params['end_time'])
    
    return data, params['event_time'], params['start_time'], params['end_time']