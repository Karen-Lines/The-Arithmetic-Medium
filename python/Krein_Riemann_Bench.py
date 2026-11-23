import numpy as np
import matplotlib.pyplot as plt
import mpmath as mp
from mpl_toolkits.mplot3d import Axes3D

# Set precision
mp.dps = 50

# Define the grid
sigma = np.linspace(0.1, 0.9, 100)
t = np.linspace(0, 50, 100)
S, T = np.meshgrid(sigma, t)
Z = S + 1j * T

# The completed zeta function (stable version)
def completed_zeta(s):
    # Use the fact that ξ(s) = 1/2 s(s-1) π^{-s/2} Γ(s/2) ζ(s)
    # For numerical stability, use the log form when needed
    return mp.zeta(s) * s * (s - 1) * mp.gamma(s / 2) * (mp.pi ** (-s / 2)) / 2

# Compute the magnitude and phase on the grid
magnitude = np.zeros_like(Z, dtype=float)
phase = np.zeros_like(Z, dtype=float)
for i in range(Z.shape[0]):
    for j in range(Z.shape[1]):
        s = Z[i, j]
        xi_s = completed_zeta(s)
        magnitude[i, j] = float(abs(xi_s))
        phase[i, j] = np.angle(complex(xi_s))

# Plot
fig = plt.figure(figsize=(14, 6))

# 3D Magnitude (the zeros as pits)
ax1 = fig.add_subplot(121, projection='3d')
log_mag = np.log10(magnitude + 1e-50)
ax1.plot_surface(S, T, log_mag, cmap='viridis')
ax1.set_xlabel('Re(s) = σ')
ax1.set_ylabel('Im(s) = t')
ax1.set_zlabel('log10 |ξ(s)|')
ax1.set_title('3D Magnitude (Zeros as Pits)')
ax1.plot([0.5, 0.5], [0, 50], [np.min(log_mag)]*2, 
         color='red', linewidth=2, label='Critical Line')
ax1.legend()

# 2D Phase (the winding)
ax2 = fig.add_subplot(122)
im = ax2.imshow(phase, extent=[0.1, 0.9, 0, 50], origin='lower', cmap='twilight', aspect='auto')
ax2.axvline(0.5, color='red', linewidth=2, label='Critical Line (σ = 1/2)')
ax2.set_xlabel('Re(s) = σ')
ax2.set_ylabel('Im(s) = t')
ax2.set_title('2D Phase (Mirror Winding)')
plt.colorbar(im, ax=ax2, label='Phase of ξ(s)')

plt.tight_layout()
plt.show()
