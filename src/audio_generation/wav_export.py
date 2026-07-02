"""
Audio-file generation utilities.
"""

import numpy as np
from scipy.io.wavfile import write

def signal_to_audio(time_data, amplitude_data, event_time, time_window=1.5):
    """
    Convert signal data into audio data.
    
    Args:
        time_data: Time array.
        amplitude_data: Amplitude array.
        event_time: Event time.
        time_window: Time window in seconds.
    
    Returns:
        tuple: (sample rate, audio data)
    """
    # Extract data near the event.
    mask = (time_data < (event_time + time_window)) & (time_data > (event_time - time_window))
    y = amplitude_data[mask]
    
    # Normalize the signal.
    y = y / np.max(np.abs(y))
    
    # Calculate the effective sample rate.
    time_diff = np.diff(time_data[mask])
    fs = int(1 / np.median(time_diff))
    
    # Convert to 16-bit integer format.
    amplitude = np.iinfo(np.int16).max
    audio_data = (np.array(y) * amplitude).astype(np.int16)
    
    return fs, audio_data

def generate_gravitational_wave_audio(time_data, amplitude_data, event_time, 
                                    filename=None, event_name="GW"):
    """
    Generate a gravitational-wave audio file.
    
    Args:
        time_data: Time array.
        amplitude_data: Amplitude array.
        event_time: Event time.
        filename: Output filename.
        event_name: Event name.
    """
    if filename is None:
        filename = f"gravitational_wave_{event_name}.wav"
    
    # Convert signal data to audio data.
    fs, audio_data = signal_to_audio(time_data, amplitude_data, event_time)
    
    # Write the WAV file.
    write(filename, fs, audio_data)
    
    print(f"Audio file generated: {filename}")
    print(f"Sample rate: {fs} Hz")
    print(f"Audio duration: {len(audio_data)/fs:.2f} seconds")
    
    return filename, fs, audio_data
