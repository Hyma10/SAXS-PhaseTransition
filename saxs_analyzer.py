import os
import numpy as np
import matplotlib.pyplot as plt

# Create output directory for plots if it doesn't exist
os.makedirs('output_plots', exist_ok=True)

def simulate_saxs_profile(q, peak_positions, intensities, sigma=0.03):
    """Generates a synthetic 1D SAXS intensity profile with Gaussian peaks."""
    I = np.zeros_like(q)
    for pos, amp in zip(peak_positions, intensities):
        I += amp * np.exp(-((q - pos) ** 2) / (2 * sigma ** 2))
    # Add a smooth background scattering decay
    background = 0.5 / (q + 0.1)
    return background + I

# Momentum transfer vector (q) range in inverse Angstroms
q = np.linspace(0.01, 0.3, 300)

# Time points for kinetic evolution (tracking lamellar repeat-spacing shifts)
time_points = np.linspace(0, 60, 5) # 5 time frames
plt.figure(figsize=(10, 6))

colors = ['#008080', '#20B2AA', '#4682B4', '#6A5ACD', '#9370DB']

for i, t in enumerate(time_points):
    # Simulate gradual shift in peak positions due to structural swelling/transition
    q1 = 0.08 + (t * 0.0003)
    q2 = 0.16 + (t * 0.0006) # Higher order reflection (2q)
    
    intensities = [2.5 - (t * 0.01), 1.2 + (t * 0.005)]
    I_profile = simulate_saxs_profile(q, [q1, q2], intensities)
    
    # Offset profiles vertically for clear multi-line visualization
    offset_profile = I_profile + (i * 0.8)
    plt.plot(q, offset_profile, color=colors[i], linewidth=2, label=f'Time = {int(t)} min')

plt.title('Time-Resolved SAXS Structural Evolution During Phase Transition', fontsize=12, fontweight='bold')
plt.xlabel(r'Scattering Vector \(q\) (\(\AA^{-1}\))', fontsize=11)
plt.ylabel(r'Intensity \(I(q)\) + Offset (a.u.)', fontsize=11)
plt.legend(frameon=True, facecolor='#f8f9fa')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()

# Save the plot automatically
plt.savefig('output_plots/saxs_structural_evolution.png', dpi=300)
plt.show()
