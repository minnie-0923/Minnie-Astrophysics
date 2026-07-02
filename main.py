#!/usr/bin/env python3
"""
Gravitational Wave Data Analysis Main Program
Based on LIGO data from GW150914 and GW170817 events
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import warnings
warnings.filterwarnings('ignore')

# ==================== Import necessary libraries ====================
try:
    from gwpy.timeseries import TimeSeries
    from gwpy.signal import filter_design
    from gwpy.plot import Plot
except ImportError:
    print("Error: Please install GWPy library first: pip install gwpy")
    exit(1)


def analyze_gravitational_wave(event_type=2, generate_audio=True):
    """
    Main analysis function
    
    Parameters:
    event_type: 1=GW170817, 2=GW150914
    generate_audio: whether to generate audio files
    """
    
    print(f"Starting gravitational-wave analysis for: {'GW170817' if event_type == 1 else 'GW150914'}")
    print("=" * 50)
    
    # ==================== Data acquisition ====================
    print("Fetching strain data from GWOSC...")
    
    if event_type == 1:
        # GW170817 - binary neutron-star merger
        t0 = 1187008882.4
        start_time = 1187008842
        end_time = 1187008922
        event_name = "GW170817"
    else:
        # GW150914 - first detected binary black-hole merger
        t0 = 1126259462.4
        start_time = 1126259446
        end_time = 1126259478
        event_name = "GW150914"
    
    # Fetch Hanford detector data.
    hdata = TimeSeries.fetch_open_data('H1', start_time, end_time)
    print(f"Fetched {event_name} data successfully: {len(hdata)} samples")
    
    # ==================== Spectral analysis ====================
    print("Running spectral analysis...")

    plt.figure(figsize=[10, 6])
    asd = hdata.asd()
    plt.plot(asd.frequencies, asd, color='blue', linewidth=1)
    plt.xlim(10, 2000)
    plt.ylim(1e-24, 1e-19)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude Spectral Density [strain/√Hz]')
    plt.title(f'{event_name} - LIGO Hanford Amplitude Spectral Density')
    plt.grid(True, alpha=0.3)

    # Mark power-line interference.
    ymin, ymax = 1e-24, 1e-19
    for freq in [60, 120, 180]:
        plt.axvline(freq, linestyle="--", color="red", alpha=0.5)

    plt.tight_layout()
    plt.savefig(f'results/plots/{event_name}_ASD.png', dpi=300, bbox_inches='tight')
    plt.show()

    # ==================== Filter design and application ====================
    print("Designing and applying filters...")
    bp = filter_design.bandpass(50, 250, hdata.sample_rate)
    notches = [filter_design.notch(line, hdata.sample_rate) for line in (60, 120, 180)]
    zpk = filter_design.concatenate_zpks(bp, *notches)

    hfilt = hdata.filter(zpk, filtfilt=True)
    hdata_cropped = hdata.crop(*hdata.span.contract(1))
    hfilt = hfilt.crop(*hfilt.span.contract(1))
    print("Filter application complete")

    # ==================== Filter visualization ====================
    print("Plotting filter comparison...")

    plot = Plot(
        hdata,
        hfilt, 
        figsize=[12, 6],
        separate=True,
        sharex=True,
        color='black'
    )
    ax1, ax2 = plot.axes

    ax1.set_title(f'LIGO-Hanford Strain Data ({event_name})')
    ax1.text(1.0, 1.01, 'Raw Data', transform=ax1.transAxes, ha='right')
    ax1.set_ylabel('Strain Amplitude', y=-0.2)

    ax2.set_ylabel('')
    ax2.text(1.0, 1.01, '50-250 Hz Bandpass, 60/120/180 Hz Notch Filters',
            transform=ax2.transAxes, ha='right')

    plot.savefig(f'results/plots/{event_name}_filter_comparison.png', dpi=300)
    plot.show()

    # ==================== ASD comparison before and after filtering ====================
    print("Comparing spectra before and after filtering...")

    plt.figure(figsize=[12, 8])

    asd_original = hdata.asd()
    plt.plot(asd_original.frequencies, asd_original,
            label='Original Data', color='red', alpha=0.7, linewidth=1.5)

    asd_filtered = hfilt.asd()
    plt.plot(asd_filtered.frequencies, asd_filtered,
            label='Filtered Data', color='blue', alpha=0.7, linewidth=1.5)

    plt.xlim(10, 2000)
    plt.ylim(1e-24, 1e-19)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude Spectral Density [strain/√Hz]')

    # Mark the filter range.
    plt.axvspan(50, 250, alpha=0.1, color='green', label='Bandpass Region (50-250 Hz)')

    for freq in [60, 120, 180]:
        plt.axvline(freq, linestyle="--", color="orange", alpha=0.7)

    plt.legend(loc='upper right')
    plt.title(f'LIGO-Hanford ASD Comparison: Original vs Filtered Data ({event_name})')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(f'results/plots/{event_name}_ASD_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

    # ==================== Filtered signal detail ====================
    print("Inspecting filtered signal details...")

    plot = hfilt.plot(color='black')
    ax = plot.gca()
    ax.set_ylabel('Strain Amplitude')

    if event_type == 1:
        ax.set_title('LIGO-Hanford Strain Data (GW170817)')
        ax.set_xlim(1187008862, 1187008902)
        ax.set_xscale('seconds', epoch=1187008862)
    else:
        ax.set_title('LIGO-Hanford Strain Data (GW150914)')
        ax.set_xlim(1126259462, 1126259462.6)
        ax.set_xscale('seconds', epoch=1126259462)

    plot.savefig(f'results/plots/{event_name}_filtered_strain.png', dpi=300)
    plot.show()

    x_val = np.array(hfilt.times.value)
    y_val = np.array(hfilt.value)

    # ==================== Dual-detector comparison ====================
    print("Fetching Livingston detector data for comparison...")

    if event_type == 1:
        ldata = TimeSeries.fetch_open_data('L1', 1187008862, 1187008902)
    else:
        ldata = TimeSeries.fetch_open_data('L1', 1126259446, 1126259478)

    # Apply the same filter.
    lfilt = ldata.filter(zpk, filtfilt=True)

    # Shift L1 in time and adjust phase to compare detector responses.
    lfilt.shift('6.9ms')
    lfilt *= -1

    # Plot the two detector data streams.
    plot = Plot(figsize=[12, 4])
    ax = plot.gca()
    ax.plot(hfilt, label='LIGO-Hanford', color='black')
    ax.plot(lfilt, label='LIGO-Livingston', color='gray')

    if event_type == 1:
        ax.set_title('LIGO Strain Data (GW170817)')
        ax.set_xlim(1187008862, 1187008902)
        ax.set_xscale('seconds', epoch=1187008842)
    else:
        ax.set_title('LIGO Strain Data (GW150914)')
        ax.set_xlim(1126259462, 1126259462.6)
        ax.set_xscale('seconds', epoch=1126259462)

    ax.set_ylabel('Strain Amplitude')
    ax.set_ylim(-1e-21, 1e-21)
    ax.legend()
    plot.savefig(f'results/comparison/{event_name}_detector_comparison.png', dpi=300)
    plot.show()

    # ==================== Q-transform time-frequency analysis ====================
    print("Running Q-transform time-frequency analysis...")

    if event_type == 1:
        dt_0 = 10
        dt_1 = 10
    else:
        dt_0 = 0.2
        dt_1 = 0.1
        
    hq = hfilt.q_transform(outseg=(t0-dt_0, t0+dt_1))
    fig4 = hq.plot()
    ax = fig4.gca()
    fig4.colorbar(label="Normalized Energy")
    ax.grid(False)
    ax.set_yscale('log')
    plt.savefig(f'results/plots/{event_name}_q_transform.png', dpi=300, bbox_inches='tight')
    plt.show()

    # ==================== Audio generation ====================
    if generate_audio:
        print("Generating gravitational-wave audio file...")
        
        amplitude = np.iinfo(np.int16).max
        
        # Extract data within 1.5 seconds of the event for audio conversion.
        ind = np.where((x_val < (t0+1.5)) & (x_val > (t0-1.5)))
        y = y_val[ind]
        
        # Normalize the signal.
        y = y / np.max(np.abs(y))
        
        # Calculate the effective sample rate and write the WAV file.
        fs = int(1 / np.median(np.diff(np.array(x_val[ind] - t0))))
        print(f"Audio sampling rate fs = {fs}")
        
        filename = f"audio/gravitational_wave_{event_name}.wav"
        write(filename, fs, (np.array(y) * amplitude).astype(np.int16))
        print(f"Audio file saved: {filename}")

    print("=" * 50)
    print("Analysis complete. All figures have been saved to the results/ folder.")
    return hdata, hfilt


if __name__ == "__main__":
    # Example usage.
    print("Gravitational-Wave Data Analysis Program")
    print("Choose an event to analyze:")
    print("1. GW170817 (binary neutron-star merger)")
    print("2. GW150914 (binary black-hole merger)")
    
    try:
        choice = int(input("Enter your choice (1 or 2, default 2): ") or "2")
        audio_choice = input("Generate an audio file? (y/n, default y): ").lower() or "y"
        
        generate_audio = audio_choice in ['y', 'yes']
        
        # Run the analysis.
        original_data, filtered_data = analyze_gravitational_wave(
            event_type=choice,
            generate_audio=generate_audio
        )
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
