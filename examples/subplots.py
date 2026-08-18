import numpy as np
import matplotlib.pyplot as plt
from matplotlib_resampler import DynamicDownsampler

def generate_sine_wave_plots(n, num_spikes):

    # Create the horizontal axis (0 to 4*pi)
    x = np.linspace(0, 4 * np.pi, n)
    
    # Define four different noise multipliers
    noise_levels = [0.1, 0.25, 0.5, 0.8]
    
    # Set up a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Sine Waves with Varying Noise and Exactly 10 Random Spikes', fontsize=16, fontweight='bold')

    for i, ax in enumerate(axs.flat):
        # 1. Base Sine Wave
        y = np.sin(x)
        
        # 2. Add Gaussian (normal) noise
        noise = np.random.randn(n) * noise_levels[i]
        y_noisy = y + noise
        
        # 3. Add 10 random spikes
        # Select 10 random indices along the array length
        spike_indices = np.random.choice(n, size=num_spikes, replace=False)
        
        # Generate random spike magnitudes (both positive and negative)
        spike_magnitudes = np.random.uniform(3, 5, size=num_spikes) * np.random.choice([-1, 1], size=num_spikes)
        
        # Inject spikes into the noisy data
        y_spiky = y_noisy.copy()
        y_spiky[spike_indices] += spike_magnitudes
        
        # 4. Plotting and Styling
        ax.plot(x, y_spiky, label='Noisy Wave', color='royalblue', alpha=0.8)
        
        ax.set_title(f'Noise Level Coefficient: {noise_levels[i]}', fontsize=12)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper right')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    DynamicDownsampler(plt)
    plt.show()

# Execute the generator with as many points as you want
generate_sine_wave_plots(n=250_000_000, num_spikes=10)
