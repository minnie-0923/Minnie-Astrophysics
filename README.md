# Minnie-Astrophysics

An astrophysics data-analysis project that explores LIGO gravitational-wave events through signal processing, visualization, detector comparison, and audio sonification.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![GWPy](https://img.shields.io/badge/GWPy-3.0%2B-orange)](https://gwpy.github.io/)

## Project Overview

This repository analyzes public LIGO data from two landmark gravitational-wave detections:

- **GW150914**: the first direct detection of gravitational waves, produced by a binary black-hole merger.
- **GW170817**: a historic binary neutron-star merger with electromagnetic counterparts, marking a major moment in multi-messenger astronomy.

The project uses open data from the Gravitational Wave Open Science Center (GWOSC) to turn raw strain measurements into interpretable scientific outputs: amplitude spectral density plots, filtered strain curves, Q-transform time-frequency maps, detector comparisons, and audible WAV files.

## Key Features

- **Open data access**: downloads LIGO strain data directly from GWOSC.
- **Spectral analysis**: computes amplitude spectral density (ASD) to inspect detector noise and signal bands.
- **Signal filtering**: applies a 50-250 Hz bandpass filter and notch filters at 60, 120, and 180 Hz.
- **Time-frequency analysis**: uses Q-transforms to visualize gravitational-wave chirp structure.
- **Multi-detector comparison**: compares Hanford (H1) and Livingston (L1) data after time-shift and phase adjustment.
- **Audio sonification**: converts gravitational-wave strain data into audible WAV files.

## Repository Structure

```text
Minnie-Astrophysics/
├── src/                     # Source code
│   ├── data_processing/     # Data download and filtering utilities
│   ├── visualization/       # Plotting functions
│   ├── audio_generation/    # WAV conversion utilities
│   └── utils/               # Constants and shared parameters
├── notebooks/               # Jupyter notebooks
│   ├── GW150914_Analysis.ipynb
│   └── GW170817_Analysis.ipynb
├── audio/                   # Generated gravitational-wave audio files
├── results/                 # Analysis outputs
│   ├── plots/               # Generated plots
│   └── comparison/          # Multi-detector comparison figures
├── requirement.txt
└── README.md
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/minnie-0923/Minnie-Astrophysics.git
cd Minnie-Astrophysics
```

### 2. Install Dependencies

```bash
pip install -r requirement.txt
```

### 3. Run the Analysis

Use the main Python script:

```bash
python main.py
```

Or open one of the event-specific notebooks:

```bash
jupyter notebook notebooks/GW150914_Analysis.ipynb
```

## Analysis Workflow

### 1. Data Acquisition

The project retrieves strain data from the Hanford (H1) and Livingston (L1) LIGO detectors through GWOSC.

### 2. Spectral Analysis

- Calculates amplitude spectral density (ASD).
- Identifies power-line interference at 60, 120, and 180 Hz.
- Examines detector noise characteristics across frequency bands.

### 3. Signal Filtering

- Uses a 50-250 Hz bandpass filter to preserve the frequency range where the gravitational-wave signal is most visible.
- Applies notch filters to suppress power-line noise.
- Uses zero-phase filtering to reduce phase distortion.

### 4. Time-Domain Analysis

- Compares raw and filtered strain data.
- Focuses on the signal window surrounding each event.
- Visualizes how the strain amplitude changes near the merger.

### 5. Time-Frequency Analysis

- Uses Q-transforms to show how signal frequency changes over time.
- Highlights the chirp-like structure of compact-object mergers.
- Displays normalized energy distribution in the time-frequency plane.

### 6. Multi-Detector Comparison

- Compares Hanford and Livingston detections.
- Applies a 6.9 ms time shift to account for arrival-time differences.
- Adjusts phase to compare the two detector responses more clearly.

### 7. Audio Generation

- Normalizes the filtered strain signal.
- Converts the selected time window into 16-bit WAV format.
- Creates an audible representation of gravitational-wave data.

## Scientific Context

According to general relativity, gravitational waves are ripples in spacetime produced by accelerating massive objects. Binary black-hole and neutron-star mergers generate signals with three characteristic stages:

- **Inspiral**: the objects orbit closer together and the signal frequency rises.
- **Merger**: the compact objects combine, producing the strongest part of the signal.
- **Ringdown**: the final object settles into a stable state.

This project examines how those physical events appear in real detector data, showing the path from raw observation to processed evidence.

## Main Dependencies

- **GWPy**: gravitational-wave data access and analysis.
- **NumPy / SciPy**: numerical computing and signal processing.
- **Matplotlib**: scientific visualization.
- **Jupyter**: interactive analysis notebooks.

## Example Filter Design

```python
# Bandpass filter: 50-250 Hz
bp = filter_design.bandpass(50, 250, hdata.sample_rate)

# Notch filters: remove power-line interference
notches = [filter_design.notch(line, hdata.sample_rate) for line in (60, 120, 180)]
```

## Outputs

The repository generates several kinds of analysis products:

- Amplitude spectral density plots.
- Raw versus filtered strain comparisons.
- Q-transform time-frequency maps.
- Hanford-Livingston detector comparisons.
- Gravitational-wave audio files.

## Acknowledgments

- Open data provided by the LIGO Scientific Collaboration and the Gravitational Wave Open Science Center.
- Analysis tools provided by the GWPy development team.
- Inspired in part by github.com/wj198414/ASTRON1221.
