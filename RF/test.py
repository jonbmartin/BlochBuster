import numpy as np

def mybir4(n, beta, kappa, theta, dw0):
    r"""Design a BIR-4 adiabatic pulse.

    BIR-4 is equivalent to two BIR-1 pulses back-to-back.

    Args:
        n (int): number of samples (should be a multiple of 4).
        beta (float): AM waveform parameter.
        kappa (float): FM waveform parameter.
        theta (float): flip angle in radians.
        dw0: FM waveform scaling (radians/s).

    Returns:
        2-element tuple containing

        - **a** (*array*): AM waveform.
        - **om** (*array*): FM waveform (radians/s).

    References:
        Staewen, R.S. et al. (1990). '3-D FLASH Imaging using a single surface
        coil and a new adiabatic pulse, BIR-4'.
        Invest. Radiology, 25:559-567.
    """

    dphi1 = np.pi + theta / 2
    dphi2 = - np.pi + theta / 2

    t = np.arange(0, n) / n

    a1 = np.tanh(beta * (1 - 4 * t[: n // 4]))
    a2 = np.tanh(beta * (4 * t[n // 4 : n // 2] - 1))
    a3 = np.tanh(beta * (3 - 4 * t[n // 2 : 3 * n // 4]))
    a4 = np.tanh(beta * (4 * t[3 * n // 4 :] - 3))

    a = np.concatenate((a1, a2, a3, a4)).astype(np.complex64)
    a[n // 4 : 3 * n // 4] = a[n // 4 : 3 * n // 4] 

    # Apply phase shifts
    a[: n // 2] *= np.exp(1j * dphi1)
    a[n // 2:] *= np.exp(1j * dphi2)

    om1 = dw0 * np.tan(kappa * 4 * t[: n // 4]) / np.tan(kappa)
    om2 = dw0 * np.tan(kappa * (4 * t[n // 4 : n // 2] - 2)) / np.tan(kappa)
    om3 = dw0 * np.tan(kappa * (4 * t[n // 2 : 3 * n // 4] - 2)) / np.tan(kappa)
    om4 = dw0 * np.tan(kappa * (4 * t[3 * n // 4 :] - 4)) / np.tan(kappa)
    
    om = np.concatenate((om1, om2, om3, om4))

    return a, om