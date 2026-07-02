"""
Signal filtering utilities.
"""

from gwpy.signal import filter_design

def design_filters(sample_rate):
    """
    Design the filter set.
    
    Args:
        sample_rate: Sampling rate.
    
    Returns:
        tuple: (bandpass filter, list of notch filters, combined filter)
    """
    # Design the bandpass filter (50-250 Hz).
    bp = filter_design.bandpass(50, 250, sample_rate)
    
    # Design notch filters to remove power-line interference.
    notches = [filter_design.notch(line, sample_rate) for line in (60, 120, 180)]
    
    # Combine all filters.
    zpk = filter_design.concatenate_zpks(bp, *notches)
    
    return bp, notches, zpk

def apply_filters(data, zpk, crop_edges=True):
    """
    Apply filters to the data.
    
    Args:
        data: Input data.
        zpk: Filter in zero-pole-gain format.
        crop_edges: Whether to crop edges after filtering.
    
    Returns:
        TimeSeries: Filtered data.
    """
    # Apply the filter.
    filtered_data = data.filter(zpk, filtfilt=True)
    
    # Crop data edges to reduce edge effects.
    if crop_edges:
        data = data.crop(*data.span.contract(1))
        filtered_data = filtered_data.crop(*filtered_data.span.contract(1))
    
    return filtered_data

def process_signal(data):
    """
    Run the complete signal-processing workflow.
    
    Args:
        data: Raw data.
    
    Returns:
        tuple: (filtered data, filter)
    """
    # Design filters.
    bp, notches, zpk = design_filters(data.sample_rate)
    
    # Apply filters.
    filtered_data = apply_filters(data, zpk)
    
    return filtered_data, zpk
