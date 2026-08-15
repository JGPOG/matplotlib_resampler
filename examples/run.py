import matplotlib.pyplot as plt
import numpy as np
from matplotlib_resampler import DynamicDownsampler

# Set seed for reproducible random noise and spikes
np.random.seed(42)

# Parameters
fs = 1_000_000  # Sampling frequency (Hz)
duration = 1  # Duration in seconds
freq = 1.0  # Sine wave frequency (Hz)

# 1. Generate time vector and 1 Hz sine wave
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
sine_wave = np.sin(2 * np.pi * freq * t)

# 2. Add Gaussian noise
noise = np.random.normal(loc=0.0, scale=0.2, size=len(t))
noisy_sine = sine_wave + noise

# 3. Add 10 random spikes
num_spikes = 10
spike_indices = np.random.choice(len(t), size=num_spikes, replace=False)
spike_amplitudes = np.random.choice([-1, 1], size=num_spikes) * np.random.uniform(
    2.5, 4.0, size=num_spikes
)

signal = noisy_sine.copy()
signal[spike_indices] += spike_amplitudes

# 4. Plot using matplotlib
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