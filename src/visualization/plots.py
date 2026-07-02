"""
Plotting utilities for gravitational-wave data visualization.
"""

import matplotlib.pyplot as plt
from gwpy.plot import Plot

def plot_spectral_density(data, title=None, show_power_lines=True):
    """
    Plot amplitude spectral density.
    
    Args:
        data: Strain data.
        title: Plot title.
        show_power_lines: Whether to show power-line interference.
    """
    asd = data.asd()
    
    plt.figure(figsize=[10, 6])
    plt.plot(asd.frequencies, asd, color='blue', linewidth=1)
    plt.xlim(10, 2000)
    plt.ylim(1e-24, 1e-19)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude Spectral Density [strain/√Hz]')
    
    if title:
        plt.title(title)
    
    plt.grid(True, alpha=0.3)
    
    # Mark power-line interference.
    if show_power_lines:
        for freq in [60, 120, 180]:
            plt.axvline(freq, linestyle="--", color="red", alpha=0.5)
    
    plt.tight_layout()
    return plt.gcf()

def plot_time_series(original_data, filtered_data, title=None):
    """
    Plot a time-domain comparison between raw and filtered data.
    
    Args:
        original_data: Raw data.
        filtered_data: Filtered data.
        title: Plot title.
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
    
    ax1.text(1.0, 1.01, 'Unfiltered Data', transform=ax1.transAxes, ha='right')
    ax1.set_ylabel('Amplitude [strain]', y=-0.2)
    
    ax2.set_ylabel('')
    ax2.text(1.0, 1.01, '50-250 Hz bandpass, 60/120/180 Hz notch filters',
             transform=ax2.transAxes, ha='right')
    
    return plot

def plot_filter_comparison(original_data, filtered_data, title=None):
    """
    Plot a spectral comparison before and after filtering.
    """
    plt.figure(figsize=[12, 8])
    
    # ASD of the raw data.
    asd_original = original_data.asd()
    plt.plot(asd_original.frequencies, asd_original,
             label='Raw Data', color='red', alpha=0.7, linewidth=1.5)
    
    # ASD of the filtered data.
    asd_filtered = filtered_data.asd()
    plt.plot(asd_filtered.frequencies, asd_filtered,
             label='Filtered Data', color='blue', alpha=0.7, linewidth=1.5)
    
    plt.xlim(10, 2000)
    plt.ylim(1e-24, 1e-19)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude Spectral Density [strain/√Hz]')
    
    # Mark the filter range.
    plt.axvspan(50, 250, alpha=0.1, color='green', label='Bandpass Region (50-250 Hz)')
    
    # Mark notch-filter frequencies.
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
    Plot a Q-transform time-frequency map.
    
    Args:
        data: Filtered data.
        event_time: Event time.
        time_window: Time window in seconds.
    """
    hq = data.q_transform(outseg=(event_time-time_window, event_time+time_window/2))
    plot = hq.plot()
    ax = plot.gca()
    plot.colorbar(label="Normalized Energy")
    ax.grid(False)
    ax.set_yscale('log')
    
    return plot

def plot_detector_comparison(hfilt, lfilt, event_time, event_name):
    """
    Plot a dual-detector comparison.
    """
    plot = Plot(figsize=[12, 4])
    ax = plot.gca()
    ax.plot(hfilt, label='LIGO-Hanford', color='black')
    ax.plot(lfilt, label='LIGO-Livingston', color='gray')
    
    ax.set_title(f'LIGO Strain Data ({event_name})')
    ax.set_xlim(event_time-0.3, event_time+0.3)
    ax.set_xscale('seconds', epoch=event_time)
    ax.set_ylabel('Amplitude [strain]')
    ax.set_ylim(-1e-21, 1e-21)
    ax.legend()
    
    return plot
