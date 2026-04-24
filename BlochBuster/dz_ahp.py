import numpy as np
import matplotlib.pyplot as plt
import sigpy.mri.rf as rfsp

# Design adiabatic half passage pulse
n = 512  # number of time points
dt = 4e-6  # time step [s]
beta = 80  # modulation parameter (larger = more adiabatic)
mu = 5  # controls bandwidth
flip = np.pi/2  # 90 degree flip angle

# Create frequency sweep (hyperbolic secant modulation)
T = n * dt
t = np.arange(0, n) * dt - T/2

# Frequency modulation (FM) - hyperbolic tangent
A = mu / T
om = A * np.tanh(beta * t / T)

# Amplitude modulation (AM) - sech envelope
# For AHP: flip ≈ (π * B1_max * T) / beta
B1_max = flip * beta / (np.pi * T)
am = B1_max * (1 / np.cosh(beta * t / T))

# Calculate phase from frequency
phi = np.cumsum(om) * dt * 180 / np.pi  # [degrees]

# Handle negative amplitudes
for ii in range(0, np.size(phi)):
    if am[ii] < 0:
        am[ii] = abs(am[ii])
        phi[ii] = phi[ii] + 180

# Wrap phase to [-180, 180] range
phi = ((phi + 180) % 360) - 180

# Plot it
t_ms = t * 1000
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t_ms, am)
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude (a.u.)')
plt.title('AHP Amplitude Modulation')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t_ms, om / (2 * np.pi))
plt.xlabel('Time (ms)')
plt.ylabel('Frequency (Hz)')
plt.title('AHP Frequency Modulation')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t_ms, phi)
plt.xlabel('Time (ms)')
plt.ylabel('Phase (degrees)')
plt.title('AHP Phase')
plt.grid(True)

plt.tight_layout()
plt.show()

# Save to YAML format
output_file = 'RF/ahp_90.yml'
amp = np.real(am.flatten())
phase = phi.flatten()

with open(output_file, 'w') as f:
    # Write amp array on a single line
    f.write('amp: [')
    f.write(','.join(f'{v:.5f}' for v in amp))
    f.write(']\n')
    
    # Write phase array on a single line
    f.write('phase: [')
    f.write(','.join(f'{v:.5f}' for v in phase))
    f.write(']\n')

print(f"Successfully created {output_file}")
print(f"Pulse duration: {T*1000:.3f} ms")
print(f"Number of amplitude values: {len(amp)}")
print(f"Number of phase values: {len(phase)}")
print(f"Max B1: {np.max(amp):.5f}")
