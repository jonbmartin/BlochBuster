import numpy as np
import matplotlib.pyplot as plt
import sigpy.mri.rf as rfsp

# Design it
n = 1176
dt = 4e-6 # [s]
dw0 = 100*np.pi/dt/n
beta = 10
kappa = np.arctan(20)
flip90 = np.pi/2 #np.pi
# flip180 = np.pi

[am_bir90, om_bir90] = rfsp.adiabatic.bir4(n, beta, kappa, flip90, dw0)
# [am_bir180, om_bir180] = mybir4(n, beta, kappa, flip180, dw0)

phi =  np.cumsum(om_bir90) * dt * 180 / np.pi # [degrees]
# for ii in range(0,np.size(phi)):
#     if am_bir90[ii] < 0:
#         # am_bir90[ii] = abs(am_bir90[ii])
#         phi[ii] = phi[ii] + 180*2

# Wrap phase to [-180, 180] range
# phi = ((phi + 180) % 360) - 180


# Plot it
T = n*dt
print('pulse duration: ', T*1000, 'ms')
t = np.arange(-T/2,T/2,dt)*1000
plt.figure()
plt.plot(t, np.real(am_bir90))
# plt.plot(t, np.real(am_bir180))
plt.xlabel('ms')
plt.ylabel('a.u.')
plt.title('|AM|')
plt.figure()
plt.plot(t, om_bir90/(2*np.pi))
# plt.plot(t, om_bir180/(2*np.pi*1000))
plt.xlabel('ms')
plt.ylabel('Hz')
plt.title('FM')
plt.figure()
plt.plot(phi)

# Save to YAML format
output_file = 'RF/bir4-90-test.yml'
amp = np.real(am_bir90.flatten())
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
print(f"Number of amplitude values: {len(amp)}")
print(f"Number of phase values: {len(phase)}")
