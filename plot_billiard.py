import numpy as np
import matplotlib.pyplot as plt

# Load the single data file
try:
    x, y = np.loadtxt('simulation_data.txt', unpack=True)
except OSError:
    print("No data found! Run the C simulation first.")
    exit()

fig, ax = plt.subplots()
ax.plot(x, y, label='Trajectory')

# Draw the boundary
circle = plt.Circle((0, 0), 7.5, fill=False, color='black')
ax.add_artist(circle)

# Optional: Draw the flat line if it looks like a semi-circle (checking data)
if np.min(y) > -0.1: # Heuristic check
    plt.axhline(0, color='black', linestyle='-')

ax.set_aspect('equal')
plt.show()
