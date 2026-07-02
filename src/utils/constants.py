"""
Shared constants.
"""

# Gravitational-wave event parameters.
EVENT_PARAMS = {
    'GW150914': {
        'event_time': 1126259462.4,
        'start_time': 1126259446,
        'end_time': 1126259478,
        'description': 'First detected binary black-hole merger'
    },
    'GW170817': {
        'event_time': 1187008882.4,
        'start_time': 1187008842,
        'end_time': 1187008922,
        'description': 'Binary neutron-star merger'
    }
}

# Detector colors.
DETECTOR_COLORS = {
    'H1': 'black',      # Hanford
    'L1': 'gray'        # Livingston
}

# Filter parameters.
BANDPASS_RANGE = (50, 250)  # Hz
NOTCH_FREQUENCIES = [60, 120, 180]  # Hz

# Audio parameters.

AUDIO_TIME_WINDOW = 1.5  # seconds
