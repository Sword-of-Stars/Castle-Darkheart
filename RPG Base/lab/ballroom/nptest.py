import numpy as np
import matplotlib.pyplot as plt

# Define theta values
theta = np.linspace(0, 2*np.pi, 1000)

# Define parameters
a = 1  # amplitude
n = 6  # number of petals
phi = np.pi/6  # phase shift (adjust to ensure the rose doesn't touch the origin)

# Define the polar equation for the rose curve
r = a * np.cos(n*theta + phi)

# Plot the curve
plt.figure(figsize=(8, 8))
plt.polar(theta, r, color='blue')
plt.title('Polar Curve for a Rose with Phase Shift')
plt.show()
