# Matplotlib Dynamic Downsampler
### High Performance Time-Series Visualization

A python package for universal **data downsampling and interactive visualization** 
using Matplotlib and tsdownsampler.

`matplotlib_resampler` improves scalability of `Matplotlib` for visualizing massive time-series
datasets. The library *dynamically* **resamples time-series data respective to the current
graph view**, ensuring fast, responsive updates during panning or zooming. 

This aggregation functionality is achieved by utilizing highly optimized data point selection
algorithms from **tsdownsample**. Our default data aggregation method is MinMaxLTTB (defaulting
to 5,000 points per view), which guarantees maximum visual fidelity and preserves narrow data spikes.

This works with more than 1 plot and can visualize over 1 Billion data points.

## Features

- **Convenient and "Plug & Play"**: Just pass your existing plt object to our class constructor. Preserves all original Matplotlib styling, colors, labels and figure configurations.
- **No Backend Servers Required**: Requires zero web servers, Dash apps, or Jupyter widget overhead.
    Runs entirely via Matplotlib's native event backend.
- **Efficient visualization of large datasets**: Dynamic zooming in and out while keeping high fidelity
    based on user's point preference.

## Installation

Clone the repository:
git clone https://github.com/JGPOG/matplotlib_resampler.git

Install the package:
pip install matplotlib_resampler\dist\matplotlib_resampler-0.1.0-py3-none-any.whl

## Usage
Add dynamic aggregation to your figure with minimal overhead.

```python 
import numpy as np
import matplotlib.pyplot as plt
from tsdownsample import MinMaxLTTBDownsampler

plt.figure(figsize=(10, 5))
plt.plot(t, signal, label="Noisy 1 Hz Sine Wave")

plt.title("1 Hz Noisy Sine Wave with 10 Random Spikes")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(loc="upper right")
plt.tight_layout()
DynamicDownsampler(plt)
plt.show()
```

`In example demo, 200,000,000 data points across 4 subplots (50M each) are visualized!`

## Matplotlib Standalone vs Matplotlib + Resampler
DynamicDownsampler() acts as an invisible wrapper around standard Matplotlib figures.
It adds visualization scalability to line charts by resampling the data based on GUI zoom or pan events. 
- **Standard Matplotlib** attempts to render more points than the computer may be capable of handling. 
- **matplotlib_enhancer** intercepts these points *before* rendering and only plots
    a mathematically representative downsampled version. When you zoom in, it
    automatically recalculates and reveals the high resolution details for that window.

## Important Considerations & Tips

- **Sorting Requirement**: The underlying tsdownsample Rust engine requires your X-axis data
    to be monotonic/sorted and free of NaN values.
- **Aliasing and Signal Spikes**: MinMaxLTTB ensures extreme peaks and troughs in raw data are never
    accidentally skipped when rendering a zoomed out view.
- **None Networked/Portable Installations**: If you have installed using a non networked or portable folder, there is a chance you receive an error about the figure not being interactive and it won't plot. In this case you need to install PyQt6. 
