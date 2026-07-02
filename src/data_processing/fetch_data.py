"""
Data acquisition utilities for downloading LIGO data from GWOSC.
"""

from gwpy.timeseries import TimeSeries

def fetch_ligo_data(detector, start_time, end_time, cache=False):
    """
    Fetch LIGO strain data from GWOSC.
    
    Args:
        detector: Detector name ('H1' or 'L1').
        start_time: Start time in GPS seconds.
        end_time: End time in GPS seconds.
        cache: Whether to cache downloaded data.
    
    Returns:
        TimeSeries: Strain data.
    """
    print(f"Fetching {detector} data from GWOSC: {start_time} to {end_time}")
    
    try:
        data = TimeSeries.fetch_open_data(detector, start_time, end_time, cache=cache)
        print(f"Fetched {detector} data successfully: {len(data)} samples")
        return data
    except Exception as e:
        print(f"Data fetch failed: {e}")
        raise

def fetch_event_data(event_name, detector='H1'):
    """
    Fetch data for a specific event.
    
    Args:
        event_name: Event name ('GW150914' or 'GW170817').
        detector: Detector name.
    
    Returns:
        tuple: (data, event time, start time, end time)
    """
    from ..utils.constants import EVENT_PARAMS
    
    if event_name not in EVENT_PARAMS:
        raise ValueError(f"Unknown event: {event_name}")
    
    params = EVENT_PARAMS[event_name]
    data = fetch_ligo_data(detector, params['start_time'], params['end_time'])
    
    return data, params['event_time'], params['start_time'], params['end_time']
