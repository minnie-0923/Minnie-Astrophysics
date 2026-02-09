"""
常量定义
"""

# 引力波事件参数
EVENT_PARAMS = {
    'GW150914': {
        'event_time': 1126259462.4,
        'start_time': 1126259446,
        'end_time': 1126259478,
        'description': '首个黑洞合并事件'
    },
    'GW170817': {
        'event_time': 1187008882.4,
        'start_time': 1187008842,
        'end_time': 1187008922,
        'description': '中子星合并事件'
    }
}

# 探测器颜色
DETECTOR_COLORS = {
    'H1': 'black',      # Hanford
    'L1': 'gray'        # Livingston
}

# 滤波器参数
BANDPASS_RANGE = (50, 250)  # Hz
NOTCH_FREQUENCIES = [60, 120, 180]  # Hz

# 音频参数

AUDIO_TIME_WINDOW = 1.5  # 秒
